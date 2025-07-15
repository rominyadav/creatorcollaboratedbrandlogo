import csv
import os

def clean_field(value):
    """Sanitize commas in fields (replace with ' | ')."""
    if isinstance(value, str):
        return value.replace(',', ' ')
    return value

def get_output_columns(file_type):
    """Get the appropriate output columns based on file type."""
    base_columns = [
        "email",
        "primary_social_link",
        "username",
        "first_name",
        "last_name",
        "address_city",
        "address_state",
        "address_country",
        "address_zip",
        "collaboration_status",
        "creator_type",
        "top_collaboration",
        "hashtags",
        "niche_primary",
        "niche_secondary",
        "follower_count",
        "creator_size",
        "age_group",
        "age",
        "gender",
        "phone_number",
        "profile_picture",
        "tiktok_link",
        "linktree_link",
        "other_social_media",
        "business_category",
        "mention",
        "latitude",
        "longitude",
        "street_address",
    ]
    
    if file_type == "creator_pic":
        base_columns.append("top_collaboration_creator_pic")
    else:
        base_columns.append("top_collaboration_brand_logo")
    
    return base_columns

def process_creators_csv(input_file, output_file, file_type):
    """Process a single CSV file with error handling."""
    try:
        if not os.path.exists(input_file):
            print(f"Warning: Input file '{input_file}' does not exist. Skipping...")
            return False

        with open(input_file, 'r', encoding='utf-8') as infile:
            raw_reader = csv.reader(infile)
            raw_headers = next(raw_reader)

            seen = set()
            unique_headers = []
            header_indices = []
            for idx, col in enumerate(raw_headers):
                # Remove duplicates and exclude columns ending with '.1'
                if col not in seen and not col.endswith('.1'):
                    seen.add(col)
                    unique_headers.append(col)
                    header_indices.append(idx)

            infile.seek(0)
            next(infile)  # skip header

            reader = csv.reader(infile)
            rows = []
            for row in reader:
                cleaned_row = {unique_headers[i]: row[header_indices[i]] for i in range(len(unique_headers)) if i < len(row)}
                rows.append(cleaned_row)

        # Get appropriate output columns
        output_columns = get_output_columns(file_type)

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=output_columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for row in rows:
                # Handle GPS coordinates
                gps = row.get('gps_coordinate', '')
                if ',' in gps:
                    parts = gps.split(',', 1)
                    row['latitude'] = parts[0].strip()
                    row['longitude'] = parts[1].strip()
                else:
                    row['latitude'] = ''
                    row['longitude'] = ''

                # Remove gps_coordinate from row dict if present
                row.pop('gps_coordinate', None)

                # Ensure all output columns exist in the row
                for col in output_columns:
                    if col not in row:
                        row[col] = ''

                # Sanitize all fields (replace commas)
                sanitized_row = {key: clean_field(value) for key, value in row.items()}

                # Write row with exact columns order
                writer.writerow({col: sanitized_row.get(col, '') for col in output_columns})

        print(f"Successfully processed '{input_file}' -> '{output_file}'")
        return True

    except Exception as e:
        print(f"Error processing file '{input_file}': {str(e)}")
        return False

def process_all_files():
    """Process all four CSV files."""
    files_to_process = [
        {
            'input': 'brand_with_creator_pic.csv',
            'output': 'sanitized/brand_with_creator_pic_sanitized.csv',
            'type': 'creator_pic'
        },
        {
            'input': 'brand_with_no_creator.csv',
            'output': 'sanitized/brand_with_no_creator_sanitized.csv',
            'type': 'brand_logo'
        },
        {
            'input': 'creator_with_brand_logo.csv',
            'output': 'sanitized/creator_with_brand_logo_sanitized.csv',
            'type': 'brand_logo'
        },
        {
            'input': 'creator_with_no_brand.csv',
            'output': 'sanitized/creator_with_no_brand_sanitized.csv',
            'type': 'brand_logo'
        }
    ]

    processed_count = 0
    for file_info in files_to_process:
        if process_creators_csv(file_info['input'], file_info['output'], file_info['type']):
            processed_count += 1

    print(f"\nProcessing complete: {processed_count} out of {len(files_to_process)} files processed successfully.")

if __name__ == "__main__":
    process_all_files()
