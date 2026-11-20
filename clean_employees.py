"""Clean a messy employee CSV and log every change.

Input : raw_employees.csv
Output: cleaned_employees.csv, cleaning_log.md
"""
import re
import pandas as pd

RAW = "raw_employees.csv"
OUT = "cleaned_employees.csv"
LOG = "cleaning_log.md"

CITY_MAP = {"calcutta": "Kolkata", "gauhati": "Guwahati", "bangalore": "Bengaluru"}

log = []
def note(step, detail):
    log.append(f"- **{step}:** {detail}")

df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
note("Loaded", f"{len(df)} rows, {df.shape[1]} columns from `{RAW}`")

# 1. Trim spaces everywhere
before = df.copy()
df = df.apply(lambda col: col.str.strip())
changed = (before != df).sum().sum()
note("Trimmed whitespace", f"{changed} cell values had leading or trailing spaces")

# 2. Standardise city names
def clean_city(c):
    key = c.lower()
    if key in CITY_MAP:
        return CITY_MAP[key]
    return c.title()
city_before = df["city"].copy()
df["city"] = df["city"].map(clean_city)
note("Standardised city names", f"{(city_before != df['city']).sum()} city values changed (e.g., 'Calcutta' to 'Kolkata', 'KOLKATA' to 'Kolkata')")

# 3. Remove exact duplicate rows
dups = df.duplicated().sum()
df = df.drop_duplicates()
note("Removed exact duplicates", f"{dups} duplicate rows removed; {len(df)} rows remain")

# 4. Parse dates: accept ISO (2026-04-10) and day/month/year (24/10/2026)
def parse_date(s):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return pd.to_datetime(s, format="%Y-%m-%d")
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s):
        return pd.to_datetime(s, format="%d/%m/%Y")
    return pd.NaT
parsed = df["join_date"].map(parse_date)
bad_dates = parsed.isna().sum()
mixed = df["join_date"].str.contains("/").sum()
df["join_date"] = parsed.dt.strftime("%Y-%m-%d")
note("Standardised dates", f"{mixed} dates were in day/month/year format and were converted to YYYY-MM-DD; {bad_dates} could not be parsed")

# 5. Salaries: '17k' -> 17000, blank -> missing
def parse_salary(s):
    s = s.strip().lower().replace(",", "")
    if s == "":
        return None
    if s.endswith("k"):
        return int(float(s[:-1]) * 1000)
    return int(float(s))
df["monthly_salary_inr"] = df["monthly_salary_inr"].map(parse_salary)
missing_salary = df["monthly_salary_inr"].isna().sum()
note("Converted salaries to numbers", f"values like '17k' converted to 17000; {missing_salary} rows have no salary and were left blank (not guessed)")

# 6. Department: blank -> 'Unknown'
blank_dept = (df["department"] == "").sum()
df["department"] = df["department"].replace("", "Unknown")
note("Filled blank departments", f"{blank_dept} blank departments set to 'Unknown'")

# 7. Final validation
assert df["employee_id"].is_unique, "Duplicate employee IDs remain"
assert df["join_date"].str.match(r"\d{4}-\d{2}-\d{2}").all(), "Bad date format remains"
note("Validation passed", "employee IDs are unique and all dates are in YYYY-MM-DD format")

df.to_csv(OUT, index=False)
note("Saved", f"`{OUT}` with {len(df)} rows")

with open(LOG, "w", encoding="utf-8") as f:
    f.write("# Cleaning log\n\n")
    f.write("\n".join(log) + "\n")

print("\n".join(log))
