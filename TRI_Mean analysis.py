import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid", palette="muted")

def read_ruggedness_data(dataset_filepath: str, sheet: str) -> pd.DataFrame:
    return pd.read_excel(dataset_filepath, sheet_name= sheet, header=1)


def road_TRI_stats(df: pd.DataFrame, state_col: str, road_TRI: str) -> pd.DataFrame:
    road_TRI_desc = (df.groupby(state_col)[road_TRI].describe())
    road_stats = road_TRI_desc.sort_values(by='mean')
    return road_stats

def state_road_TRI_plot(stats: pd.DataFrame, state_col: str, stat_col: str )-> None:
    stats = stats.reset_index()
    plt.figure(figsize=(8, 12))
    road_plot = sns.scatterplot(data=stats, x=stat_col, y=state_col)
    road_plot.invert_yaxis()
    plt.savefig('scatter_plot_road_TRI.png', bbox_inches='tight')



def area_TRI_stats(df: pd.DataFrame, state_col: str, area_TRI: str) -> pd.DataFrame:
    area_TRI_desc = (df.groupby(state_col)[area_TRI].describe())
    area_stats = area_TRI_desc.sort_values(by='mean')
    return area_stats

def main():
    df = read_ruggedness_data('(read)ruggedness-scales-2020-tracts.xlsx',
                               'Ruggedness Scales 2020 Data')
    road_summary = road_TRI_stats(df, 'StateName20', 'RoadTRI_Mean')
    #area_summary = area_TRI_stats(df, 'StateName20', 'AreaTRI_Mean')
    state_road_TRI_plot(road_summary, 'StateName20', 'mean')




if __name__ == '__main__':
    main()
