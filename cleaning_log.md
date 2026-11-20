# Cleaning log

- **Loaded:** 192 rows, 6 columns from `raw_employees.csv`
- **Trimmed whitespace:** 25 cell values had leading or trailing spaces
- **Standardised city names:** 92 city values changed (e.g., 'Calcutta' to 'Kolkata', 'KOLKATA' to 'Kolkata')
- **Removed exact duplicates:** 12 duplicate rows removed; 180 rows remain
- **Standardised dates:** 43 dates were in day/month/year format and were converted to YYYY-MM-DD; 0 could not be parsed
- **Converted salaries to numbers:** values like '17k' converted to 17000; 69 rows have no salary and were left blank (not guessed)
- **Filled blank departments:** 40 blank departments set to 'Unknown'
- **Validation passed:** employee IDs are unique and all dates are in YYYY-MM-DD format
- **Saved:** `cleaned_employees.csv` with 180 rows
