import pandas as pd

xls = pd.ExcelFile('Cohort Analysis.xlsx')

retention_rate = pd.read_excel(xls, 'Users Retention Rate', skiprows=3)
emails_sent = pd.read_excel(xls, 'Emails sent', skiprows=3)
emails_clicks = pd.read_excel(xls, 'Emails clicks', skiprows=3)


def clean_data(df, value_name):
    df.columns = ['Week of Install', 'Installs'] + [f"Week {i}" for i in range(1, len(df.columns)-1)]
    df = df.melt(id_vars=['Week of Install', 'Installs'], var_name='Week', value_name=value_name)
    df['Week'] = df['Week'].str.extract('(\\d+)').astype(int)
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce')
    return df


emails_sent_clean = clean_data(emails_sent, 'Emails Sent')
emails_clicks_clean = clean_data(emails_clicks, 'Emails Clicks')
retention_clean = clean_data(retention_rate, 'Retention Rate')


emails_data = emails_sent_clean.merge(emails_clicks_clean, on=['Week of Install', 'Week', 'Installs'])


def avg_emails_per_user(weeks):
    df = emails_data[emails_data['Week'] <= weeks]
    summary = df.groupby('Week of Install').agg({'Emails Sent': 'sum', 'Installs': 'first'})
    summary['Avg Emails per User'] = summary['Emails Sent'] / summary['Installs']
    return summary['Avg Emails per User'].mean()


avg_3_months = avg_emails_per_user(13)
avg_6_months = avg_emails_per_user(26)
avg_12_months = avg_emails_per_user(52)


user_lifetime_weeks = retention_clean.groupby('Week of Install').apply(
    lambda x: x['Retention Rate'].fillna(0).sum()  ).mean()


annual_cost = avg_12_months * 0.1


def calculate_ctr(start_week, end_week):
    cohort = emails_data[(emails_data['Week of Install'] >= start_week) & (emails_data['Week of Install'] <= end_week)]
    return cohort['Emails Clicks'].sum() / cohort['Emails Sent'].sum()


ctr_17_20 = calculate_ctr(17, 20)
ctr_21_24 = calculate_ctr(21, 24)
ctr_25_28 = calculate_ctr(25, 28)


results = pd.DataFrame({
    'Metric': [
        '1a', '1б', '1в',
        'Користувач живе тижнів:', 'Річна вартість утримання', '4а',
        '4б', '4в'
    ],
    'Value': [
        avg_3_months, avg_6_months, avg_12_months, user_lifetime_weeks,
        annual_cost, ctr_17_20, ctr_21_24, ctr_25_28
    ]
})


print(results)
