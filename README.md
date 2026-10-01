# Customer Shopping Behavior & Revenue Analysis

[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)

An end-to-end data analytics project exploring 3,900 customer transactions across demographic, purchase, and subscription dimensions to uncover revenue drivers, customer segments, and retention opportunities.

---

## Dashboard Preview

![Customer Behavior Dashboard](dashboard/dashboard_preview.png)

---

## Project Overview & Objectives

* **Dataset:** 3,900 purchase records with 18 features (demographics, transaction values, discounts, ratings, shipping types).
* **Objective:** Clean raw transactional data, engineer business features, answer core monetization questions using relational SQL queries, and present findings in an interactive Power BI dashboard.

---

## Tech Stack & Workflow

1. **Python (pandas):**
   * Handled missing data by imputing category-specific median ratings into `Review Rating` (37 nulls).
   * Standardized schema naming conventions to snake_case.
   * Engineered features: binned `age_group` (Young Adult, Middle-aged, Adult, Senior) and cleaned frequency metrics.
   * Conducted redundancy checks (verified `discount_applied` vs. `promo_code_used` and removed redundant attributes).

2. **PostgreSQL (pgAdmin 4):**
   * Loaded cleaned data via SQLAlchemy pipeline.
   * Executed analytical SQL queries using CTEs, window functions (`ROW_NUMBER()` / `DENSE_RANK()`), and conditional aggregations across 10 business use cases:
     * Revenue contribution by gender and age group.
     * High-spending discount users ($>\$59.76$ average order value).
     * Subscription vs. non-subscription spend behavior.
     * Category-level top product rankings and discount dependency rates.

3. **Power BI Desktop:**
   * Designed a responsive UI with custom color-accented KPI cards, donut distributions, and synchronized category/sales bar charts.
   * Built interactive multi-slicer filtering by Subscription Status, Gender, Category, and Shipping Type.

---

## Key Insights

* **Revenue Skew:** Male shoppers accounted for 67.7% of total revenue ($157.9K vs. $75.2K for female shoppers).
* **Subscription Uptake:** Only 27% (1,053) of customers hold active subscriptions. Average order value remained virtually identical between subscribers ($59.49) and non-subscribers ($59.87), indicating subscriptions drive predictability rather than larger basket sizes.
* **Top Revenue Categories:** Clothing dominated order volume and revenue (> $100K), followed by Accessories, Footwear, and Outerwear.
* **Discount Vulnerability:** Over 47%–50% of purchases in categories like Hats, Sneakers, and Coats were transacted under discounts, highlighting product lines where price sensitivity is highest.

---

## Actionable Business Recommendations

1. **Subscription Restructuring:** Introduce tiered perks or member-exclusive merchandise to incentivize basket growth, as current subscribers spend the same per transaction as non-subscribers.
2. **Targeted Loyalty Programs:** 3,116 customers fall into the "Loyal" cohort based on previous transactions; prioritizing retention automations here yields higher ROI than broad acquisition discounts.
3. **Margin Protection:** Rationalize discount schedules on high-margin apparel and reserve promotional codes for clearing low-velocity inventory.

---

## Running the Pipeline

The script loads the cleaned data into a local PostgreSQL database named
`customer_behavior`. The database password is read from an environment
variable, so no credentials are stored in the code:

```bash
export DB_PASSWORD="your-postgres-password"
python notebooks/eda_and_data_cleaning.py
```

---

## Repository Contents

* `notebooks/`: Jupyter Notebook containing data preprocessing, median imputation, and feature binning.
* `sql/`: Clean `.sql` scripts detailing all 10 business problem queries.
* `dashboard/`: The standalone `.pbix` Power BI file and high-resolution layout preview.
