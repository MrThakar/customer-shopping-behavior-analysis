"""
Customer Shopping Behavior - Data Cleaning, Preprocessing & SQL Ingestion
Tech Stack: Python (pandas, SQLAlchemy) -> PostgreSQL
"""

import os

import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# 1. LOAD DATA & INITIAL EXPLORATION
# ==========================================

df = pd.read_csv("customer_shopping_behavior.csv")
print(df.head())
print(df.info())
print(df.describe(include="all"))
print(df.isnull().sum())

# ==========================================
# 2. MISSING VALUE IMPUTATION
# ==========================================

# Impute missing review ratings with category-specific median
df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(
    lambda x: x.fillna(x.median())
)
print(df.isnull().sum())

# ==========================================
# 3. SCHEMA STANDARDIZATION
# ==========================================

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})
print(df.columns)

# ==========================================
# 4. FEATURE ENGINEERING
# ==========================================

# Create demographic cohort binning
labels = ["Young Adult", "Adult", "Middle-aged", "Senior"]
df["age_group"] = pd.qcut(df["age"], q=4, labels=labels)
print(df[["age", "age_group"]].head(10))

# Map purchase frequency strings to numerical day cycles
frequency_mapping = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90,
}
df["purchase_frequency_days"] = df["frequency_of_purchases"].map(frequency_mapping)
print(df[["purchase_frequency_days", "frequency_of_purchases"]].head(10))

# ==========================================
# 5. REDUNDANCY CHECK & COLUMN PRUNING
# ==========================================

print(df[["discount_applied", "promo_code_used"]].head(10))
is_redundant = (df["discount_applied"] == df["promo_code_used"]).all()
print(f"Are discount_applied and promo_code_used identical? {is_redundant}")

df = df.drop("promo_code_used", axis=1)
print(df.columns)

# ==========================================
# 6. POSTGRESQL DATABASE INGESTION
# ==========================================

# Database connection settings come from environment variables so that no
# credentials are stored in the code. Only DB_PASSWORD is required.
username = os.environ.get("DB_USER", "postgres")
password = os.environ["DB_PASSWORD"]
host = os.environ.get("DB_HOST", "localhost")
port = os.environ.get("DB_PORT", "5432")
database = os.environ.get("DB_NAME", "customer_behavior")

# Create connection engine & load dataframe
engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)
table_name = "customer"

df.to_sql(table_name, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")