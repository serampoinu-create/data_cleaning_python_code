# Data Cleaning with Python (practice project)

A Python script that cleans a messy employee dataset and writes a log of every change.

**Data:** `raw_employees.csv` is synthetic practice data with realistic problems. It is not real employee information.

## Problems the script fixes
- Extra spaces around values
- Inconsistent city names (for example, "Calcutta", "KOLKATA", and "Bangalore" standardised to one name each)
- Two date formats mixed together (YYYY-MM-DD and DD/MM/YYYY)
- Salaries written as text, such as "17k"
- Missing salaries, which are left blank rather than guessed
- Blank departments, filled as "Unknown"
- Exact duplicate rows

## Files
- `clean_employees.py`: the cleaning script (pandas)
- `raw_employees.csv`: input data
- `cleaned_employees.csv`: output
- `cleaning_log.md`: a record of each step and how many rows or values it changed
- `make_messy.py`: generates the practice input file

## How to run
```
pip install pandas
python clean_employees.py
```

## Skills demonstrated
- Loading and inspecting data with pandas
- Writing repeatable cleaning steps instead of editing by hand
- Parsing dates and numbers safely, with explicit formats
- Documenting changes so the process can be audited
- Adding validation checks that fail loudly if something is wrong
