import pandas as pd

df = pd.read_csv('cleaned_supply_chain.csv')
print(df.shape)
print(df['Product Name'].nunique())
product_revenue = df.groupby('Product Name')['Sales'].sum().reset_index()
product_revenue = product_revenue.sort_values(by='Sales', ascending=False)
print(product_revenue.head(10))
total_revenue = product_revenue['Sales'].sum()

product_revenue['revenue_percent'] = product_revenue['Sales'] / total_revenue * 100
product_revenue['cumulative_percent'] = product_revenue['revenue_percent'].cumsum()

print(product_revenue.head(15))
def assign_abc(cum_percent):
    if cum_percent <= 70:
        return 'A'
    elif cum_percent <= 90:
        return 'B'
    else:
        return 'C'

product_revenue['ABC_class'] = product_revenue['cumulative_percent'].apply(assign_abc)

print(product_revenue['ABC_class'].value_counts())
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_month'] = df['order_date'].dt.to_period('M')

monthly_demand = df.groupby(['Product Name', 'order_month'])['Order Item Quantity'].sum().reset_index()
print(monthly_demand.head(10))
demand_stats = monthly_demand.groupby('Product Name')['Order Item Quantity'].agg(['mean', 'std']).reset_index()
demand_stats['CV'] = demand_stats['std'] / demand_stats['mean']

print(demand_stats.head(10))
def assign_xyz(cv):
    if pd.isna(cv):
        return 'Z'
    elif cv <= 0.5:
        return 'X'
    elif cv <= 1.0:
        return 'Y'
    else:
        return 'Z'

demand_stats['XYZ_class'] = demand_stats['CV'].apply(assign_xyz)

print(demand_stats['XYZ_class'].value_counts())
final_table = product_revenue.merge(demand_stats, on='Product Name')
final_table['ABC_XYZ'] = final_table['ABC_class'] + final_table['XYZ_class']

print(final_table[['Product Name', 'Sales', 'ABC_class', 'CV', 'XYZ_class', 'ABC_XYZ']].sort_values(by='Sales', ascending=False))
print(final_table['ABC_XYZ'].value_counts())
final_table.to_csv('abc_xyz_classification.csv', index=False)
print('ABC-XYZ analysis saved')