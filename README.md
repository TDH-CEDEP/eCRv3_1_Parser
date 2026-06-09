# **eCRv3_1_Parser**

![https://img.shields.io/badge/License-MIT-green.svg](https://img.shields.io/badge/License-MIT-green.svg)
![https://img.shields.io/badge/Python-3.14+-blue.svg](https://img.shields.io/badge/Python-3.14+-blue.svg)
![https://img.shields.io/badge/Status-Active-lightgrey.svg](https://img.shields.io/badge/Status-Active-lightgrey.svg)

## Overview

**eCRv3_1_Parser** is a Python-based extraction tool designed to process **electronic Initial Case Report (eICR)** documents delivered as ZIP archives. It parses CDA‑based HL7 v3 XML files, extracts a very large set of clinical, demographic, and encounter‑level data elements, and outputs them into a consolidated CSV file suitable for downstream analysis.

The tool was built primarily for **epidemiologic and public health surveillance** workflows, enabling rapid ingestion of high‑volume eCR feeds for analytics, case investigation support, or integration into broader reporting systems.

Although originally developed for a specific workflow, the script contains no proprietary dependencies and can be adapted for other data pipelines with minimal modification.

---

## Key Features

- Automatically walks file directories to locate ZIP files for a given date.
- Extracts CDA‑compliant **eICR v3.1** XML content.
- Parses and exports over **300+ structured data fields** (patient info, provider, immunizations, occupations, pregnancy data, risk factors, clinical elements, procedures, observations, etc.).
- Writes all extracted values to a **single daily CSV output**.
- Designed for repeated daily ingestion without manual cleanup.
- Cross‑platform compatible with minor path adjustments (developed on Windows).

---

## Intended Audience

This tool is targeted primarily at:

- Public health epidemiologists  
- Surveillance system developers  
- Informatics teams working with HL7 CDA or eICR formats  
- Analysts processing eICR feeds for case investigation or population-level reporting  

---

## Requirements

### Python Version
The script was written and tested using:

- **Python 3.14.2**

Based on syntax and imports, this script **will not run on Python 2.x**.  
It should run correctly on **Python 3.7+**, but has not been validated outside 3.14.

### Required Python Libraries

The script uses the following external modules:

- `pandas`
- `lxml` (specifically `lxml.etree`)
- `csv`
- `glob`
- `zipfile`

These can be installed via:

```
pip install pandas lxml
```

---

## Setup

Before running the script, users **must manually set three variables inside the file**:

### 1. `eICR_file_path`
The root directory where ZIP files are stored.

```
eICR_file_path = "C:\\path\\to\\your\\incoming\\zips"
```

### 2. `output_path`
Directory where the final CSV output is written.

```
output_path = "C:\\path\\to\\output\\directory"
```

### 3. `extract_location`
Temporary directory for unzipped XML files.

```
extract_location = "C:\\path\\to\\scratch\\workspace"
```

These paths can point to local or network-mounted directories.

---

## How to Use

1. Ensure directories exist and the variables above are populated.
2. Place the incoming ZIP files in the correct date-based folder structure:
   ```
   <eICR_file_path>\<year>\<year><month>\<yyyymmdd>\
   ```
3. Run the script:
   ```
   python eCRv3_1_Parser.py
   ```
4. The output CSV will appear at:
   ```
   <output_path>\<yyyymmdd>_zip.csv
   ```
5. Each run appends new rows to the existing output file for that date.

---

## File Structure Expectations

Your directory structure must follow:

```
eICR_file_path
└── YYYY
    └── YYYYMM
        └── YYYYMMDD
            ├── file1.zip
            ├── file2.zip
            └── ...
```

Inside each ZIP, the expected CDA file is named:

```
CDA_eICR.xml
```

---

## Error Handling

Two helper functions are defined within the script:

- `set_wdir()` — safely changes working directory.
- `printException()` — prints detailed traceback including file, line number, and offending code.

These functions are used during directory navigation and XML parsing to provide clear debugging information.

---

## Extensibility Notes

Although this tool was developed quickly to address an immediate need, it includes a strong structural foundation for future enhancements. Some areas that could be expanded include:

- Output to SQL databases instead of CSV  
- Automated cleanup of extracted XML files  
- Multiprocessing for very large daily volumes  
- Schema validation against HL7 CDA introduction  
- More robust logging system  

If community interest emerges, contributions are welcome.

---

## License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this project with proper attribution.

---

## GitHub Badges Included

- MIT License  
- Python version  
- Project status (Active)

If you'd like more (code coverage, tests, Docker builds), I can add them.

---

## Flow Diagram

             Daily ZIP Delivery (from EHR/HIE)
                             │
                             ▼
                ┌────────────────────────┐
                │   Date-Based Folder    │
                │   <YYYY>/<YYYYMM>/     │
                │   <YYYYMMDD>/          │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │     ZIP Extraction      │
                │   (extract_location)    │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │     CDA_eICR.xml       │
                │   Loaded via lxml.etree│
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │     XML Parsing        │
                │  300+ HL7 CDA fields   │
                │  (patient, provider,   │
                │   encounter, labs,     │
                │   occupation, etc.)    │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   Row Assembly         │
                │   Python CSV writer    │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   Output CSV File      │
                │ <output_path>/<date>   │
                │     _zip.csv           │
                └────────────────────────┘
                             │
                             ▼
         Ready for Epidemiology / Public Health Analysis
