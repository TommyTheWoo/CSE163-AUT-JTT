"""
Analysis of the light-duty vehicle registration data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import vehicle_registration_data as rvrh

def statistics(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a seven number summary (mean, stdev, and percentiles)
    of a dataframe.
    '''
    return df.describe().drop('count')


def plot_totals_by_year(data: dict[pd.DataFrame], col: str, ax) -> None:
    '''
    Produces a plot representing the total count of vehicles of a certain
    fuel type over years.
    '''
    years = []
    means = []
    for year, df in data.items():
        years.append(year)
        means.append(df[col].sum())
    ax.plot(years, means, label=col)


def plot_states_by_year(data, state, year) -> None:
    '''
    Produces a plot representing the the distribution of vehicles with fuel
    types EV, PHEV, HEV, and Gasoline for a given state and year.
    '''
    df = data[year]
    sns.catplot(df[df['State'] == state], kind='bar')
    plt.title(f'Fuel type distribution in {state}')
    plt.xlabel('Fuel type')
    plt.ylabel('Amount registered (log)')
    plt.yscale('log')
    plt.savefig(f'{state.lower()}_registered_vehicle_types.png', bbox_inches='tight')


def plot_totals_all(data) -> None:
    '''
    Produces a plot representing the total count of vehicles of fuel types
    EV, PHEV, HEV, and Gasoline over years.
    '''
    sns.set_theme()
    fig, ax = plt.subplots(1, figsize=(15, 7))
    for col in ['EV', 'PHEV', 'HEV', 'Gasoline']:
        plot_totals_by_year(data, col, ax)
    plt.title('US vehicle registration by type over time')
    plt.xlabel('Year')
    plt.ylabel('Registrations (log)')
    plt.yscale('log')
    plt.legend()
    plt.savefig('totals_by_year.png', bbox_inches='tight')

def main():
    data = rvrh.main()
    plot_totals_all(data)
    plot_states_by_year(data, 'Washington', 2020)
    return data

if __name__ == '__main__':
    main()
