import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

# Load and prepare data
df = pd.read_csv('cleaned_supply_chain.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_month'] = df['order_date'].dt.to_period('M')

# Trim incomplete final months (Oct 2017 onward showed an ~80% volume drop
# across ALL products — confirmed as incomplete data, not a real business event)
df_trimmed = df[df['order_month'] <= '2017-09']
print('Original rows:', df.shape[0])
print('Trimmed rows:', df_trimmed.shape[0])

# Error metrics
def mean_abs_error(actual, predicted):
    return np.mean(np.abs(np.array(actual) - np.array(predicted)))

def mean_abs_percent_error(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    return np.mean(np.abs((actual - predicted) / actual)) * 100

# Reusable forecasting function
def forecast_product(product_name, data):
    product_df = data[data['Product Name'] == product_name]
    monthly = product_df.groupby('order_month')['Order Item Quantity'].sum()

    train = monthly[:-6]
    test = monthly[-6:]

    model = SimpleExpSmoothing(train).fit(optimized=True)
    forecast = model.forecast(6)

    error_abs = mean_abs_error(test, forecast)
    error_pct = mean_abs_percent_error(test, forecast)
    smoothing = model.model.params['smoothing_level']

    return error_abs, error_pct, smoothing

# Load top 6 revenue products from our ABC-XYZ results
abc_xyz_df = pd.read_csv('abc_xyz_classification.csv')
top_products = abc_xyz_df.sort_values(by='Sales', ascending=False).head(6)['Product Name'].tolist()
print(top_products)

# Run forecast for each top product using the TRIMMED data
print()
print('--- Forecast results (using trimmed, complete-months-only data) ---')
for p in top_products:
    error_abs, error_pct, smoothing = forecast_product(p, df_trimmed)
    print(p, '| Error (units):', round(error_abs, 1), '| Error %:', round(error_pct, 1), '| Smoothing level:', round(smoothing, 3))

results = []
for p in top_products:
    error_abs, error_pct, smoothing = forecast_product(p, df_trimmed)
    results.append({'Product Name': p, 'Forecast_Error_Units': round(error_abs, 1), 
                     'Forecast_Error_Percent': round(error_pct, 1), 'Smoothing_Level': round(smoothing, 3)})

forecast_results_df = pd.DataFrame(results)
forecast_results_df.to_csv('forecast_results.csv', index=False)
print('Forecast results saved')