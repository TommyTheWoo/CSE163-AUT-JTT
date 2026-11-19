
"""
Analyzes the relationship between terrain ruggedness
and vehicle registration by fuel type.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ruggedness_stats as rs
import vehicle_registration_data as vrd

sns.set_theme(style='whitegrid', palette='muted')


def aggregate_terrain(data):
    """
    Calculates population-weighted average area TRI
    for each state.
    """
    data = data.copy()

    data['Population'] = pd.to_numeric(
        data['Population'], errors='coerce'
    )
    data['AreaTRI_Mean'] = pd.to_numeric(
        data['AreaTRI_Mean'], errors='coerce'
    )

    data = data.dropna(
        subset=['StateName20', 'Population', 'AreaTRI_Mean']
    )

    data['weighted_TRI'] = (
        data['AreaTRI_Mean'] * data['Population']
    )

    result = data.groupby('StateName20').agg(
        weighted_TRI=('weighted_TRI', 'sum'),
        Population=('Population', 'sum')
    ).reset_index()

    result['AreaTRI_Mean'] = (
        result['weighted_TRI'] / result['Population']
    )

    return result[['StateName20', 'AreaTRI_Mean']]


def merge_data(terrain_data, vehicle_data, year):
    """
    Merges state-level terrain data with vehicle
    registration data for a selected year.
    """
    terrain = aggregate_terrain(terrain_data)
    vehicles = vehicle_data[year].copy()

    fuel_types = ['EV', 'PHEV', 'HEV', 'Gasoline']

    for fuel in fuel_types:
        vehicles[fuel] = pd.to_numeric(
            vehicles[fuel].astype(str).str.replace(',', ''),
            errors='coerce'
        )

    data = pd.merge(
        terrain,
        vehicles,
        left_on='StateName20',
        right_on='State',
        how='inner'
    )

    # Calculate percentage of registrations by fuel type
    data['Total'] = data[fuel_types].sum(axis=1)

    for fuel in fuel_types:
        data[f'{fuel}_rate'] = (
            data[fuel] / data['Total'] * 100
        )

    return data


def plot_tri_fuel(data, fuel_type, ax):
    """
    Plots terrain ruggedness against the registration
    percentage of a selected fuel type.
    """
    sns.regplot(
        data=data,
        x='AreaTRI_Mean',
        y=f'{fuel_type}_rate',
        ax=ax,
        scatter_kws={'s': 45, 'alpha': 0.7},
        line_kws={'color': 'red', 'linewidth': 2}
    )

    ax.set_xlabel('Population-weighted Area TRI')
    ax.set_ylabel('Registration share (%)')
    ax.set_title(f'{fuel_type} vehicles')
    

def main():
    # Read original datasets
    terrain_data = rs.read_ruggedness_data(
        '(read)ruggedness-scales-2020-tracts.xlsx',
        'Ruggedness Scales 2020 Data'
    )

    vehicle_data = vrd.main()

    year = 2020

    # Merge and calculate registration percentages
    data = merge_data(terrain_data, vehicle_data, year)

    print('Number of states:', len(data))
    print(data.head())

    # Create four plots
    fuel_types = ['EV', 'PHEV', 'HEV', 'Gasoline']

    fig, axes = plt.subplots(
        2, 2, figsize=(13, 9)
    )

    for fuel, ax in zip(fuel_types, axes.flatten()):
        plot_tri_fuel(data, fuel, ax)

    fig.suptitle(
        f'Terrain Ruggedness and Vehicle Registration by Fuel Type ({year})',
        fontsize=15,
        fontweight='bold'
    )

    plt.tight_layout()
    #plt.savefig('terrain_vehicle_combined.png',
                #dpi=300, bbox_inches='tight')
    #plt.show()


if __name__ == '__main__':
    main()

data = merge_data(terrain_data, vehicle_data, year)
print("Shape:", data.shape)
print("Number of rows:", len(data))
print("Number of columns:", len(data.columns))
print("Missing values:", data.isna().sum().sum())