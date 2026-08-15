import pandas as pd

abc_xyz = pd.read_csv('abc_xyz_classification.csv')
forecast_results = pd.read_csv('forecast_results.csv')

print(abc_xyz.columns.tolist())
print(forecast_results.columns.tolist())

scorecard = abc_xyz.merge(forecast_results, on='Product Name', how='left')
print(scorecard.shape)
print(scorecard.head(10))

def abc_score(abc_class):
    if abc_class == 'A':
        return 3
    elif abc_class == 'B':
        return 2
    else:
        return 1

def xyz_score(xyz_class):
    if xyz_class == 'Z':
        return 3
    elif xyz_class == 'Y':
        return 2
    else:
        return 1

scorecard['abc_points'] = scorecard['ABC_class'].apply(abc_score)
scorecard['xyz_points'] = scorecard['XYZ_class'].apply(xyz_score)

print(scorecard[['Product Name', 'ABC_class', 'abc_points', 'XYZ_class', 'xyz_points']].head(10))

# For products without a forecast error, treat missing as 0 (no extra info to add)
scorecard['Forecast_Error_Percent'] = scorecard['Forecast_Error_Percent'].fillna(0)

# Normalize forecast error to a comparable 0-3 scale (so it doesn't overpower the other scores)
scorecard['forecast_points'] = scorecard['Forecast_Error_Percent'] / scorecard['Forecast_Error_Percent'].max() * 3
scorecard['forecast_points'] = scorecard['forecast_points'].fillna(0)

# Final combined risk score
scorecard['risk_score'] = scorecard['abc_points'] + scorecard['xyz_points'] + scorecard['forecast_points']

final_scorecard = scorecard[['Product Name', 'Sales', 'ABC_class', 'XYZ_class', 'Forecast_Error_Percent', 'risk_score']].sort_values(by='risk_score', ascending=False)
print(final_scorecard.head(15))

scorecard['has_forecast'] = scorecard['Forecast_Error_Percent'] > 0

final_scorecard = scorecard[['Product Name', 'Sales', 'ABC_class', 'XYZ_class', 'Forecast_Error_Percent', 'has_forecast', 'risk_score']].sort_values(by='risk_score', ascending=False)

print(final_scorecard.head(20))
final_scorecard.to_csv('final_risk_scorecard.csv', index=False)
print('Risk scorecard saved')