"""
Analyzes the relationship between terrain ruggedness
and vehicle registration by fuel type.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ruggedness_stats as rs
import vehicle_registration_data as vrd

sns.set_theme()


def merge_data(data1, data2, year):
    result = pd.merge(data1, data2[year], on='State', how='inner')
    return result


def plot_tri_fuel(data1, data2, fuel_type, ax, year):
    data = merge_data(data1, data2, year)
    sns.relplot(data=data, x='TRI_mean', y=fuel_type, ax=ax)
    ax.set_xlabel('TRI mean')
    ax.set_ylabel(f'{fuel_type} vehicle registrations')
    ax.set_title(f'{fuel_type} registrations against TRI in {year}')


def main():
    terrain_data = rs.main()
    vehicle_data = vrd.main()
    fig, ax = plt.subplots(1, figsize=(15, 7))
    plot_tri_fuel(terrain_data, vehicle_data, 'EV', ax, 2020)
    plt.savefig('hello.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
