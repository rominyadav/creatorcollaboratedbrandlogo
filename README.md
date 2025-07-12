Brand Logo Filtering Pipeline

Overview

This project processes Instagram creator data to identify business (brand) accounts that appear in the top_collaboration field of content‑creator profiles, then attaches direct links to each brand’s logo image. The result is a clean, analytics‑ready CSV you can feed into downstream dashboards or partner‑matching engines.

Why this matters

Influencer discovery often clutters a brand’s shortlist with other creators or accounts that lack a clear brand identity. By filtering purely for business accounts backed by verified logo‑style avatars, you get a high‑confidence list of real brands that have already collaborated with your creators.

File Glossary

File

Purpose

input_main.csv

Master dataset of Instagram profiles. Must contain at least username, creator_type, and top_collaboration columns.

imageclassification.csv

Map of profile‑image filenames (<username>.jpg) to a single column, classification, whose value is either logo or pic.

main.py

Pipeline script implementing the logic described below.

creatorWithNonBlankTopCollaboration.csv

Intermediate – content creators whose top_collaboration field is non‑empty.

missing.csv

Intermediate – usernames referenced in top_collaboration that do not exist in input_main.csv.

creator_with_brand_logo.csv

Final output – creators paired with a filtered, logo‑verified list of brand collaborators plus ready‑to‑use logo URLs.

Pipeline at a Glance

Select creators of interest – keep rows where creator_type == "Content Creator" and top_collaboration isn’t blank.

Keep only known business collaborators

Split top_collaboration on |.

Remove usernames absent from input_main.csv (logged to missing.csv).

Drop collaborators whose own creator_type equals Content Creator; keep those flagged Business.

Enforce logo avatars – cross‑reference each remaining collaborator with imageclassification.csv. Remove usernames classified as pic.

Generate branded logo URLs – produce top_collaboration_brand_logo where each entry looks like:

angarajewelry;https://insta.rominyadav.com.np/angarajewelry.jpg | cariloha;https://insta.rominyadav.com.np/cariloha.jpg

Save results – write cleaned creators and their verified brand‑logo partners to creator_with_brand_logo.csv.

Quick‑start

# 1. Clone or copy the repo
# 2. Install dependencies
python -m pip install pandas

# 3. Place input CSVs in the project root
# 4. Execute the pipeline
python filter_brand_logo.py

All intermediate and final CSVs will appear alongside your script.

CSV Schema Details

input_main.csv (required columns)

Column

Example

Notes

username

my_influencer

Lower‑case, no leading @

creator_type

Content Creator / Business

Case‑sensitive match to the two strings the script expects

top_collaboration

`brand_1

brand_2

brand_3`

Pipe‑separated usernames

imageclassification.csv

Column

Example

filename

brand_1.jpg

classification

logo / pic

Output Example

After running, creator_with_brand_logo.csv includes all original columns plus:

top_collaboration

top_collaboration_brand_logo

`brand_1

brand_2`

`brand_1;https://insta.rominyadav.com.np/brand_1.jpg

brand_2;https://insta.rominyadav.com.np/brand_2.jpg`

Tip: The semicolon (;) separates the username from its logo URL; adjust downstream parsers accordingly.

Customisation

Logo host URL – swap the base URL inside generate_logo_urls() if your logos live elsewhere.

Business definition – update the username_type_map lookup if you track brands via another flag.

Additional filters – insert extra conditions in the process_collaborations() or filter_by_logo() helpers.

Troubleshooting

Symptom

Likely Cause

Fix

creator_with_brand_logo.csv is empty

All collaborators were creators or lacked logos

Verify that imageclassification.csv is up‑to‑date and that your creators do indeed collaborate with brands

Missing usernames overflow

Many refs absent from input_main.csv

Update your master dataset or run audits on top_collaboration integrity

License

MIT © 2025 Your Name – free for commercial and private use.

Contributing

Pull requests are welcome! Feel free to open issues for bugs or feature ideas.

Author

Romin Yadav – Team Lead, Data Filtration