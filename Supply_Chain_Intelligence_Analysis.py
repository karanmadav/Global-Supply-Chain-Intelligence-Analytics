#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd

print("Pandas is working")


# In[19]:


folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

print(folder)


# In[21]:


import os

print(os.path.exists(folder))


# In[23]:


files = os.listdir(folder)

for file in files:
    print(file)


# In[25]:


excel_files = []

for file in files:
    if file.endswith(".xlsx"):
        excel_files.append(file)

print(excel_files)


# In[27]:


print("Total Excel files:", len(excel_files))


# In[29]:


file_path = os.path.join(
    folder,
    "Export of goods and services (% of GDP).xlsx"
)

print(file_path)


# In[31]:


export_data = pd.read_excel(file_path)


# In[32]:


export_data.head()


# In[33]:


export_data.shape


# In[34]:


export_data.columns


# In[39]:


print("Hello Supply Chain Project")


# In[41]:


import pandas as pd
import os

print("Pandas is working")


# In[43]:


folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

print(os.path.exists(folder))


# In[45]:


files = os.listdir(folder)

for file in files:
    print(file)


# In[47]:


file_path = os.path.join(
    folder,
    "Export of goods and services (% of GDP).xlsx"
)

export_data = pd.read_excel(
    file_path,
    sheet_name="Data"
)

print("File loaded successfully!")


# In[48]:


export_data.head()


# In[49]:


print("Rows:", export_data.shape[0])
print("Columns:", export_data.shape[1])


# In[53]:


print(export_data.columns.tolist())


# In[55]:


export_data.isnull().sum()


# In[57]:


print(export_data["Country Name"].head(20))


# In[59]:


print("Total countries/rows:", export_data["Country Name"].nunique())


# In[63]:


export_data.head()


# In[65]:


# 1. Export data
export_data = pd.read_excel(
    os.path.join(folder, "Export of goods and services (% of GDP).xlsx"),
    sheet_name="Data"
)

# 2. GDP
gdp_data = pd.read_excel(
    os.path.join(folder, "GDP (Current US$).xlsx"),
    sheet_name="Data"
)

# 3. GDP Growth
growth_data = pd.read_excel(
    os.path.join(folder, "GDP Growth (annual %).xlsx"),
    sheet_name="Data"
)

# 4. Inflation
inflation_data = pd.read_excel(
    os.path.join(folder, "Inflation, consumer prices (annual %).xlsx"),
    sheet_name="Data"
)

# 5. Population
population_data = pd.read_excel(
    os.path.join(folder, "Population, Total.xlsx"),
    sheet_name="Data"
)

# 6. UN Comtrade
comtrade_data = pd.read_excel(
    os.path.join(folder, "UN Comtrade.xlsx"),
    sheet_name="Sheet2"
)

# 7. World Bank LPI
lpi_data = pd.read_excel(
    os.path.join(folder, "World Bank LPI.xlsx"),
    sheet_name="Data"
)

print("All 7 datasets loaded successfully! ✅")


# In[66]:


print("Export:", export_data.shape)
print("GDP:", gdp_data.shape)
print("GDP Growth:", growth_data.shape)
print("Inflation:", inflation_data.shape)
print("Population:", population_data.shape)
print("UN Comtrade:", comtrade_data.shape)
print("LPI:", lpi_data.shape)


# In[67]:


print("EXPORT COLUMNS")
print(export_data.columns.tolist())

print("\nGDP COLUMNS")
print(gdp_data.columns.tolist())

print("\nGROWTH COLUMNS")
print(growth_data.columns.tolist())

print("\nINFLATION COLUMNS")
print(inflation_data.columns.tolist())

print("\nPOPULATION COLUMNS")
print(population_data.columns.tolist())

print("\nCOMTRADE COLUMNS")
print(comtrade_data.columns.tolist())

print("\nLPI COLUMNS")
print(lpi_data.columns.tolist())


# In[68]:


def clean_world_bank_data(df, new_name):
    
    df = df.copy()
    
    # Keep country information
    df = df.drop(
        columns=["Series Name", "Series Code"],
        errors="ignore"
    )
    
    # Rename country columns
    df = df.rename(columns={
        "Country Name": "country",
        "Country Code": "country_code"
    })
    
    # Convert wide format to long format
    df = df.melt(
        id_vars=["country", "country_code"],
        var_name="year",
        value_name=new_name
    )
    
    # Extract only year
    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )
    
    # Convert year to number
    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )
    
    # Convert values to numbers
    df[new_name] = pd.to_numeric(
        df[new_name],
        errors="coerce"
    )
    
    return df


# In[79]:


export_clean = clean_world_bank_data(
    export_data,
    "export_pct_gdp"
)

gdp_clean = clean_world_bank_data(
    gdp_data,
    "gdp_usd"
)

growth_clean = clean_world_bank_data(
    growth_data,
    "gdp_growth_pct"
)

inflation_clean = clean_world_bank_data(
    inflation_data,
    "inflation_pct"
)

population_clean = clean_world_bank_data(
    population_data,
    "population"
)

print("All 5 economic datasets cleaned successfully! ✅")


# In[81]:


export_clean.head()


# In[69]:


master = gdp_clean.copy()


# In[ ]:


master = master.merge(
    export_clean,
    on=["country", "country_code", "year"],
    how="left"
)


# In[89]:


print("Master dataset shape:", master.shape)


# In[ ]:


master.head()


# In[ ]:


master.columns.tolist()


# In[ ]:


def clean_wb_data(df, value_name):
    df = df.copy()

    # Remove unnecessary columns
    df = df.drop(
        columns=["Series Name", "Series Code"],
        errors="ignore"
    )

    # Rename country columns
    df = df.rename(columns={
        "Country Name": "country",
        "Country Code": "country_code"
    })

    # Identify year columns
    year_columns = [
        col for col in df.columns
        if str(col)[:4].isdigit()
    ]

    # Keep required columns
    df = df[
        ["country", "country_code"] + year_columns
    ]

    # Convert wide → long
    df = df.melt(
        id_vars=["country", "country_code"],
        var_name="year",
        value_name=value_name
    )

    # Extract year
    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    # Convert values to numeric
    df[value_name] = pd.to_numeric(
        df[value_name],
        errors="coerce"
    )

    return df


# In[73]:


export = clean_wb_data(
    export_data,
    "export_pct_gdp"
)

gdp = clean_wb_data(
    gdp_data,
    "gdp_usd"
)

growth = clean_wb_data(
    growth_data,
    "gdp_growth_pct"
)

inflation = clean_wb_data(
    inflation_data,
    "inflation_pct"
)

population = clean_wb_data(
    population_data,
    "population"
)

print("All 5 economic datasets cleaned successfully! ✅")


# In[74]:


print(export.head())


# In[75]:


print("Export:", export.shape)
print("GDP:", gdp.shape)
print("Growth:", growth.shape)
print("Inflation:", inflation.shape)
print("Population:", population.shape)


# In[79]:


master = gdp.copy()

print(master.head())


# In[81]:


master = master.merge(
    export,
    on=["country", "country_code", "year"],
    how="left"
)

print(master.shape)


# In[9]:


def clean_world_bank_data(df, new_name):

    df = df.copy()

    df = df.drop(
        columns=["Series Name", "Series Code"],
        errors="ignore"
    )

    df = df.rename(columns={
        "Country Name": "country",
        "Country Code": "country_code"
    })

    df = df.melt(
        id_vars=["country", "country_code"],
        var_name="year",
        value_name=new_name
    )

    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    df[new_name] = pd.to_numeric(
        df[new_name],
        errors="coerce"
    )

    return df


# In[15]:


import pandas as pd
import os

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

gdp_data = pd.read_excel(
    os.path.join(folder, "GDP (Current US$).xlsx"),
    sheet_name="Data"
)

print("GDP data loaded successfully! ✅")
print(gdp_data.shape)
print(gdp_data.head())


# In[16]:


gdp_clean = clean_world_bank_data(
    gdp_data,
    "gdp_usd"
)

print("GDP Clean created successfully! ✅")
print(gdp_clean.shape)
print(gdp_clean.head())


# In[21]:


print([x for x in globals() if "export" in x.lower()])


# In[23]:


import os

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

print("FILES IN PROJECT FOLDER:\n")

for file in os.listdir(folder):
    print(file)


# In[29]:


import os

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

print("FILES IN PROJECT FOLDER:")
print("=" * 60)

for file in os.listdir(folder):
    print(file)


# In[33]:


import os

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

print("EXCEL FILES FOUND:")
print("=" * 60)

for file in os.listdir(folder):
    if file.lower().endswith((".xlsx", ".xls", ".csv")):
        print(file)


# In[35]:


import pandas as pd
import os

EXPORT_FILE = "Export of goods and services (% of GDP).xlsx"

export_path = os.path.join(folder, EXPORT_FILE)

print("Export file path:")
print(export_path)

print("\nFile exists:")
print(os.path.exists(export_path))

if os.path.exists(export_path):
    export_data = pd.read_excel(export_path)

    print("\n✅ EXPORT DATA LOADED SUCCESSFULLY!")
    print("Shape:", export_data.shape)

    print("\nColumns:")
    print(export_data.columns.tolist())

    print("\nFirst 5 rows:")
    display(export_data.head())
else:
    print("\n❌ Export file not found.")


# In[37]:


print("EXPORT DATA INFO")
print("=" * 60)

print("\nData Types:")
print(export_data.dtypes)

print("\nMissing Values:")
print(export_data.isna().sum())

print("\nDuplicate Rows:")
print(export_data.duplicated().sum())


# In[39]:


export_data.columns = (
    export_data.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Cleaned Export Columns:")
print(export_data.columns.tolist())


# In[41]:


print("EXPORT DATA SAMPLE")
print("=" * 60)

display(export_data.head(10))

print("\nLast 5 rows:")
display(export_data.tail())

print("\nShape:")
print(export_data.shape)

print("\nColumns:")
for col in export_data.columns:
    print("-", col)


# In[45]:


# ============================================================
# STEP 7 — EXPORT DATA CLEANING
# WIDE FORMAT → LONG FORMAT
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. Make a copy
# ------------------------------------------------------------

export_clean = export_data.copy()

print("Original Shape:", export_clean.shape)

# ------------------------------------------------------------
# 2. Clean column names
# ------------------------------------------------------------

export_clean.columns = (
    export_clean.columns
    .str.strip()
    .str.lower()
)

print("\nColumns:")
print(export_clean.columns.tolist())

# ------------------------------------------------------------
# 3. Identify year columns
# ------------------------------------------------------------

year_columns = [
    col for col in export_clean.columns
    if col[:4].isdigit()
]

print("\nYear Columns Found:")
print(year_columns)

print("\nNumber of year columns:", len(year_columns))

# ------------------------------------------------------------
# 4. Convert WIDE format to LONG format
# ------------------------------------------------------------

export_clean = export_clean.melt(
    id_vars=[
        "series_name",
        "series_code",
        "country_name",
        "country_code"
    ],
    value_vars=year_columns,
    var_name="year",
    value_name="exports_pct_gdp"
)

# ------------------------------------------------------------
# 5. Extract actual year number
# ------------------------------------------------------------

export_clean["year"] = (
    export_clean["year"]
    .str[:4]
    .astype(int)
)

# ------------------------------------------------------------
# 6. Clean country names
# ------------------------------------------------------------

export_clean["country_name"] = (
    export_clean["country_name"]
    .astype(str)
    .str.strip()
)

# ------------------------------------------------------------
# 7. Clean country codes
# ------------------------------------------------------------

export_clean["country_code"] = (
    export_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 8. Convert export value to numeric
# ------------------------------------------------------------

export_clean["exports_pct_gdp"] = pd.to_numeric(
    export_clean["exports_pct_gdp"],
    errors="coerce"
)

# ------------------------------------------------------------
# 9. Remove invalid rows
# ------------------------------------------------------------

export_clean = export_clean.dropna(
    subset=[
        "country_name",
        "year",
        "exports_pct_gdp"
    ]
)

# ------------------------------------------------------------
# 10. Rename country column
# ------------------------------------------------------------

export_clean = export_clean.rename(
    columns={
        "country_name": "country"
    }
)

# ------------------------------------------------------------
# 11. Keep only required columns
# ------------------------------------------------------------

export_clean = export_clean[
    [
        "country",
        "country_code",
        "year",
        "exports_pct_gdp"
    ]
]

# ------------------------------------------------------------
# 12. Remove duplicates
# ------------------------------------------------------------

before = len(export_clean)

export_clean = export_clean.drop_duplicates(
    subset=[
        "country",
        "country_code",
        "year"
    ],
    keep="first"
)

after = len(export_clean)

# ------------------------------------------------------------
# 13. Sort data
# ------------------------------------------------------------

export_clean = export_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)

# ------------------------------------------------------------
# 14. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✅ EXPORT CLEANING SUCCESSFUL")
print("=" * 60)

print("\nOriginal Shape:", export_data.shape)

print("Final Shape:", export_clean.shape)

print("Duplicates Removed:", before - after)

print("\nFinal Columns:")
print(export_clean.columns.tolist())

print("\nMissing Values:")
print(export_clean.isna().sum())

print("\nFirst 10 Rows:")
display(export_clean.head(10))


# In[49]:


# ============================================================
# STEP 8 — GDP GROWTH DATA CLEANING
# WIDE FORMAT → LONG FORMAT
# ============================================================

import pandas as pd
import os

# ------------------------------------------------------------
# 1. Load GDP Growth file again
# ------------------------------------------------------------

GROWTH_FILE = "GDP Growth (annual %).xlsx"

growth_path = os.path.join(folder, GROWTH_FILE)

print("File exists:")
print(os.path.exists(growth_path))

growth_data = pd.read_excel(growth_path)

print("\n✅ GDP GROWTH DATA LOADED")

print("Original Shape:", growth_data.shape)

# ------------------------------------------------------------
# 2. Rename first 4 columns safely
# ------------------------------------------------------------

growth_data = growth_data.rename(
    columns={
        growth_data.columns[0]: "series_name",
        growth_data.columns[1]: "series_code",
        growth_data.columns[2]: "country",
        growth_data.columns[3]: "country_code"
    }
)

# ------------------------------------------------------------
# 3. Identify year columns
# ------------------------------------------------------------

year_columns = [
    col for col in growth_data.columns
    if str(col)[:4].isdigit()
]

print("\nYear Columns Found:")
print(year_columns)

print("\nNumber of Years:", len(year_columns))

# ------------------------------------------------------------
# 4. Convert WIDE → LONG
# ------------------------------------------------------------

growth_clean = growth_data.melt(
    id_vars=[
        "series_name",
        "series_code",
        "country",
        "country_code"
    ],
    value_vars=year_columns,
    var_name="year",
    value_name="gdp_growth_pct"
)

# ------------------------------------------------------------
# 5. Extract year
# ------------------------------------------------------------

growth_clean["year"] = (
    growth_clean["year"]
    .astype(str)
    .str[:4]
)

growth_clean["year"] = pd.to_numeric(
    growth_clean["year"],
    errors="coerce"
)

# ------------------------------------------------------------
# 6. Clean country
# ------------------------------------------------------------

growth_clean["country"] = (
    growth_clean["country"]
    .astype(str)
    .str.strip()
)

# ------------------------------------------------------------
# 7. Clean country code
# ------------------------------------------------------------

growth_clean["country_code"] = (
    growth_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 8. Convert GDP growth to numeric
# ------------------------------------------------------------

growth_clean["gdp_growth_pct"] = pd.to_numeric(
    growth_clean["gdp_growth_pct"],
    errors="coerce"
)

# ------------------------------------------------------------
# 9. Remove invalid rows
# ------------------------------------------------------------

growth_clean = growth_clean.dropna(
    subset=[
        "country",
        "year",
        "gdp_growth_pct"
    ]
)

# ------------------------------------------------------------
# 10. Convert year to integer
# ------------------------------------------------------------

growth_clean["year"] = growth_clean["year"].astype(int)

# ------------------------------------------------------------
# 11. Keep only required columns
# ------------------------------------------------------------

growth_clean = growth_clean[
    [
        "country",
        "country_code",
        "year",
        "gdp_growth_pct"
    ]
]

# ------------------------------------------------------------
# 12. Remove duplicate country-year records
# ------------------------------------------------------------

before = len(growth_clean)

growth_clean = growth_clean.drop_duplicates(
    subset=[
        "country",
        "country_code",
        "year"
    ],
    keep="first"
)

after = len(growth_clean)

# ------------------------------------------------------------
# 13. Sort
# ------------------------------------------------------------

growth_clean = growth_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)

# ------------------------------------------------------------
# 14. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✅ GDP GROWTH CLEANING SUCCESSFUL")
print("=" * 60)

print("\nOriginal Shape:")
print(growth_data.shape)

print("\nFinal Shape:")
print(growth_clean.shape)

print("\nDuplicates Removed:")
print(before - after)

print("\nFinal Columns:")
print(growth_clean.columns.tolist())

print("\nMissing Values:")
print(growth_clean.isna().sum())

print("\nFirst 10 Rows:")
display(growth_clean.head(10))


# In[51]:


# ============================================================
# STEP 9 — INFLATION DATA CLEANING
# WIDE FORMAT → LONG FORMAT
# ============================================================

import pandas as pd
import os

# ------------------------------------------------------------
# 1. Load Inflation file
# ------------------------------------------------------------

INFLATION_FILE = "Inflation, consumer prices (annual %).xlsx"

inflation_path = os.path.join(folder, INFLATION_FILE)

print("File path:")
print(inflation_path)

print("\nFile exists:")
print(os.path.exists(inflation_path))

inflation_data = pd.read_excel(inflation_path)

print("\n✅ INFLATION DATA LOADED")

print("Original Shape:")
print(inflation_data.shape)

print("\nOriginal Columns:")
print(inflation_data.columns.tolist())

# ------------------------------------------------------------
# 2. Rename first 4 columns safely
# ------------------------------------------------------------

inflation_data = inflation_data.rename(
    columns={
        inflation_data.columns[0]: "series_name",
        inflation_data.columns[1]: "series_code",
        inflation_data.columns[2]: "country",
        inflation_data.columns[3]: "country_code"
    }
)

# ------------------------------------------------------------
# 3. Identify year columns
# ------------------------------------------------------------

year_columns = [
    col for col in inflation_data.columns
    if str(col)[:4].isdigit()
]

print("\nYear Columns Found:")
print(year_columns)

print("\nNumber of Years:")
print(len(year_columns))

# ------------------------------------------------------------
# 4. Convert WIDE → LONG
# ------------------------------------------------------------

inflation_clean = inflation_data.melt(
    id_vars=[
        "series_name",
        "series_code",
        "country",
        "country_code"
    ],
    value_vars=year_columns,
    var_name="year",
    value_name="inflation_pct"
)

# ------------------------------------------------------------
# 5. Extract year
# ------------------------------------------------------------

inflation_clean["year"] = (
    inflation_clean["year"]
    .astype(str)
    .str[:4]
)

inflation_clean["year"] = pd.to_numeric(
    inflation_clean["year"],
    errors="coerce"
)

# ------------------------------------------------------------
# 6. Clean country
# ------------------------------------------------------------

inflation_clean["country"] = (
    inflation_clean["country"]
    .astype(str)
    .str.strip()
)

# ------------------------------------------------------------
# 7. Clean country code
# ------------------------------------------------------------

inflation_clean["country_code"] = (
    inflation_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 8. Convert inflation value to numeric
# ------------------------------------------------------------

inflation_clean["inflation_pct"] = pd.to_numeric(
    inflation_clean["inflation_pct"],
    errors="coerce"
)

# ------------------------------------------------------------
# 9. Remove invalid rows
# ------------------------------------------------------------

inflation_clean = inflation_clean.dropna(
    subset=[
        "country",
        "year",
        "inflation_pct"
    ]
)

# ------------------------------------------------------------
# 10. Convert year to integer
# ------------------------------------------------------------

inflation_clean["year"] = inflation_clean["year"].astype(int)

# ------------------------------------------------------------
# 11. Keep required columns
# ------------------------------------------------------------

inflation_clean = inflation_clean[
    [
        "country",
        "country_code",
        "year",
        "inflation_pct"
    ]
]

# ------------------------------------------------------------
# 12. Remove duplicates
# ------------------------------------------------------------

before = len(inflation_clean)

inflation_clean = inflation_clean.drop_duplicates(
    subset=[
        "country",
        "country_code",
        "year"
    ],
    keep="first"
)

after = len(inflation_clean)

# ------------------------------------------------------------
# 13. Sort
# ------------------------------------------------------------

inflation_clean = inflation_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)

# ------------------------------------------------------------
# 14. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✅ INFLATION CLEANING SUCCESSFUL")
print("=" * 60)

print("\nOriginal Shape:")
print(inflation_data.shape)

print("\nFinal Shape:")
print(inflation_clean.shape)

print("\nDuplicates Removed:")
print(before - after)

print("\nFinal Columns:")
print(inflation_clean.columns.tolist())

print("\nMissing Values:")
print(inflation_clean.isna().sum())

print("\nFirst 10 Rows:")
display(inflation_clean.head(10))


# In[53]:


# ============================================================
# STEP 10 — POPULATION DATA CLEANING
# WIDE FORMAT → LONG FORMAT
# ============================================================

import pandas as pd
import os

# ------------------------------------------------------------
# 1. Load Population file
# ------------------------------------------------------------

POPULATION_FILE = "Population, Total.xlsx"

population_path = os.path.join(folder, POPULATION_FILE)

print("File path:")
print(population_path)

print("\nFile exists:")
print(os.path.exists(population_path))

population_data = pd.read_excel(population_path)

print("\n✅ POPULATION DATA LOADED")

print("Original Shape:")
print(population_data.shape)

print("\nOriginal Columns:")
print(population_data.columns.tolist())


# ------------------------------------------------------------
# 2. Rename first 4 columns safely
# ------------------------------------------------------------

population_data = population_data.rename(
    columns={
        population_data.columns[0]: "series_name",
        population_data.columns[1]: "series_code",
        population_data.columns[2]: "country",
        population_data.columns[3]: "country_code"
    }
)


# ------------------------------------------------------------
# 3. Identify year columns
# ------------------------------------------------------------

year_columns = [
    col for col in population_data.columns
    if str(col)[:4].isdigit()
]

print("\nYear Columns Found:")
print(year_columns)

print("\nNumber of Years:")
print(len(year_columns))


# ------------------------------------------------------------
# 4. Convert WIDE → LONG
# ------------------------------------------------------------

population_clean = population_data.melt(
    id_vars=[
        "series_name",
        "series_code",
        "country",
        "country_code"
    ],
    value_vars=year_columns,
    var_name="year",
    value_name="population_total"
)


# ------------------------------------------------------------
# 5. Extract year
# ------------------------------------------------------------

population_clean["year"] = (
    population_clean["year"]
    .astype(str)
    .str[:4]
)

population_clean["year"] = pd.to_numeric(
    population_clean["year"],
    errors="coerce"
)


# ------------------------------------------------------------
# 6. Clean country
# ------------------------------------------------------------

population_clean["country"] = (
    population_clean["country"]
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# 7. Clean country code
# ------------------------------------------------------------

population_clean["country_code"] = (
    population_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ------------------------------------------------------------
# 8. Convert population to numeric
# ------------------------------------------------------------

population_clean["population_total"] = pd.to_numeric(
    population_clean["population_total"],
    errors="coerce"
)


# ------------------------------------------------------------
# 9. Remove invalid rows
# ------------------------------------------------------------

population_clean = population_clean.dropna(
    subset=[
        "country",
        "year",
        "population_total"
    ]
)


# ------------------------------------------------------------
# 10. Convert year to integer
# ------------------------------------------------------------

population_clean["year"] = population_clean["year"].astype(int)


# ------------------------------------------------------------
# 11. Keep required columns only
# ------------------------------------------------------------

population_clean = population_clean[
    [
        "country",
        "country_code",
        "year",
        "population_total"
    ]
]


# ------------------------------------------------------------
# 12. Remove duplicates
# ------------------------------------------------------------

before = len(population_clean)

population_clean = population_clean.drop_duplicates(
    subset=[
        "country",
        "country_code",
        "year"
    ],
    keep="first"
)

after = len(population_clean)


# ------------------------------------------------------------
# 13. Sort
# ------------------------------------------------------------

population_clean = population_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)


# ------------------------------------------------------------
# 14. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✅ POPULATION CLEANING SUCCESSFUL")
print("=" * 60)

print("\nOriginal Shape:")
print(population_data.shape)

print("\nFinal Shape:")
print(population_clean.shape)

print("\nDuplicates Removed:")
print(before - after)

print("\nFinal Columns:")
print(population_clean.columns.tolist())

print("\nMissing Values:")
print(population_clean.isna().sum())

print("\nFirst 10 Rows:")
display(population_clean.head(10))


# In[55]:


# ============================================================
# STEP 11 — UN COMTRADE DATA INSPECTION
# ============================================================

import pandas as pd
import os

COMTRADE_FILE = "UN Comtrade.xlsx"

comtrade_path = os.path.join(folder, COMTRADE_FILE)

print("File path:")
print(comtrade_path)

print("\nFile exists:")
print(os.path.exists(comtrade_path))

comtrade_data = pd.read_excel(comtrade_path)

print("\n✅ UN COMTRADE DATA LOADED")

print("\nShape:")
print(comtrade_data.shape)

print("\nColumns:")
print(comtrade_data.columns.tolist())

print("\nFirst 10 Rows:")
display(comtrade_data.head(10))

print("\nData Types:")
print(comtrade_data.dtypes)


# In[57]:


# ============================================================
# STEP 11 — UN COMTRADE CLEANING
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. Start with loaded Comtrade data
# ------------------------------------------------------------

comtrade_clean = comtrade_data.copy()

# ------------------------------------------------------------
# 2. Rename columns
# ------------------------------------------------------------

comtrade_clean = comtrade_clean.rename(
    columns={
        "reporterCode": "reporter_code",
        "periods": "year",
        "reporterDesc": "country",
        "reporters": "country_code",
        "totalRecords": "total_trade_records",
        "tarifflineTotalRecords": "tariffline_total_records"
    }
)

# ------------------------------------------------------------
# 3. Clean country
# ------------------------------------------------------------

comtrade_clean["country"] = (
    comtrade_clean["country"]
    .astype(str)
    .str.strip()
)

# ------------------------------------------------------------
# 4. Clean country code
# ------------------------------------------------------------

comtrade_clean["country_code"] = (
    comtrade_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 5. Clean year
# ------------------------------------------------------------

comtrade_clean["year"] = pd.to_numeric(
    comtrade_clean["year"],
    errors="coerce"
)

# ------------------------------------------------------------
# 6. Convert record columns to numeric
# ------------------------------------------------------------

comtrade_clean["total_trade_records"] = pd.to_numeric(
    comtrade_clean["total_trade_records"],
    errors="coerce"
)

comtrade_clean["tariffline_total_records"] = pd.to_numeric(
    comtrade_clean["tariffline_total_records"],
    errors="coerce"
)

# ------------------------------------------------------------
# 7. Remove invalid rows
# ------------------------------------------------------------

comtrade_clean = comtrade_clean.dropna(
    subset=[
        "country",
        "year"
    ]
)

# ------------------------------------------------------------
# 8. Convert year to integer
# ------------------------------------------------------------

comtrade_clean["year"] = comtrade_clean["year"].astype(int)

# ------------------------------------------------------------
# 9. Keep only required columns
# ------------------------------------------------------------

comtrade_clean = comtrade_clean[
    [
        "country",
        "country_code",
        "year",
        "total_trade_records",
        "tariffline_total_records"
    ]
]

# ------------------------------------------------------------
# 10. Aggregate to ONE row per country-year
# ------------------------------------------------------------

comtrade_clean = (
    comtrade_clean
    .groupby(
        [
            "country",
            "country_code",
            "year"
        ],
        as_index=False
    )
    .agg(
        total_trade_records=(
            "total_trade_records",
            "max"
        ),
        tariffline_total_records=(
            "tariffline_total_records",
            "max"
        )
    )
)

# ------------------------------------------------------------
# 11. Sort
# ------------------------------------------------------------

comtrade_clean = comtrade_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)

# ------------------------------------------------------------
# 12. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✅ UN COMTRADE CLEANING SUCCESSFUL")
print("=" * 60)

print("\nFinal Shape:")
print(comtrade_clean.shape)

print("\nFinal Columns:")
print(comtrade_clean.columns.tolist())

print("\nMissing Values:")
print(comtrade_clean.isna().sum())

print("\nDuplicate Country-Year Keys:")
print(
    comtrade_clean.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    ).sum()
)

print("\nFirst 10 Rows:")
display(comtrade_clean.head(10))


# In[59]:


# ============================================================
# STEP 12 — WORLD BANK LPI DATA INSPECTION
# ============================================================

import pandas as pd
import os

LPI_FILE = "World Bank LPI.xlsx"

lpi_path = os.path.join(folder, LPI_FILE)

print("File path:")
print(lpi_path)

print("\nFile exists:")
print(os.path.exists(lpi_path))

lpi_data = pd.read_excel(lpi_path)

print("\n✅ WORLD BANK LPI DATA LOADED")

print("\nShape:")
print(lpi_data.shape)

print("\nColumns:")
print(lpi_data.columns.tolist())

print("\nFirst 10 Rows:")
display(lpi_data.head(10))

print("\nData Types:")
print(lpi_data.dtypes)


# In[61]:


# ============================================================
# STEP 12 — WORLD BANK LPI CLEANING
# WIDE FORMAT → LONG FORMAT
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. Start with loaded LPI data
# ------------------------------------------------------------

lpi_clean = lpi_data.copy()

print("Original Shape:")
print(lpi_clean.shape)

# ------------------------------------------------------------
# 2. Rename first 4 columns safely
# ------------------------------------------------------------

lpi_clean = lpi_clean.rename(
    columns={
        "Country Name": "country",
        "Country Code": "country_code",
        "Indicator Name": "indicator_name",
        "Indicator Code": "indicator_code"
    }
)

# ------------------------------------------------------------
# 3. Identify year columns
# ------------------------------------------------------------

year_columns = [
    col for col in lpi_clean.columns
    if str(col).isdigit()
]

print("\nYear Columns Found:")
print(year_columns)

print("\nNumber of Years:")
print(len(year_columns))

# ------------------------------------------------------------
# 4. Convert WIDE → LONG
# ------------------------------------------------------------

lpi_clean = lpi_clean.melt(
    id_vars=[
        "country",
        "country_code",
        "indicator_name",
        "indicator_code"
    ],
    value_vars=year_columns,
    var_name="year",
    value_name="lpi_score"
)

# ------------------------------------------------------------
# 5. Clean year
# ------------------------------------------------------------

lpi_clean["year"] = pd.to_numeric(
    lpi_clean["year"],
    errors="coerce"
)

# ------------------------------------------------------------
# 6. Clean country
# ------------------------------------------------------------

lpi_clean["country"] = (
    lpi_clean["country"]
    .astype(str)
    .str.strip()
)

# ------------------------------------------------------------
# 7. Clean country code
# ------------------------------------------------------------

lpi_clean["country_code"] = (
    lpi_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 8. Convert LPI score to numeric
# ------------------------------------------------------------

lpi_clean["lpi_score"] = pd.to_numeric(
    lpi_clean["lpi_score"],
    errors="coerce"
)

# ------------------------------------------------------------
# 9. Remove invalid rows
# ------------------------------------------------------------

lpi_clean = lpi_clean.dropna(
    subset=[
        "country",
        "year",
        "lpi_score"
    ]
)

# ------------------------------------------------------------
# 10. Convert year to integer
# ------------------------------------------------------------

lpi_clean["year"] = lpi_clean["year"].astype(int)

# ------------------------------------------------------------
# 11. Keep required columns
# ------------------------------------------------------------

lpi_clean = lpi_clean[
    [
        "country",
        "country_code",
        "year",
        "lpi_score"
    ]
]

# ------------------------------------------------------------
# 12. Remove duplicates
# ------------------------------------------------------------

before = len(lpi_clean)

lpi_clean = lpi_clean.drop_duplicates(
    subset=[
        "country",
        "country_code",
        "year"
    ],
    keep="first"
)

after = len(lpi_clean)

# ------------------------------------------------------------
# 13. Sort
# ------------------------------------------------------------

lpi_clean = lpi_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)

# ------------------------------------------------------------
# 14. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✅ WORLD BANK LPI CLEANING SUCCESSFUL")
print("=" * 60)

print("\nFinal Shape:")
print(lpi_clean.shape)

print("\nDuplicates Removed:")
print(before - after)

print("\nFinal Columns:")
print(lpi_clean.columns.tolist())

print("\nMissing Values:")
print(lpi_clean.isna().sum())

print("\nDuplicate Country-Year Keys:")
print(
    lpi_clean.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    ).sum()
)

print("\nFirst 10 Rows:")
display(lpi_clean.head(10))


# In[63]:


# ============================================================
# STEP 13 — FINAL DATASET VALIDATION
# ============================================================

print("=" * 70)
print("🔍 FINAL VALIDATION OF ALL DATASETS")
print("=" * 70)


# ------------------------------------------------------------
# 1. Dataset list
# ------------------------------------------------------------

datasets = {
    "GDP": gdp_clean,
    "EXPORT": export_clean,
    "GDP GROWTH": growth_clean,
    "INFLATION": inflation_clean,
    "POPULATION": population_clean,
    "COMTRADE": comtrade_clean,
    "LPI": lpi_clean
}


# ------------------------------------------------------------
# 2. Check each dataset
# ------------------------------------------------------------

for name, df in datasets.items():

    print("\n" + "-" * 70)
    print(name)

    print("Shape:", df.shape)

    print("Columns:")
    print(df.columns.tolist())

    print("Duplicate Country-Year Keys:")

    duplicates = df.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    ).sum()

    print(duplicates)

    print("Missing Values:")
    print(df.isna().sum())


# ------------------------------------------------------------
# 3. Check year ranges
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("📅 YEAR RANGE CHECK")
print("=" * 70)

for name, df in datasets.items():

    print(
        f"{name}: "
        f"{df['year'].min()} → {df['year'].max()}"
    )


# ------------------------------------------------------------
# 4. Check country counts
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("🌍 UNIQUE COUNTRY CHECK")
print("=" * 70)

for name, df in datasets.items():

    print(
        f"{name}: "
        f"{df['country'].nunique()} unique countries"
    )


# ------------------------------------------------------------
# 5. Check country-code consistency
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("🔑 COUNTRY CODE CHECK")
print("=" * 70)

for name, df in datasets.items():

    print(
        f"{name}: "
        f"{df['country_code'].nunique()} unique country codes"
    )


# ------------------------------------------------------------
# 6. Check required key columns
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("🔎 KEY COLUMN VALIDATION")
print("=" * 70)

required_columns = [
    "country",
    "country_code",
    "year"
]

for name, df in datasets.items():

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if len(missing_columns) == 0:
        print(f"✅ {name}: Key columns OK")
    else:
        print(
            f"❌ {name}: Missing columns → "
            f"{missing_columns}"
        )


# ------------------------------------------------------------
# 7. Final status
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✅ STEP 13 VALIDATION COMPLETED")
print("=" * 70)


# In[65]:


# ============================================================
# STEP 13A — GDP DUPLICATE INVESTIGATION
# ============================================================

print("=" * 70)
print("🔍 GDP DUPLICATE INVESTIGATION")
print("=" * 70)

# Duplicate rows based on country + country_code + year
gdp_duplicates = gdp_clean[
    gdp_clean.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ],
        keep=False
    )
].sort_values(
    [
        "country",
        "year"
    ]
)

print("\nTotal duplicate rows:")
print(len(gdp_duplicates))

print("\nNumber of duplicate country-year groups:")
print(
    gdp_duplicates[
        [
            "country",
            "country_code",
            "year"
        ]
    ]
    .drop_duplicates()
    .shape[0]
)

print("\nFirst 30 duplicate rows:")
display(gdp_duplicates.head(30))


# In[67]:


# ============================================================
# STEP 13B — CHECK GDP INDICATORS
# ============================================================

print("=" * 70)
print("🔍 CHECKING GDP SOURCE INDICATORS")
print("=" * 70)

print("\nGDP Source Shape:")
print(gdp_data.shape)

print("\nGDP Source Columns:")
print(gdp_data.columns.tolist())

print("\nUnique Series Names:")
display(
    gdp_data["Series Name"]
    .drop_duplicates()
    .to_frame()
)

print("\nUnique Series Codes:")
display(
    gdp_data["Series Code"]
    .drop_duplicates()
    .to_frame()
)


# In[69]:


# ============================================================
# STEP 13B — FINAL GDP CLEANING
# ONLY GDP (CURRENT US$)
# ============================================================

import pandas as pd

print("=" * 70)
print("🔧 REBUILDING GDP CLEAN DATASET")
print("=" * 70)

# ------------------------------------------------------------
# 1. Reload original GDP data
# ------------------------------------------------------------

gdp_data = pd.read_excel(
    os.path.join(
        folder,
        "GDP (Current US$).xlsx"
    )
)

print("\nOriginal Shape:")
print(gdp_data.shape)

# ------------------------------------------------------------
# 2. Keep ONLY GDP (current US$)
# ------------------------------------------------------------

gdp_data = gdp_data[
    gdp_data["Series Code"] == "NY.GDP.MKTP.CD"
].copy()

print("\nAfter selecting GDP (current US$):")
print(gdp_data.shape)

# ------------------------------------------------------------
# 3. Rename columns
# ------------------------------------------------------------

gdp_data = gdp_data.rename(
    columns={
        "Country Name": "country",
        "Country Code": "country_code"
    }
)

# ------------------------------------------------------------
# 4. Identify year columns
# ------------------------------------------------------------

year_columns = [
    col for col in gdp_data.columns
    if str(col)[:4].isdigit()
]

print("\nYear Columns:")
print(year_columns)

# ------------------------------------------------------------
# 5. WIDE → LONG
# ------------------------------------------------------------

gdp_clean = gdp_data.melt(
    id_vars=[
        "Series Name",
        "Series Code",
        "country",
        "country_code"
    ],
    value_vars=year_columns,
    var_name="year",
    value_name="gdp_usd"
)

# ------------------------------------------------------------
# 6. Extract year
# ------------------------------------------------------------

gdp_clean["year"] = (
    gdp_clean["year"]
    .astype(str)
    .str[:4]
)

gdp_clean["year"] = pd.to_numeric(
    gdp_clean["year"],
    errors="coerce"
)

# ------------------------------------------------------------
# 7. Clean country
# ------------------------------------------------------------

gdp_clean["country"] = (
    gdp_clean["country"]
    .astype(str)
    .str.strip()
)

# ------------------------------------------------------------
# 8. Clean country code
# ------------------------------------------------------------

gdp_clean["country_code"] = (
    gdp_clean["country_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 9. Convert GDP to numeric
# ------------------------------------------------------------

gdp_clean["gdp_usd"] = pd.to_numeric(
    gdp_clean["gdp_usd"],
    errors="coerce"
)

# ------------------------------------------------------------
# 10. Remove invalid rows
# ------------------------------------------------------------

gdp_clean = gdp_clean.dropna(
    subset=[
        "country",
        "country_code",
        "year"
    ]
)

# ------------------------------------------------------------
# 11. Convert year to integer
# ------------------------------------------------------------

gdp_clean["year"] = gdp_clean["year"].astype(int)

# ------------------------------------------------------------
# 12. Keep only required columns
# ------------------------------------------------------------

gdp_clean = gdp_clean[
    [
        "country",
        "country_code",
        "year",
        "gdp_usd"
    ]
]

# ------------------------------------------------------------
# 13. Remove duplicate keys
# ------------------------------------------------------------

gdp_clean = gdp_clean.drop_duplicates(
    subset=[
        "country",
        "country_code",
        "year"
    ],
    keep="first"
)

# ------------------------------------------------------------
# 14. Sort
# ------------------------------------------------------------

gdp_clean = gdp_clean.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)

# ------------------------------------------------------------
# 15. FINAL GDP CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✅ GDP CLEANING SUCCESSFUL")
print("=" * 70)

print("\nFinal Shape:")
print(gdp_clean.shape)

print("\nFinal Columns:")
print(gdp_clean.columns.tolist())

print("\nDuplicate Country-Year Keys:")
print(
    gdp_clean.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    ).sum()
)

print("\nMissing Values:")
print(gdp_clean.isna().sum())

print("\nFirst 10 Rows:")
display(gdp_clean.head(10))


# In[71]:


# ============================================================
# STEP 13C — FINAL VALIDATION AFTER GDP FIX
# ============================================================

datasets = {
    "GDP": gdp_clean,
    "EXPORT": export_clean,
    "GDP GROWTH": growth_clean,
    "INFLATION": inflation_clean,
    "POPULATION": population_clean,
    "COMTRADE": comtrade_clean,
    "LPI": lpi_clean
}

print("=" * 70)
print("🔍 FINAL VALIDATION — ALL 7 DATASETS")
print("=" * 70)

for name, df in datasets.items():

    print("\n" + "-" * 70)
    print(f"📊 {name}")

    print("Shape:", df.shape)

    duplicates = df.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    ).sum()

    print("Duplicate Country-Year Keys:", duplicates)

    print("\nMissing Values:")
    print(df.isna().sum())

    print(
        "\nYear Range:",
        df["year"].min(),
        "→",
        df["year"].max()
    )

    print(
        "Unique Countries:",
        df["country"].nunique()
    )

print("\n" + "=" * 70)
print("✅ FINAL VALIDATION COMPLETED")
print("=" * 70)


# In[73]:


# ============================================================
# STEP 14 — MASTER DATASET MERGE
# ============================================================

print("=" * 70)
print("🚀 CREATING MASTER SUPPLY CHAIN DATASET")
print("=" * 70)

# ------------------------------------------------------------
# 1. Create GDP-based master
# ------------------------------------------------------------

master = gdp_clean[
    [
        "country",
        "country_code",
        "year",
        "gdp_usd"
    ]
].copy()

print("\nStarting Master Shape:")
print(master.shape)


# ------------------------------------------------------------
# 2. Merge EXPORT
# ------------------------------------------------------------

master = master.merge(
    export_clean[
        [
            "country",
            "country_code",
            "year",
            "exports_pct_gdp"
        ]
    ],
    on=[
        "country",
        "country_code",
        "year"
    ],
    how="left"
)

print("After EXPORT merge:", master.shape)


# ------------------------------------------------------------
# 3. Merge GDP GROWTH
# ------------------------------------------------------------

master = master.merge(
    growth_clean[
        [
            "country",
            "country_code",
            "year",
            "gdp_growth_pct"
        ]
    ],
    on=[
        "country",
        "country_code",
        "year"
    ],
    how="left"
)

print("After GDP GROWTH merge:", master.shape)


# ------------------------------------------------------------
# 4. Merge INFLATION
# ------------------------------------------------------------

master = master.merge(
    inflation_clean[
        [
            "country",
            "country_code",
            "year",
            "inflation_pct"
        ]
    ],
    on=[
        "country",
        "country_code",
        "year"
    ],
    how="left"
)

print("After INFLATION merge:", master.shape)


# ------------------------------------------------------------
# 5. Merge POPULATION
# ------------------------------------------------------------

master = master.merge(
    population_clean[
        [
            "country",
            "country_code",
            "year",
            "population_total"
        ]
    ],
    on=[
        "country",
        "country_code",
        "year"
    ],
    how="left"
)

print("After POPULATION merge:", master.shape)


# ------------------------------------------------------------
# 6. Merge COMTRADE
# IMPORTANT:
# Comtrade country_code is not compatible with World Bank codes.
# Therefore merge using country + year only.
# ------------------------------------------------------------

master = master.merge(
    comtrade_clean[
        [
            "country",
            "year",
            "total_trade_records",
            "tariffline_total_records"
        ]
    ],
    on=[
        "country",
        "year"
    ],
    how="left"
)

print("After COMTRADE merge:", master.shape)


# ------------------------------------------------------------
# 7. Merge LPI
# ------------------------------------------------------------

master = master.merge(
    lpi_clean[
        [
            "country",
            "country_code",
            "year",
            "lpi_score"
        ]
    ],
    on=[
        "country",
        "country_code",
        "year"
    ],
    how="left"
)

print("After LPI merge:", master.shape)


# ------------------------------------------------------------
# 8. Sort master
# ------------------------------------------------------------

master = master.sort_values(
    [
        "country",
        "year"
    ]
).reset_index(drop=True)


# ------------------------------------------------------------
# 9. FINAL MASTER CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✅ MASTER DATASET CREATED")
print("=" * 70)

print("\nFinal Shape:")
print(master.shape)

print("\nFinal Columns:")
print(master.columns.tolist())

print("\nDuplicate Country-Year Keys:")

print(
    master.duplicated(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    ).sum()
)

print("\nMissing Values:")
print(master.isna().sum())

print("\nFirst 10 Rows:")
display(master.head(10))

print("\nLast 10 Rows:")
display(master.tail(10))


# In[75]:


# ============================================================
# STEP 14A — REBUILD EXPORT, GROWTH, INFLATION, POPULATION
# ============================================================

import pandas as pd
import os

print("=" * 70)
print("🔧 REBUILDING 4 WORLD BANK DATASETS")
print("=" * 70)


# ============================================================
# FUNCTION — WORLD BANK WIDE TO LONG
# ============================================================

def clean_world_bank_file(
    filename,
    value_column,
    indicator_code=None
):

    path = os.path.join(folder, filename)

    print("\n" + "-" * 70)
    print("Loading:", filename)

    df = pd.read_excel(path)

    print("Original Shape:", df.shape)

    # --------------------------------------------------------
    # Rename first 4 columns safely
    # --------------------------------------------------------

    df = df.rename(
        columns={
            df.columns[0]: "series_name",
            df.columns[1]: "series_code",
            df.columns[2]: "country",
            df.columns[3]: "country_code"
        }
    )

    # --------------------------------------------------------
    # Select required indicator if specified
    # --------------------------------------------------------

    if indicator_code is not None:

        df = df[
            df["series_code"].astype(str).str.strip()
            == indicator_code
        ].copy()

        print(
            "After Indicator Filter:",
            df.shape
        )

    # --------------------------------------------------------
    # Find year columns
    # --------------------------------------------------------

    year_columns = [
        col for col in df.columns
        if str(col)[:4].isdigit()
    ]

    print("Years Found:", len(year_columns))

    # --------------------------------------------------------
    # Wide → Long
    # --------------------------------------------------------

    clean = df.melt(
        id_vars=[
            "series_name",
            "series_code",
            "country",
            "country_code"
        ],
        value_vars=year_columns,
        var_name="year",
        value_name=value_column
    )

    # --------------------------------------------------------
    # Clean year
    # --------------------------------------------------------

    clean["year"] = (
        clean["year"]
        .astype(str)
        .str[:4]
    )

    clean["year"] = pd.to_numeric(
        clean["year"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Clean country
    # --------------------------------------------------------

    clean["country"] = (
        clean["country"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Clean country code
    # --------------------------------------------------------

    clean["country_code"] = (
        clean["country_code"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # --------------------------------------------------------
    # Numeric value
    # --------------------------------------------------------

    clean[value_column] = pd.to_numeric(
        clean[value_column],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Remove invalid keys
    # --------------------------------------------------------

    clean = clean.dropna(
        subset=[
            "country",
            "country_code",
            "year"
        ]
    )

    clean["year"] = clean["year"].astype(int)

    # --------------------------------------------------------
    # Keep required columns
    # --------------------------------------------------------

    clean = clean[
        [
            "country",
            "country_code",
            "year",
            value_column
        ]
    ]

    # --------------------------------------------------------
    # Remove duplicate keys
    # --------------------------------------------------------

    clean = clean.drop_duplicates(
        subset=[
            "country",
            "country_code",
            "year"
        ],
        keep="first"
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    clean = clean.sort_values(
        [
            "country",
            "year"
        ]
    ).reset_index(drop=True)

    print("Final Shape:", clean.shape)

    print(
        "Duplicate Keys:",
        clean.duplicated(
            subset=[
                "country",
                "country_code",
                "year"
            ]
        ).sum()
    )

    return clean


# ============================================================
# 1. EXPORT
# ============================================================

export_clean = clean_world_bank_file(
    "Export of goods and services (% of GDP).xlsx",
    "exports_pct_gdp",
    "NE.EXP.GNFS.ZS"
)


# ============================================================
# 2. GDP GROWTH
# ============================================================

growth_clean = clean_world_bank_file(
    "GDP Growth (annual %).xlsx",
    "gdp_growth_pct",
    "NY.GDP.MKTP.KD.ZG"
)


# ============================================================
# 3. INFLATION
# ============================================================

inflation_clean = clean_world_bank_file(
    "Inflation, consumer prices (annual %).xlsx",
    "inflation_pct",
    "FP.CPI.TOTL.ZG"
)


# ============================================================
# 4. POPULATION
# ============================================================

population_clean = clean_world_bank_file(
    "Population, Total.xlsx",
    "population_total",
    "SP.POP.TOTL"
)


# ============================================================
# FINAL CHECK
# ============================================================

print("\n" + "=" * 70)
print("✅ 4 DATASETS REBUILT SUCCESSFULLY")
print("=" * 70)

print("\nEXPORT:")
display(export_clean.head(5))

print("\nGDP GROWTH:")
display(growth_clean.head(5))

print("\nINFLATION:")
display(inflation_clean.head(5))

print("\nPOPULATION:")
display(population_clean.head(5))


# In[77]:


print("===== EXPORT CHECK =====")
print(export_clean.head(20))

print("\n===== EXPORT MISSING =====")
print(export_clean["exports_pct_gdp"].isna().sum())

print("\n===== EXPORT NON-MISSING SAMPLE =====")
print(
    export_clean[
        export_clean["exports_pct_gdp"].notna()
    ].head(10)
)

print("\n===== INFLATION NON-MISSING SAMPLE =====")
print(
    inflation_clean[
        inflation_clean["inflation_pct"].notna()
    ].head(10)
)


# In[79]:


# ============================================================
# STEP 14 — FINAL MASTER DATASET MERGE
# ============================================================

import pandas as pd

print("=" * 70)
print("BUILDING FINAL MASTER DATASET")
print("=" * 70)

# ------------------------------------------------------------
# 1. START WITH GDP
# ------------------------------------------------------------

master = gdp_clean[
    ["country", "country_code", "year", "gdp_usd"]
].copy()

print("\nStarting Master Shape:", master.shape)


# ------------------------------------------------------------
# 2. MERGE EXPORT
# ------------------------------------------------------------

master = master.merge(
    export_clean[
        ["country", "country_code", "year", "exports_pct_gdp"]
    ],
    on=["country", "country_code", "year"],
    how="left",
    validate="one_to_one"
)

print("After Export:", master.shape)


# ------------------------------------------------------------
# 3. MERGE GDP GROWTH
# ------------------------------------------------------------

master = master.merge(
    growth_clean[
        ["country", "country_code", "year", "gdp_growth_pct"]
    ],
    on=["country", "country_code", "year"],
    how="left",
    validate="one_to_one"
)

print("After GDP Growth:", master.shape)


# ------------------------------------------------------------
# 4. MERGE INFLATION
# ------------------------------------------------------------

master = master.merge(
    inflation_clean[
        ["country", "country_code", "year", "inflation_pct"]
    ],
    on=["country", "country_code", "year"],
    how="left",
    validate="one_to_one"
)

print("After Inflation:", master.shape)


# ------------------------------------------------------------
# 5. MERGE POPULATION
# ------------------------------------------------------------

master = master.merge(
    population_clean[
        ["country", "country_code", "year", "population_total"]
    ],
    on=["country", "country_code", "year"],
    how="left",
    validate="one_to_one"
)

print("After Population:", master.shape)


# ------------------------------------------------------------
# 6. MERGE UN COMTRADE
# ------------------------------------------------------------
# Comtrade country codes are different,
# so merge using country + year only.

master = master.merge(
    comtrade_clean[
        [
            "country",
            "year",
            "total_trade_records",
            "tariffline_total_records"
        ]
    ],
    on=["country", "year"],
    how="left"
)

print("After Comtrade:", master.shape)


# ------------------------------------------------------------
# 7. MERGE LPI
# ------------------------------------------------------------

master = master.merge(
    lpi_clean[
        ["country", "country_code", "year", "lpi_score"]
    ],
    on=["country", "country_code", "year"],
    how="left",
    validate="one_to_one"
)

print("After LPI:", master.shape)


# ------------------------------------------------------------
# 8. SORT
# ------------------------------------------------------------

master = master.sort_values(
    ["country", "year"]
).reset_index(drop=True)


# ------------------------------------------------------------
# 9. FINAL SHAPE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL MASTER SHAPE")
print("=" * 70)

print(master.shape)


# ------------------------------------------------------------
# 10. COLUMNS
# ------------------------------------------------------------

print("\nFINAL COLUMNS:")
print(master.columns.tolist())


# ------------------------------------------------------------
# 11. DUPLICATE CHECK
# ------------------------------------------------------------

duplicates = master.duplicated(
    subset=["country", "country_code", "year"]
).sum()

print("\nDuplicate Country-Year Keys:", duplicates)


# ------------------------------------------------------------
# 12. MISSING VALUES
# ------------------------------------------------------------

print("\nMISSING VALUES:")
print(master.isna().sum())


# ------------------------------------------------------------
# 13. SAMPLE DATA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SAMPLE DATA")
print("=" * 70)

print(master.head(20).to_string(index=False))


# ------------------------------------------------------------
# 14. CHECK AFGHANISTAN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AFGHANISTAN CHECK")
print("=" * 70)

print(
    master[
        master["country"] == "Afghanistan"
    ].head(10).to_string(index=False)
)


print("\n" + "=" * 70)
print("✅ MASTER DATASET CREATED SUCCESSFULLY")
print("=" * 70)


# In[81]:


# ============================================================
# STEP 15 — FINAL MASTER QUALITY CHECK
# ============================================================

print("=" * 70)
print("FINAL MASTER DATA QUALITY CHECK")
print("=" * 70)

# ------------------------------------------------------------
# 1. SHAPE
# ------------------------------------------------------------

print("\n1️⃣ DATASET SHAPE")
print(master.shape)


# ------------------------------------------------------------
# 2. COLUMNS
# ------------------------------------------------------------

print("\n2️⃣ COLUMNS")
for i, col in enumerate(master.columns, start=1):
    print(i, "->", col)


# ------------------------------------------------------------
# 3. DUPLICATE CHECK
# ------------------------------------------------------------

duplicate_keys = master.duplicated(
    subset=["country", "country_code", "year"]
).sum()

print("\n3️⃣ DUPLICATE KEYS")
print("Duplicate Country-Year Keys:", duplicate_keys)


# ------------------------------------------------------------
# 4. COUNTRY COUNT
# ------------------------------------------------------------

print("\n4️⃣ COUNTRIES")
print("Unique Countries:", master["country"].nunique())
print("Unique Country Codes:", master["country_code"].nunique())


# ------------------------------------------------------------
# 5. YEAR RANGE
# ------------------------------------------------------------

print("\n5️⃣ YEAR RANGE")
print("Minimum Year:", master["year"].min())
print("Maximum Year:", master["year"].max())


# ------------------------------------------------------------
# 6. MISSING VALUES
# ------------------------------------------------------------

print("\n6️⃣ MISSING VALUES")

missing_summary = pd.DataFrame({
    "missing_count": master.isna().sum(),
    "missing_percentage": (
        master.isna().mean() * 100
    ).round(2)
})

print(missing_summary)


# ------------------------------------------------------------
# 7. NUMERIC DATA CHECK
# ------------------------------------------------------------

print("\n7️⃣ NUMERIC COLUMNS")

numeric_columns = [
    "gdp_usd",
    "exports_pct_gdp",
    "gdp_growth_pct",
    "inflation_pct",
    "population_total",
    "total_trade_records",
    "tariffline_total_records",
    "lpi_score"
]

print(master[numeric_columns].dtypes)


# ------------------------------------------------------------
# 8. BASIC STATISTICS
# ------------------------------------------------------------

print("\n8️⃣ BASIC STATISTICS")

print(
    master[numeric_columns].describe().T
)


# ------------------------------------------------------------
# 9. CHECK FOR IMPOSSIBLE POPULATION VALUES
# ------------------------------------------------------------

print("\n9️⃣ POPULATION CHECK")

print(
    "Population <= 0:",
    (master["population_total"] <= 0).sum()
)


# ------------------------------------------------------------
# 10. CHECK GDP
# ------------------------------------------------------------

print("\n🔟 GDP CHECK")

print(
    "GDP <= 0:",
    (master["gdp_usd"] <= 0).sum()
)


# ------------------------------------------------------------
# 11. CHECK EXPORT PERCENTAGE
# ------------------------------------------------------------

print("\n1️⃣1️⃣ EXPORT % CHECK")

print(
    "Export values < 0:",
    (master["exports_pct_gdp"] < 0).sum()
)

print(
    "Export values > 100:",
    (master["exports_pct_gdp"] > 100).sum()
)


# ------------------------------------------------------------
# 12. CHECK LPI
# ------------------------------------------------------------

print("\n1️⃣2️⃣ LPI CHECK")

print(
    "LPI non-missing:",
    master["lpi_score"].notna().sum()
)

print(
    "LPI missing:",
    master["lpi_score"].isna().sum()
)


# ------------------------------------------------------------
# 13. FINAL SAMPLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL SAMPLE")
print("=" * 70)

print(
    master.sample(
        min(10, len(master)),
        random_state=42
    ).to_string(index=False)
)


# ------------------------------------------------------------
# FINAL STATUS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✅ FINAL QUALITY CHECK COMPLETED")
print("=" * 70)


# In[83]:


# ============================================================
# STEP 16 — EXPORT FINAL MASTER DATASET
# ============================================================

import os

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

# ------------------------------------------------------------
# FINAL FILE PATHS
# ------------------------------------------------------------

csv_path = os.path.join(
    folder,
    "FINAL_SUPPLY_CHAIN_MASTER.csv"
)

excel_path = os.path.join(
    folder,
    "FINAL_SUPPLY_CHAIN_MASTER.xlsx"
)


# ------------------------------------------------------------
# EXPORT CSV
# ------------------------------------------------------------

master.to_csv(
    csv_path,
    index=False
)


# ------------------------------------------------------------
# EXPORT EXCEL
# ------------------------------------------------------------

master.to_excel(
    excel_path,
    index=False
)


# ------------------------------------------------------------
# VERIFY FILES
# ------------------------------------------------------------

print("=" * 70)
print("FINAL MASTER DATASET EXPORTED")
print("=" * 70)

print("\nCSV:")
print(csv_path)

print("\nExcel:")
print(excel_path)

print("\nCSV Exists:", os.path.exists(csv_path))
print("Excel Exists:", os.path.exists(excel_path))

print("\nCSV Size:",
      round(os.path.getsize(csv_path) / (1024 * 1024), 2),
      "MB")

print("Excel Size:",
      round(os.path.getsize(excel_path) / (1024 * 1024), 2),
      "MB")


# ------------------------------------------------------------
# FINAL VERIFICATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL VERIFICATION")
print("=" * 70)

print("Rows:", len(master))
print("Columns:", len(master.columns))
print("Duplicate Keys:",
      master.duplicated(
          subset=["country", "country_code", "year"]
      ).sum())

print("\n✅ FINAL FILES READY FOR MYSQL + POWER BI")


# In[85]:


# ============================================================
# GLOBAL SUPPLY CHAIN DISRUPTION & LOGISTICS INTELLIGENCE
# Q1 - Q7 ADVANCED REAL-WORLD ANALYSIS
# ============================================================

import pandas as pd
import numpy as np
import os

print("=" * 80)
print("GLOBAL SUPPLY CHAIN INTELLIGENCE — Q1 TO Q7")
print("=" * 80)


# ============================================================
# STEP 1 — COPY MASTER
# ============================================================

df = master.copy()

print("\nMaster Dataset:", df.shape)


# ============================================================
# STEP 2 — HELPER FUNCTIONS
# ============================================================

def minmax(series):
    """
    Converts a variable into 0-100 scale.
    Higher value = higher intensity/risk.
    """
    s = series.copy()

    min_val = s.min()
    max_val = s.max()

    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return pd.Series(np.nan, index=s.index)

    return ((s - min_val) / (max_val - min_val)) * 100


def percentile_score(series):
    """
    Converts variable into percentile score 0-100.
    """
    return series.rank(pct=True) * 100


# ============================================================
# STEP 3 — PREPARE RISK VARIABLES
# ============================================================

# ------------------------------------------------------------
# Export dependence
# Higher exports/GDP = higher external exposure
# ------------------------------------------------------------

df["export_exposure_score"] = percentile_score(
    df["exports_pct_gdp"]
)


# ------------------------------------------------------------
# GDP size
# Larger GDP = stronger economic capacity
# ------------------------------------------------------------

df["economic_strength_score"] = percentile_score(
    np.log1p(df["gdp_usd"])
)


# ------------------------------------------------------------
# GDP growth instability
# Absolute growth = magnitude of economic movement
# ------------------------------------------------------------

df["growth_instability"] = abs(
    df["gdp_growth_pct"]
)

df["growth_instability_score"] = percentile_score(
    df["growth_instability"]
)


# ------------------------------------------------------------
# Inflation instability
# Absolute inflation captures price instability
# ------------------------------------------------------------

df["inflation_instability"] = abs(
    df["inflation_pct"]
)

df["inflation_instability_score"] = percentile_score(
    df["inflation_instability"]
)


# ------------------------------------------------------------
# Logistics weakness
#
# IMPORTANT:
# LPI values in our dataset behave like rankings.
# Lower rank = better logistics.
# Therefore:
# Higher rank = weaker logistics.
# ------------------------------------------------------------

df["logistics_weakness_score"] = percentile_score(
    df["lpi_score"]
)


# ------------------------------------------------------------
# Small economy score
# Lower GDP = higher small-economy exposure potential
# ------------------------------------------------------------

df["small_economy_score"] = 100 - percentile_score(
    np.log1p(df["gdp_usd"])
)


# ============================================================
# Q1
# STRUCTURAL SUPPLY-CHAIN FRAGILITY
# ============================================================

print("\n" + "=" * 80)
print("Q1 — STRUCTURAL SUPPLY-CHAIN FRAGILITY")
print("=" * 80)

df["Q1_fragility_score"] = (
    0.40 * df["export_exposure_score"] +
    0.30 * df["logistics_weakness_score"] +
    0.15 * df["growth_instability_score"] +
    0.15 * df["inflation_instability_score"]
)

q1 = (
    df.groupby(
        ["country", "country_code"],
        as_index=False
    )["Q1_fragility_score"]
    .mean()
    .sort_values(
        "Q1_fragility_score",
        ascending=False
    )
)

q1["Q1_rank"] = range(1, len(q1) + 1)

print("\nTOP 20 MOST STRUCTURALLY FRAGILE ECONOMIES:\n")
print(
    q1[
        [
            "Q1_rank",
            "country",
            "country_code",
            "Q1_fragility_score"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# Q2
# TRADE–LOGISTICS MISMATCH
# ============================================================

print("\n" + "=" * 80)
print("Q2 — TRADE–LOGISTICS MISMATCH")
print("=" * 80)

df["Q2_trade_logistics_gap"] = (
    df["export_exposure_score"] *
    df["logistics_weakness_score"] /
    100
)

q2 = (
    df.groupby(
        ["country", "country_code"],
        as_index=False
    )["Q2_trade_logistics_gap"]
    .mean()
    .sort_values(
        "Q2_trade_logistics_gap",
        ascending=False
    )
)

q2["Q2_rank"] = range(1, len(q2) + 1)

print("\nTOP 20 TRADE–LOGISTICS MISMATCH ECONOMIES:\n")

print(
    q2[
        [
            "Q2_rank",
            "country",
            "country_code",
            "Q2_trade_logistics_gap"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# Q3
# HIDDEN-RISK ECONOMIES
# ============================================================

print("\n" + "=" * 80)
print("Q3 — HIDDEN-RISK ECONOMIES")
print("=" * 80)

df["Q3_hidden_risk"] = (
    0.30 * df["economic_strength_score"] +
    0.30 * df["export_exposure_score"] +
    0.25 * df["logistics_weakness_score"] +
    0.15 * df["growth_instability_score"]
)

q3 = (
    df.groupby(
        ["country", "country_code"],
        as_index=False
    )["Q3_hidden_risk"]
    .mean()
    .sort_values(
        "Q3_hidden_risk",
        ascending=False
    )
)

q3["Q3_rank"] = range(1, len(q3) + 1)

print("\nTOP 20 HIDDEN-RISK ECONOMIES:\n")

print(
    q3[
        [
            "Q3_rank",
            "country",
            "country_code",
            "Q3_hidden_risk"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# Q4
# ECONOMIC SHOCK ABSORPTION RISK
# ============================================================

print("\n" + "=" * 80)
print("Q4 — ECONOMIC SHOCK ABSORPTION RISK")
print("=" * 80)

df["Q4_shock_absorption_risk"] = (
    0.40 * df["export_exposure_score"] +
    0.30 * df["growth_instability_score"] +
    0.20 * df["inflation_instability_score"] +
    0.10 * df["logistics_weakness_score"]
)

q4 = (
    df.groupby(
        ["country", "country_code"],
        as_index=False
    )["Q4_shock_absorption_risk"]
    .mean()
    .sort_values(
        "Q4_shock_absorption_risk",
        ascending=False
    )
)

q4["Q4_rank"] = range(1, len(q4) + 1)

print("\nTOP 20 HIGH SHOCK-ABSORPTION-RISK ECONOMIES:\n")

print(
    q4[
        [
            "Q4_rank",
            "country",
            "country_code",
            "Q4_shock_absorption_risk"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# Q5
# RESILIENCE LEADERS
# ============================================================

print("\n" + "=" * 80)
print("Q5 — RESILIENCE LEADERS")
print("=" * 80)

df["Q5_resilience_score"] = (
    0.45 * (100 - df["logistics_weakness_score"]) +
    0.30 * (100 - df["growth_instability_score"]) +
    0.25 * (100 - df["inflation_instability_score"])
)

q5 = (
    df.groupby(
        ["country", "country_code"],
        as_index=False
    )["Q5_resilience_score"]
    .mean()
    .sort_values(
        "Q5_resilience_score",
        ascending=False
    )
)

q5["Q5_rank"] = range(1, len(q5) + 1)

print("\nTOP 20 RESILIENCE LEADERS:\n")

print(
    q5[
        [
            "Q5_rank",
            "country",
            "country_code",
            "Q5_resilience_score"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# Q6
# SMALL ECONOMY, BIG EXPOSURE
# ============================================================

print("\n" + "=" * 80)
print("Q6 — SMALL ECONOMY, BIG EXPOSURE")
print("=" * 80)

df["Q6_small_economy_exposure"] = (
    0.35 * df["small_economy_score"] +
    0.35 * df["export_exposure_score"] +
    0.30 * df["logistics_weakness_score"]
)

q6 = (
    df.groupby(
        ["country", "country_code"],
        as_index=False
    )["Q6_small_economy_exposure"]
    .mean()
    .sort_values(
        "Q6_small_economy_exposure",
        ascending=False
    )
)

q6["Q6_rank"] = range(1, len(q6) + 1)

print("\nTOP 20 SMALL-ECONOMY EXPOSURE RISKS:\n")

print(
    q6[
        [
            "Q6_rank",
            "country",
            "country_code",
            "Q6_small_economy_exposure"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# Q7
# SUPPLY-CHAIN EARLY WARNING SYSTEM
# ============================================================

print("\n" + "=" * 80)
print("Q7 — SUPPLY-CHAIN EARLY WARNING SYSTEM")
print("=" * 80)

# ------------------------------------------------------------
# Year-to-year changes
# ------------------------------------------------------------

df = df.sort_values(
    ["country", "year"]
).reset_index(drop=True)

df["export_change"] = (
    df.groupby("country")["exports_pct_gdp"]
    .diff()
)

df["growth_change"] = (
    df.groupby("country")["gdp_growth_pct"]
    .diff()
)

df["inflation_change"] = (
    df.groupby("country")["inflation_pct"]
    .diff()
)

df["lpi_change"] = (
    df.groupby("country")["lpi_score"]
    .diff()
)


# ------------------------------------------------------------
# Convert deterioration signals to percentile scores
# ------------------------------------------------------------

df["export_rise_score"] = percentile_score(
    df["export_change"].clip(lower=0)
)

df["growth_stress_score"] = percentile_score(
    df["growth_change"].abs()
)

df["inflation_stress_score"] = percentile_score(
    df["inflation_change"].abs()
)

df["logistics_deterioration_score"] = percentile_score(
    df["lpi_change"].clip(lower=0)
)


# ------------------------------------------------------------
# Early Warning Score
# ------------------------------------------------------------

df["Q7_early_warning_score"] = (
    0.30 * df["export_rise_score"] +
    0.25 * df["growth_stress_score"] +
    0.20 * df["inflation_stress_score"] +
    0.25 * df["logistics_deterioration_score"]
)


q7 = (
    df[
        [
            "country",
            "country_code",
            "year",
            "Q7_early_warning_score",
            "export_change",
            "growth_change",
            "inflation_change",
            "lpi_change"
        ]
    ]
    .dropna(
        subset=["Q7_early_warning_score"]
    )
    .sort_values(
        "Q7_early_warning_score",
        ascending=False
    )
)

q7["Q7_rank"] = range(1, len(q7) + 1)

print("\nTOP 30 COUNTRY-YEAR EARLY WARNING SIGNALS:\n")

print(
    q7[
        [
            "Q7_rank",
            "country",
            "country_code",
            "year",
            "Q7_early_warning_score",
            "export_change",
            "growth_change",
            "inflation_change",
            "lpi_change"
        ]
    ].head(30).to_string(index=False)
)


# ============================================================
# STEP 4 — CREATE FINAL ANALYSIS TABLE
# ============================================================

analysis_summary = q1.merge(
    q2,
    on=["country", "country_code"],
    how="outer"
)

analysis_summary = analysis_summary.merge(
    q3,
    on=["country", "country_code"],
    how="outer"
)

analysis_summary = analysis_summary.merge(
    q4,
    on=["country", "country_code"],
    how="outer"
)

analysis_summary = analysis_summary.merge(
    q5,
    on=["country", "country_code"],
    how="outer"
)

analysis_summary = analysis_summary.merge(
    q6,
    on=["country", "country_code"],
    how="outer"
)


# ============================================================
# STEP 5 — EXPORT RESULTS
# ============================================================

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

q1.to_csv(
    os.path.join(folder, "Q1_STRUCTURAL_FRAGILITY.csv"),
    index=False
)

q2.to_csv(
    os.path.join(folder, "Q2_TRADE_LOGISTICS_GAP.csv"),
    index=False
)

q3.to_csv(
    os.path.join(folder, "Q3_HIDDEN_RISK.csv"),
    index=False
)

q4.to_csv(
    os.path.join(folder, "Q4_SHOCK_ABSORPTION.csv"),
    index=False
)

q5.to_csv(
    os.path.join(folder, "Q5_RESILIENCE_LEADERS.csv"),
    index=False
)

q6.to_csv(
    os.path.join(folder, "Q6_SMALL_ECONOMY_RISK.csv"),
    index=False
)

q7.to_csv(
    os.path.join(folder, "Q7_EARLY_WARNING.csv"),
    index=False
)

analysis_summary.to_csv(
    os.path.join(folder, "SUPPLY_CHAIN_Q1_Q6_SUMMARY.csv"),
    index=False
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 80)
print("✅ Q1–Q7 ADVANCED ANALYSIS COMPLETED")
print("=" * 80)

print("\nFiles created:")

print("1. Q1_STRUCTURAL_FRAGILITY.csv")
print("2. Q2_TRADE_LOGISTICS_GAP.csv")
print("3. Q3_HIDDEN_RISK.csv")
print("4. Q4_SHOCK_ABSORPTION.csv")
print("5. Q5_RESILIENCE_LEADERS.csv")
print("6. Q6_SMALL_ECONOMY_RISK.csv")
print("7. Q7_EARLY_WARNING.csv")
print("8. SUPPLY_CHAIN_Q1_Q6_SUMMARY.csv")

print("\n" + "=" * 80)
print("PROJECT ANALYTICS READY")
print("=" * 80)


# In[89]:


# ================================================================
# GLOBAL SUPPLY CHAIN DISRUPTION & LOGISTICS INTELLIGENCE
# FINAL Q1-Q7 ANALYSIS + DIFFERENT CHART TYPES
# ================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ------------------------------------------------
# 1. OUTPUT FOLDER
# ------------------------------------------------

folder = r"C:\Users\karan\Desktop\Global Supply Chain Disruption & Logistics Intelligence System"

chart_folder = os.path.join(folder, "Q1_Q7_CHARTS")
os.makedirs(chart_folder, exist_ok=True)

print("Chart folder:")
print(chart_folder)


# ------------------------------------------------
# 2. COPY MASTER DATA
# ------------------------------------------------

df = master.copy()

print("\nMaster shape:", df.shape)
print("Columns:")
print(df.columns.tolist())


# ------------------------------------------------
# 3. HELPER FUNCTIONS
# ------------------------------------------------

def percentile_score(series):
    """
    Converts a variable into 0-100 percentile score.
    Higher value = higher risk.
    """
    return series.rank(pct=True) * 100


def minmax(series):
    """
    Converts variable into 0-100 scale.
    """
    minimum = series.min()
    maximum = series.max()

    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series(50, index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


# ------------------------------------------------
# 4. RISK COMPONENTS
# ------------------------------------------------

df["export_exposure_score"] = percentile_score(
    df["exports_pct_gdp"]
)

df["economic_strength_score"] = percentile_score(
    np.log1p(df["gdp_usd"])
)

df["growth_instability"] = df["gdp_growth_pct"].abs()

df["growth_instability_score"] = percentile_score(
    df["growth_instability"]
)

df["inflation_instability"] = df["inflation_pct"].abs()

df["inflation_instability_score"] = percentile_score(
    df["inflation_instability"]
)

# LPI behaves like rank:
# higher rank = weaker logistics
df["logistics_weakness_score"] = percentile_score(
    df["lpi_score"]
)

df["logistics_strength_score"] = (
    100 - df["logistics_weakness_score"]
)

df["growth_stability_score"] = (
    100 - df["growth_instability_score"]
)

df["inflation_stability_score"] = (
    100 - df["inflation_instability_score"]
)

df["small_economy_score"] = (
    100 - df["economic_strength_score"]
)


# ================================================================
# Q1 — STRUCTURAL SUPPLY-CHAIN FRAGILITY
# ================================================================

df["Q1_Fragility_Score"] = (
    0.40 * df["export_exposure_score"] +
    0.30 * df["logistics_weakness_score"] +
    0.15 * df["growth_instability_score"] +
    0.15 * df["inflation_instability_score"]
)

q1 = (
    df.groupby(["country", "country_code"], as_index=False)
      ["Q1_Fragility_Score"]
      .mean()
      .dropna()
      .sort_values("Q1_Fragility_Score", ascending=False)
)

q1["Rank"] = range(1, len(q1) + 1)

q1.to_csv(
    os.path.join(folder, "Q1_STRUCTURAL_FRAGILITY.csv"),
    index=False
)

print("\n================ Q1 ================")
print(q1.head(20))


# Q1 COLUMN CHART

q1_chart = q1.head(10).sort_values("Q1_Fragility_Score")

plt.figure(figsize=(12, 7))

plt.bar(
    q1_chart["country"],
    q1_chart["Q1_Fragility_Score"]
)

plt.title(
    "Q1 - Top Economies by Structural Supply-Chain Fragility",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Country")
plt.ylabel("Fragility Score")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q1_COLUMN_CHART.png"),
    dpi=200
)

plt.show()


# ================================================================
# Q2 — TRADE–LOGISTICS MISMATCH
# ================================================================

df["Q2_Trade_Logistics_Gap"] = (
    df["export_exposure_score"] *
    df["logistics_weakness_score"] / 100
)

q2 = (
    df.groupby(["country", "country_code"], as_index=False)
      .agg(
          Trade_Exposure=("export_exposure_score", "mean"),
          Logistics_Weakness=("logistics_weakness_score", "mean"),
          Trade_Logistics_Gap=("Q2_Trade_Logistics_Gap", "mean")
      )
      .dropna()
      .sort_values("Trade_Logistics_Gap", ascending=False)
)

q2["Rank"] = range(1, len(q2) + 1)

q2.to_csv(
    os.path.join(folder, "Q2_TRADE_LOGISTICS_GAP.csv"),
    index=False
)

print("\n================ Q2 ================")
print(q2.head(20))


# Q2 SCATTER CHART

q2_chart = q2.head(60)

plt.figure(figsize=(11, 7))

plt.scatter(
    q2_chart["Trade_Exposure"],
    q2_chart["Logistics_Weakness"],
    s=70,
    alpha=0.7
)

plt.axvline(
    q2_chart["Trade_Exposure"].median(),
    linestyle="--"
)

plt.axhline(
    q2_chart["Logistics_Weakness"].median(),
    linestyle="--"
)

plt.title(
    "Q2 - Trade Dependency vs Logistics Weakness",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Trade Exposure Score")
plt.ylabel("Logistics Weakness Score")

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q2_SCATTER_CHART.png"),
    dpi=200
)

plt.show()


# ================================================================
# Q3 — HIDDEN RISK ECONOMIES
# ================================================================

df["Q3_Hidden_Risk"] = (
    0.30 * df["economic_strength_score"] +
    0.30 * df["export_exposure_score"] +
    0.25 * df["logistics_weakness_score"] +
    0.15 * df["growth_instability_score"]
)

q3 = (
    df.groupby(["country", "country_code"], as_index=False)
      ["Q3_Hidden_Risk"]
      .mean()
      .dropna()
      .sort_values("Q3_Hidden_Risk", ascending=False)
)

q3["Risk_Level"] = pd.cut(
    q3["Q3_Hidden_Risk"],
    bins=[-np.inf, 33, 66, np.inf],
    labels=["Low", "Medium", "High"]
)

q3["Rank"] = range(1, len(q3) + 1)

q3.to_csv(
    os.path.join(folder, "Q3_HIDDEN_RISK.csv"),
    index=False
)

print("\n================ Q3 ================")
print(q3.head(20))


# Q3 PIE CHART

q3_pie = (
    q3["Risk_Level"]
    .value_counts()
    .reindex(["Low", "Medium", "High"])
    .fillna(0)
)

plt.figure(figsize=(8, 8))

plt.pie(
    q3_pie.values,
    labels=q3_pie.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Q3 - Hidden Vulnerability Risk Composition",
    fontsize=15,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q3_PIE_CHART.png"),
    dpi=200
)

plt.show()


# ================================================================
# Q4 — ECONOMIC SHOCK ABSORPTION RISK
# ================================================================

df["Q4_Shock_Absorption_Risk"] = (
    0.40 * df["export_exposure_score"] +
    0.30 * df["growth_instability_score"] +
    0.20 * df["inflation_instability_score"] +
    0.10 * df["logistics_weakness_score"]
)

q4 = (
    df.groupby(["country", "country_code"], as_index=False)
      ["Q4_Shock_Absorption_Risk"]
      .mean()
      .dropna()
      .sort_values(
          "Q4_Shock_Absorption_Risk",
          ascending=False
      )
)

q4["Rank"] = range(1, len(q4) + 1)

q4.to_csv(
    os.path.join(folder, "Q4_SHOCK_ABSORPTION.csv"),
    index=False
)

print("\n================ Q4 ================")
print(q4.head(20))


# Q4 HORIZONTAL BAR

q4_chart = q4.head(12).sort_values(
    "Q4_Shock_Absorption_Risk"
)

plt.figure(figsize=(11, 7))

plt.barh(
    q4_chart["country"],
    q4_chart["Q4_Shock_Absorption_Risk"]
)

plt.title(
    "Q4 - Economies with Highest Economic Shock Absorption Risk",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Shock Absorption Risk Score")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q4_BAR_CHART.png"),
    dpi=200
)

plt.show()


# ================================================================
# Q5 — RESILIENCE LEADERS
# ================================================================

# High logistics strength + economic stability
# + inflation stability + meaningful trade exposure

df["Q5_Resilience_Leadership"] = (
    0.45 * df["logistics_strength_score"] +
    0.25 * df["growth_stability_score"] +
    0.20 * df["inflation_stability_score"] +
    0.10 * df["export_exposure_score"]
)

q5 = (
    df.groupby(["country", "country_code"], as_index=False)
      .agg(
          Resilience_Score=(
              "Q5_Resilience_Leadership",
              "mean"
          ),
          Trade_Exposure=(
              "export_exposure_score",
              "mean"
          ),
          Logistics_Strength=(
              "logistics_strength_score",
              "mean"
          )
      )
      .dropna()
      .sort_values(
          "Resilience_Score",
          ascending=False
      )
)

q5["Rank"] = range(1, len(q5) + 1)

q5.to_csv(
    os.path.join(folder, "Q5_RESILIENCE_LEADERS.csv"),
    index=False
)

print("\n================ Q5 ================")
print(q5.head(20))


# Q5 SCATTER CHART

q5_chart = q5.head(60)

plt.figure(figsize=(11, 7))

plt.scatter(
    q5_chart["Trade_Exposure"],
    q5_chart["Logistics_Strength"],
    s=80,
    alpha=0.7
)

plt.axvline(
    q5_chart["Trade_Exposure"].median(),
    linestyle="--"
)

plt.axhline(
    q5_chart["Logistics_Strength"].median(),
    linestyle="--"
)

plt.title(
    "Q5 - Trade Exposure vs Logistics Strength",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Trade Exposure Score")
plt.ylabel("Logistics Strength Score")

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q5_RESILIENCE_SCATTER.png"),
    dpi=200
)

plt.show()


# ================================================================
# Q6 — SMALL ECONOMY, BIG EXPOSURE
# ================================================================

df["Q6_Small_Economy_Risk"] = (
    0.35 * df["small_economy_score"] +
    0.35 * df["export_exposure_score"] +
    0.30 * df["logistics_weakness_score"]
)

q6 = (
    df.groupby(["country", "country_code"], as_index=False)
      ["Q6_Small_Economy_Risk"]
      .mean()
      .dropna()
      .sort_values(
          "Q6_Small_Economy_Risk",
          ascending=False
      )
)

q6["Rank"] = range(1, len(q6) + 1)

q6.to_csv(
    os.path.join(folder, "Q6_SMALL_ECONOMY_RISK.csv"),
    index=False
)

print("\n================ Q6 ================")
print(q6.head(20))


# Q6 COLUMN CHART

q6_chart = q6.head(10).sort_values(
    "Q6_Small_Economy_Risk"
)

plt.figure(figsize=(12, 7))

plt.bar(
    q6_chart["country"],
    q6_chart["Q6_Small_Economy_Risk"]
)

plt.title(
    "Q6 - Small Economy Supply-Chain Risk",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Country")
plt.ylabel("Small-Economy Risk Score")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q6_COLUMN_CHART.png"),
    dpi=200
)

plt.show()


# ================================================================
# Q7 — SUPPLY-CHAIN EARLY WARNING SYSTEM
# ================================================================

# Sort by country/year

early = df.sort_values(
    ["country", "year"]
).copy()

# Changes between consecutive observed years

early["export_change"] = (
    early.groupby("country")["exports_pct_gdp"]
    .diff()
)

early["growth_change"] = (
    early.groupby("country")["gdp_growth_pct"]
    .diff()
)

early["inflation_change"] = (
    early.groupby("country")["inflation_pct"]
    .diff()
)

# LPI changes ONLY when two observed LPI values exist
# This avoids treating missing LPI years as deterioration.

early["previous_lpi"] = (
    early.groupby("country")["lpi_score"]
    .shift()
)

early["previous_lpi_year"] = (
    early.groupby("country")["year"]
    .shift()
)

early["lpi_change"] = (
    early["lpi_score"] -
    early["previous_lpi"]
)

# Only calculate LPI deterioration where
# previous observed LPI actually exists.

early.loc[
    early["previous_lpi"].isna(),
    "lpi_change"
] = np.nan


# Early-warning components

early["EW_Trade"] = percentile_score(
    early["export_change"].abs()
)

early["EW_Growth"] = percentile_score(
    early["growth_change"].abs()
)

early["EW_Inflation"] = percentile_score(
    early["inflation_change"].abs()
)

early["EW_Logistics"] = percentile_score(
    early["lpi_change"].abs()
)

# Existing logistics weakness also matters

early["EW_Logistics_Weakness"] = (
    early["logistics_weakness_score"]
)


# Final Early Warning Score

early["Q7_Early_Warning_Score"] = (
    0.25 * early["EW_Trade"] +
    0.25 * early["EW_Growth"] +
    0.20 * early["EW_Inflation"] +
    0.15 * early["EW_Logistics"] +
    0.15 * early["EW_Logistics_Weakness"]
)

q7 = (
    early[
        [
            "country",
            "country_code",
            "year",
            "Q7_Early_Warning_Score",
            "export_change",
            "growth_change",
            "inflation_change",
            "lpi_change"
        ]
    ]
    .dropna(subset=["Q7_Early_Warning_Score"])
    .sort_values(
        "Q7_Early_Warning_Score",
        ascending=False
    )
)

q7["Alert_Level"] = pd.cut(
    q7["Q7_Early_Warning_Score"],
    bins=[-np.inf, 33, 66, np.inf],
    labels=["Low", "Medium", "High"]
)

q7["Rank"] = range(1, len(q7) + 1)

q7.to_csv(
    os.path.join(folder, "Q7_EARLY_WARNING.csv"),
    index=False
)

print("\n================ Q7 ================")
print(q7.head(20))


# Q7 LINE CHART
# Show yearly average early-warning score

q7_year = (
    q7.groupby("year", as_index=False)
      ["Q7_Early_Warning_Score"]
      .mean()
      .sort_values("year")
)

plt.figure(figsize=(12, 7))

plt.plot(
    q7_year["year"],
    q7_year["Q7_Early_Warning_Score"],
    marker="o",
    linewidth=2
)

plt.title(
    "Q7 - Global Supply-Chain Early Warning Trend",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Average Early Warning Score")

plt.grid(alpha=0.25)

plt.tight_layout()

plt.savefig(
    os.path.join(chart_folder, "Q7_LINE_CHART.png"),
    dpi=200
)

plt.show()


# ================================================================
# 5. MASTER SUMMARY TABLE
# ================================================================

summary = pd.DataFrame({
    "Question": [
        "Q1 Structural Fragility",
        "Q2 Trade-Logistics Gap",
        "Q3 Hidden Risk",
        "Q4 Shock Absorption Risk",
        "Q5 Resilience Leadership",
        "Q6 Small Economy Risk",
        "Q7 Early Warning"
    ],

    "Metric": [
        "Q1_Fragility_Score",
        "Trade_Logistics_Gap",
        "Q3_Hidden_Risk",
        "Q4_Shock_Absorption_Risk",
        "Resilience_Score",
        "Q6_Small_Economy_Risk",
        "Q7_Early_Warning_Score"
    ],

    "Chart_Type": [
        "Column Chart",
        "Scatter Chart",
        "Pie Chart",
        "Bar Chart",
        "Scatter Chart",
        "Column Chart",
        "Line Chart"
    ]
})

summary.to_csv(
    os.path.join(
        folder,
        "SUPPLY_CHAIN_Q1_Q7_SUMMARY.csv"
    ),
    index=False
)


# ================================================================
# 6. EXPORT ALL ANALYSIS TO ONE EXCEL FILE
# ================================================================

analysis_excel = os.path.join(
    folder,
    "SUPPLY_CHAIN_Q1_Q7_ANALYSIS.xlsx"
)

with pd.ExcelWriter(
    analysis_excel,
    engine="openpyxl"
) as writer:

    q1.to_excel(
        writer,
        sheet_name="Q1_Fragility",
        index=False
    )

    q2.to_excel(
        writer,
        sheet_name="Q2_Trade_Logistics",
        index=False
    )

    q3.to_excel(
        writer,
        sheet_name="Q3_Hidden_Risk",
        index=False
    )

    q4.to_excel(
        writer,
        sheet_name="Q4_Shock_Risk",
        index=False
    )

    q5.to_excel(
        writer,
        sheet_name="Q5_Resilience",
        index=False
    )

    q6.to_excel(
        writer,
        sheet_name="Q6_Small_Economy",
        index=False
    )

    q7.to_excel(
        writer,
        sheet_name="Q7_Early_Warning",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Dashboard_Summary",
        index=False
    )


# ================================================================
# 7. FINAL OUTPUT
# ================================================================

print("\n\n================================================")
print("FINAL Q1-Q7 ANALYSIS COMPLETED")
print("================================================")

print("\nAnalysis Excel:")
print(analysis_excel)

print("\nCharts created:")

for file in sorted(os.listdir(chart_folder)):
    print("✔", file)

print("\n================================================")
print("CHART TYPES")
print("================================================")

print("Q1 -> Column Chart")
print("Q2 -> Scatter Chart")
print("Q3 -> Pie Chart")
print("Q4 -> Bar Chart")
print("Q5 -> Scatter Chart")
print("Q6 -> Column Chart")
print("Q7 -> Line Chart")

print("\nDONE 🔥")


# In[ ]:




