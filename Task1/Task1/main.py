import pandas as pd
from statsmodels.stats.proportion import proportions_ztest


file_path = 'raw_data.csv'
data = pd.read_csv(file_path)


data['successful_payment'] = data['successful_payment'].fillna(0)
data['amount'] = data['amount'].fillna(0)


conversion = data.groupby('split_group')['successful_payment'].mean()
arpu = data.groupby('split_group')['amount'].mean()


comparison_df = pd.DataFrame({
    'Conversion Rate': conversion,
    'ARPU': arpu,
    'Users': data.groupby('split_group')['id_user'].count(),
    'Payments': data.groupby('split_group')['successful_payment'].sum()
}).reset_index()


comparison_df['Group'] = comparison_df['split_group'].replace({0: 'Control', 1: 'Test'})
comparison_df = comparison_df.drop(columns=['split_group'])


success_counts = comparison_df['Payments']
n_counts = comparison_df['Users']


z_stat, p_value = proportions_ztest(success_counts, n_counts)


comparison_df['z-statistic'] = [z_stat, z_stat]
comparison_df['p-value'] = [p_value, p_value]


print(comparison_df)

