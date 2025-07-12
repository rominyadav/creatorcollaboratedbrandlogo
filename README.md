# Brand Logo Filtering Pipeline

## 🧠 Overview

This project processes Instagram creator data to identify **business (brand) accounts** that appear in the `top_collaboration` field of **content creator** profiles, and appends direct links to each brand’s logo image. The result: a clean, analytics-ready CSV for dashboards or partner-matching engines.

## 🎯 Why This Matters

Influencer discovery often clutters a brand’s shortlist with other creators or accounts lacking clear brand identity. By filtering purely for **business accounts** backed by verified **logo-style avatars**, you get a **high-confidence list of real brands** that have collaborated with your creators.

---

## 📁 File Glossary

| File                                      | Purpose                                                                                                                        |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `input_main.csv`                          | Master dataset of Instagram profiles. Must contain at least `username`, `creator_type`, and `top_collaboration` columns.       |
| `imageclassification.csv`                 | Maps profile image filenames (`<username>.jpg`) to a `classification` of either `logo` or `pic`.                              |
| `main.py`                                 | Pipeline script implementing the logic described below.                                                                        |
| `creatorWithNonBlankTopCollaboration.csv` | **Intermediate** — content creators with non-empty `top_collaboration`.                                                        |
| `missing.csv`                             | **Intermediate** — usernames in `top_collaboration` not found in `input_main.csv`.                                             |
| `creator_with_brand_logo.csv`             | **Final output** — creators paired with filtered, logo-verified brand collaborators and their logo URLs.                       |

---

## 🔄 Pipeline at a Glance

1. **Filter content creators**  
   Keep rows where `creator_type == "Content Creator"` and `top_collaboration` is not blank.

2. **Validate & clean collaborators**  
   - Split `top_collaboration` on `|`  
   - Drop unknown usernames (log to `missing.csv`)  
   - Keep only usernames with `creator_type == "Business"`

3. **Logo check**  
   - Cross-reference with `imageclassification.csv`  
   - Remove collaborators classified as `pic`

4. **Generate logo URLs**  
   Add a new column `top_collaboration_brand_logo` like:
   ```
   angarajewelry;https://insta.rominyadav.com.np/angarajewelry.jpg | cariloha;https://insta.rominyadav.com.np/cariloha.jpg
   ```

5. **Export**  
   Save final data to `creator_with_brand_logo.csv`

---

## 🚀 Quick Start

```bash
# 1. Clone or copy the repo
# 2. Install dependencies
python -m pip install pandas

# 3. Place your CSVs in the project root
# 4. Run the script
python main.py
```

Output files (`*.csv`) will be saved in the same directory.

---

## 📊 CSV Schema Details

### `input_main.csv`

| Column            | Example          | Notes                                                        |
| ----------------- | ---------------- | ------------------------------------------------------------ |
| `username`        | `my_influencer`  | Lowercase, no leading `@`                                    |
| `creator_type`    | `Content Creator` / `Business` | Case-sensitive exact match                                   |
| `top_collaboration` | `brand_1 | brand_2 | brand_3` | Pipe (`|`) separated usernames                         |

### `imageclassification.csv`

| Column            | Example         |
| ----------------- | --------------- |
| `filename`        | `brand_1.jpg`   |
| `classification`  | `logo` / `pic`  |

---

## ✅ Output Example

Final `creator_with_brand_logo.csv` includes:

| top_collaboration        | top_collaboration_brand_logo                                                                                  |
|--------------------------|----------------------------------------------------------------------------------------------------------------|
| `brand_1 | brand_2`       | `brand_1;https://insta.rominyadav.com.np/brand_1.jpg | brand_2;https://insta.rominyadav.com.np/brand_2.jpg` |

> 💡 **Note:** Each username is paired with its logo URL using a `;`. You can split by `;` and `|` for downstream processing.

---

## ⚙️ Customization

- 🔗 **Change logo host URL**  
  Modify `generate_logo_urls()` to point to a different image server.

- 🧠 **Redefine business logic**  
  Adjust how `username_type_map` classifies Business vs Creator.

- 🛠 **Add filters**  
  Extend `process_collaborations()` or `filter_by_logo()` with new rules as needed.

---

## 🧯 Troubleshooting

| Issue                                | Likely Cause                                    | Solution                                                                                         |
|-------------------------------------|-------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `creator_with_brand_logo.csv` is empty | All collaborators were creators or lacked logos | Check if `imageclassification.csv` is updated and creators actually collaborate with brands     |
| Many usernames in `missing.csv`     | `top_collaboration` includes unknown usernames  | Update your `input_main.csv` or audit `top_collaboration` values for accuracy                   |

---

## 📄 License

MIT © 2025 **Your Name** — Free for commercial and private use.

---

## 🤝 Contributing

Pull requests welcome! Feel free to open issues for bugs or suggestions.

---

## 👤 Author

**Romin Yadav**  
Team Lead, Data Filtration
