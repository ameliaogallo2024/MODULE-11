# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- DATA CREATION (DO NOT MODIFY) -----
np.random.seed(42)
# Updated 'Q' to 'QE' to fix the red warning text
quarters = pd.date_range(start='2022-01-01', periods=8, freq='QE')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                  'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []
for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.3 if quarter.quarter == 4 else (0.8 if quarter.quarter == 1 else 1.0)
            location_factor = {'Tampa': 1.0, 'Miami': 1.2, 'Orlando': 0.9, 'Jacksonville': 0.8}[location]
            category_factor = {'Electronics': 1.5, 'Clothing': 1.0, 'Home Goods': 0.8, 'Sporting Goods': 0.7, 'Beauty': 0.9}[category]
            growth_factor = (1 + 0.05/4) ** quarter_idx
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            quarterly_data.append({
                'Quarter': quarter, 'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location, 'Category': category, 'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2), 'Year': quarter.year
            })

customer_data = []
age_params = {'Tampa': (45, 15), 'Miami': (35, 12), 'Orlando': (38, 14), 'Jacksonville': (42, 13)}
for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(2000 * {'Tampa': 0.3, 'Miami': 0.35, 'Orlando': 0.2, 'Jacksonville': 0.15}[location])
    ages = np.clip(np.random.normal(loc=mean_age, scale=std_age, size=customer_count), 18, 80).astype(int)
    for age in ages:
        if age < 30: p = [0.3, 0.3, 0.1, 0.2, 0.1]
        elif age < 50: p = [0.25, 0.2, 0.25, 0.15, 0.15]
        else: p = [0.15, 0.1, 0.35, 0.1, 0.3]
        category_preference = np.random.choice(categories, p=p)
        base_amount = np.random.gamma(shape=5, scale=20)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], p=[0.3, 0.5, 0.2])
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        customer_data.append({
            'Location': location, 'Age': age, 'Category': category_preference,
            'PurchaseAmount': round(base_amount * tier_factor, 2), 'PriceTier': price_tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# ----- VISUALIZATION FUNCTIONS -----

def plot_quarterly_sales_trend():
    fig, ax = plt.subplots(figsize=(8, 5))
    trend = sales_df.groupby('QuarterLabel', sort=False)['Sales'].sum()
    ax.plot(trend.index, trend.values, marker='o', color='tab:blue', linewidth=2)
    ax.set_title('Overall Quarterly Sales Trend')
    ax.set_ylabel('Total Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.6)
    return fig

def plot_location_sales_comparison():
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot = sales_df.pivot_table(index='QuarterLabel', columns='Location', values='Sales', aggfunc='sum', sort=False)
    pivot.plot(ax=ax, marker='s')
    ax.set_title('Sales Comparison by Location')
    ax.legend(title='Location', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    return fig

def plot_category_performance_by_location():
    fig, ax = plt.subplots(figsize=(10, 6))
    latest = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    perf = latest.pivot_table(index='Location', columns='Category', values='Sales', aggfunc='sum')
    perf.plot(kind='bar', ax=ax)
    ax.set_title('Category Performance by Location (Latest Quarter)')
    plt.xticks(rotation=0)
    return fig

def plot_sales_composition_by_location():
    fig, ax = plt.subplots(figsize=(10, 6))
    comp = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    comp_pct = comp.div(comp.sum(axis=1), axis=0) * 100
    comp_pct.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Sales Composition % by Location')
    ax.set_ylabel('Percentage (%)')
    plt.xticks(rotation=0)
    return fig

def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots(figsize)