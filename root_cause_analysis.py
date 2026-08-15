import pandas as pd

df = pd.read_csv('cleaned_supply_chain.csv')
print(df.shape)
print(df['Shipping Mode'].value_counts())
late_by_shipping = df.groupby('Shipping Mode')['is_late'].mean() * 100
print(late_by_shipping)
shipping_days_comparison = df.groupby('Shipping Mode')[['Days for shipping (real)', 'Days for shipment (scheduled)']].mean()
print(shipping_days_comparison)
late_by_region = df.groupby('Order Region')['is_late'].mean().sort_values(ascending=False) * 100
print(late_by_region)

late_by_market = df.groupby('Market')['is_late'].mean().sort_values(ascending=False) * 100
print(late_by_market)
correlation_check = df[['is_late', 'Order Item Discount Rate', 'Order Item Quantity', 'Sales']].corr()
print(correlation_check['is_late'])
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Convert Shipping Mode into a format the model can use (dummy/one-hot encoding)
shipping_dummies = pd.get_dummies(df['Shipping Mode'], drop_first=True)
print(shipping_dummies.head())

# Prepare our input features (X) and target (y)
X = shipping_dummies.astype(int)
y = df['is_late']

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression(solver='liblinear')
model.fit(X_train, y_train)

# Check accuracy on the test set
accuracy = model.score(X_test, y_test)
print('Model accuracy:', accuracy)

# Look at the coefficients (this tells us the effect of each shipping mode)
coefficients = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_[0]})
print(coefficients)

coefficients.to_csv('shipping_mode_risk_factors.csv', index=False)
late_by_shipping.to_csv('late_rate_by_shipping_mode.csv')
print('Root cause analysis saved')