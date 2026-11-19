"""
Analyzes the relationship between public transit ridership
and vehicle registration by fuel type.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import transit_data as td
import vehicle_registration_data as vrd

states = pd.DataFrame(
    {
        'abbr': [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
            'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
            'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
            'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
            'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        ],
        'State': [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
            'Colorado', 'Connecticut',  'Delaware', 'Florida', 'Georgia',
            'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
            'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
            'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
            'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
            'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
            'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
            'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
            'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
            'District of Columbia'
        ]
    }
)


def state_merged(data: pd.DataFrame, data2: dict[pd.DataFrame],
                 year: int) -> pd.DataFrame:
    '''
    Merges datasets on state abbreviations to state names.
    '''
    data = data.reset_index()
    initial = pd.merge(data, states, left_on='HQ State',
                       right_on='abbr', how='inner')
    return pd.merge(initial, data2[year], on='State', how='inner')


def plot_reg_transit(data, data2, year):
    '''
    Plots a regression plot comparing public transit ridership and
    registered vehicle fuel types for a given year.
    '''
    df = state_merged(data, data2, year)
    fuels = ['EV', 'PHEV', 'HEV', 'Gasoline']
    total = df[fuels].sum(axis=1)
    fig, ax = plt.subplots(figsize=(10, 6))
    for fuel in fuels:
        share = df[fuel] / total
        df['z'] = (share - share.mean()) / share.std()
        fuel_df = df[['z', year]].rename(columns={year: 'ridership'})
        sns.regplot(data=fuel_df, x='z', y='ridership', ax=ax, label=fuel,
                    scatter_kws={'s': 3, 'alpha': 0.6})
    ax.set_xlabel('Registrations (z-score)')
    ax.set_ylabel(f'Transit ridership, {year}')
    ax.set_title('Public transit ridership against vehicle fuel type '
                 f'proportions (z-scored) by state, {year}')
    ax.legend()
    plt.savefig('transit_registration_regression.png', bbox_inches='tight')


def plot_corr_over_time(data, data2):
    '''
    Plots a line plot tracking the change in correlations over time in years.
    '''
    years = list(range(2016, 2026))
    results = pd.DataFrame({year: correlations(data, data2, year)
                            for year in years}).T
    fig, ax = plt.subplots(figsize=(10, 6))
    for fuel in ['EV', 'PHEV', 'HEV', 'Gasoline']:
        ax.plot(results.index, results[fuel], label=fuel)
    ax.set_xlabel('Year')
    ax.set_ylabel('Correlation')
    ax.set_title('Correlation of vehicle fuel type and ridership over time')
    ax.legend()
    plt.savefig('corr_over_time.png', bbox_inches='tight')


def correlations(data, data2, year):
    '''
    Computes the correlation between transit data and
    vehicle registration data for a given year
    '''
    df = state_merged(data, data2, year)
    fuels = ['EV', 'PHEV', 'HEV', 'Gasoline']
    total = df[fuels].sum(axis=1)
    results = {}
    for fuel in fuels:
        share = df[fuel] / total
        results[fuel] = round(share.corr(df[year]), 3)
    return pd.Series(results, name=f'Pearson r, {year}')


def main():
    transit_data = td.main()
    vehicle_data = vrd.main()
    merged = state_merged(transit_data, vehicle_data, 2020)
    print("Merged shape (rows, columns):", merged.shape)
    print(merged.isna().sum())
    sns.set_theme()
    plot_reg_transit(transit_data, vehicle_data, 2020)
    plot_corr_over_time(transit_data, vehicle_data,)
    print(correlations(transit_data, vehicle_data, 2020))


if __name__ == '__main__':
    main()
