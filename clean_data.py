import pandas as pd

df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='latin1')
print(df.shape)
for col in df.columns:
    print(col)
print(df.isnull().sum())
columns_to_drop = [
    'Customer Email', 'Customer Password', 'Customer Fname', 'Customer Lname',
    'Customer Street', 'Product Description', 'Order Zipcode', 'Product Image'
]

df = df.drop(columns=columns_to_drop)
print(df.shape)
df = df.dropna(subset=['Customer Zipcode'])
print(df.shape)
df['order_date'] = pd.to_datetime(df['order date (DateOrders)'])
df['shipping_date'] = pd.to_datetime(df['shipping date (DateOrders)'])

df = df.drop(columns=['order date (DateOrders)', 'shipping date (DateOrders)'])

print(df[['order_date', 'shipping_date']].head())
print(df.duplicated().sum())
print('Negative Sales:', (df['Sales'] < 0).sum())
print('Negative Quantity:', (df['Order Item Quantity'] < 0).sum())
df['is_late'] = (df['Delivery Status'] == 'Late delivery').astype(int)

print(df['is_late'].value_counts())
df.to_csv('cleaned_supply_chain.csv', index=False)
print('Saved successfully')