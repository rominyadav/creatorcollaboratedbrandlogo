import pandas as pd
import os
import csv

def main():
    print("Starting brand logo filtering process...")
    
    # Step 1: Filter creators with non-blank top_collaboration
    print("Step 1: Loading and filtering content creators with non-blank collaborations...")
    df_main = pd.read_csv('input_main.csv', low_memory=False)
    
    # Filter for Content Creator type with non-empty top_collaboration
    creators_with_collab = df_main[(df_main['creator_type'] == 'Content Creator') & 
                                  (df_main['top_collaboration'].notna()) & 
                                  (df_main['top_collaboration'] != '')]
    
    print(f"Found {len(creators_with_collab)} content creators with non-blank collaborations")
    creators_with_collab.to_csv(
        'creatorWithNonBlankTopCollaboration.csv',
        index=False,
        quoting=csv.QUOTE_ALL)
    
    # Step 2: Process and filter top_collaboration entries
    print("Step 2: Processing top_collaboration entries...")
    
    # Create a dictionary to store missing usernames
    missing_usernames = []
    
    # Create a set of all usernames in the main dataset for quick lookup
    all_usernames = set(df_main['username'].dropna())
    
    # Create a mapping of username to creator_type for quick lookup
    username_type_map = dict(zip(df_main['username'], df_main['creator_type']))
    
    # Process each row to filter top_collaboration
    def process_collaborations(row):
        if pd.isna(row['top_collaboration']):
            return ''
            
        collaborations = [username.strip() for username in row['top_collaboration'].split('|')]
        filtered_collabs = []
        
        for username in collaborations:
            username = username.strip()
            if username in all_usernames:
                # Check if username is a Business account
                if username_type_map.get(username) == 'Business':
                    filtered_collabs.append(username)
                # else it's a Content Creator, so we drop it
            else:
                # Username doesn't exist in input_main.csv
                missing_usernames.append({'username': username, 'source': row['username']})
        
        return ' | '.join(filtered_collabs) if filtered_collabs else ''
    
    # Apply the processing to each row
    creators_with_collab['top_collaboration'] = creators_with_collab.apply(process_collaborations, axis=1)
    
    # Filter out rows where top_collaboration became empty after processing
    creators_with_collab = creators_with_collab[creators_with_collab['top_collaboration'] != '']
    print(f"After filtering out non-business collaborations: {len(creators_with_collab)} rows")
    
    # Save missing usernames to CSV
    pd.DataFrame(missing_usernames).to_csv(
        'missing.csv',
        index=False,
        quoting=csv.QUOTE_ALL)
    
    # Step 3: Filter by logo classification
    print("Step 3: Filtering by logo classification...")
    
    # Load image classification data
    image_classification = pd.read_csv('imageclassification.csv')
    
    # Create a dictionary mapping filename to classification for quick lookup
    # Assuming filenames in the CSV are just the username.jpg
    filename_to_classification = {}
    for _, row in image_classification.iterrows():
        filename = row['filename']
        classification = row['classification']
        username = os.path.splitext(filename)[0]  # Remove .jpg extension
        filename_to_classification[username] = classification
    
    def filter_by_logo(collaboration_str):
        if pd.isna(collaboration_str) or collaboration_str == '':
            return ''
            
        usernames = [username.strip() for username in collaboration_str.split('|')]
        logo_usernames = []
        
        for username in usernames:
            # Check if this username has a logo classification
            if username in filename_to_classification and filename_to_classification[username] == 'logo':
                logo_usernames.append(username)
                
        return ' | '.join(logo_usernames) if logo_usernames else ''
    
    # Apply the logo filtering
    creators_with_collab['top_collaboration'] = creators_with_collab['top_collaboration'].apply(filter_by_logo)
    
    # Filter out rows where top_collaboration became empty after logo filtering
    creators_with_collab = creators_with_collab[creators_with_collab['top_collaboration'] != '']
    print(f"After filtering for logo classifications: {len(creators_with_collab)} rows")
    
    # Step 4: Add top_collaboration_brand_logo column
    print("Step 4: Generating brand logo URLs...")
    
    def generate_logo_urls(collaboration_str):
        if pd.isna(collaboration_str) or collaboration_str == '':
            return ''
            
        usernames = [username.strip() for username in collaboration_str.split('|')]
        formatted_entries = []
        
        for username in usernames:
            logo_url = f"https://insta.rominyadav.com.np/{username}.jpg"
            formatted_entries.append(f"{username};{logo_url}")
                
        return ' | '.join(formatted_entries)
    
    creators_with_collab['top_collaboration_brand_logo'] = creators_with_collab['top_collaboration'].apply(generate_logo_urls)
    
    # Save the final output
    creators_with_collab.to_csv(
        'creator_with_brand_logo.csv',
        index=False,
        quoting=csv.QUOTE_ALL)
    print(f"Successfully created creator_with_brand_logo.csv with {len(creators_with_collab)} rows")

    # Step 5: Generate creator_with_no_brand.csv
    print("Step 5: Generating creator_with_no_brand.csv...")

    # Get all content creators from the main input
    all_content_creators = df_main[df_main['creator_type'] == 'Content Creator'].copy()

    # If 'top_collaboration_brand_logo' doesn't exist, add it as blank
    if 'top_collaboration_brand_logo' not in all_content_creators.columns:
        all_content_creators['top_collaboration_brand_logo'] = ''

    # Mark all usernames that are in the final brand logo file
    with_brand_usernames = set(creators_with_collab['username'])

    # Select those not in the brand logo file (i.e., with no brand logo)
    creators_with_no_brand = all_content_creators[~all_content_creators['username'].isin(with_brand_usernames)].copy()

    # Ensure output columns match
    output_columns = list(creators_with_collab.columns)
    for col in output_columns:
        if col not in creators_with_no_brand.columns:
            creators_with_no_brand[col] = ''

    creators_with_no_brand = creators_with_no_brand[output_columns]

    creators_with_no_brand.to_csv(
        'creator_with_no_brand.csv',
        index=False,
        quoting=csv.QUOTE_ALL)
    print(f"Successfully created creator_with_no_brand.csv with {len(creators_with_no_brand)} rows")


if __name__ == "__main__":
    main()
