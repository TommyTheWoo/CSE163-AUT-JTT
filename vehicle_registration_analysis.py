"""

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import read_vehicle_registration_html as rvrh

def statistics(df: pd.DataFrame, col: str):
    return df[col].describe()


def plot_totals_by_year(data: dict[pd.DataFrame], col: str, ax):
    years = []
    means = []
    for year, df in data.items():
        years.append(year)
        means.append(df[col].sum())
    ax.plot(years, means, label=col)


def plot_states_by_year():
    pass


def plot_totals_all():
    sns.set_theme()
    data = rvrh.main()
    fig, ax = plt.subplots(1, figsize=(15, 7))
    for col in ['EV', 'PHEV', 'HEV', 'Gasoline']:
        plot_totals_by_year(data, col, ax)
    plt.title('US vehicle registration by type over time')
    plt.xlabel('Year')
    plt.ylabel('Registrations (log)')
    plt.yscale('log')
    plt.legend()
    plt.savefig('totals_by_year.png', bbox_inches='tight')


if __name__ == '__main__':
    main()