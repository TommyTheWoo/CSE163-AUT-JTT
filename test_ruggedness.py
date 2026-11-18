import pandas as pd
import seaborn as sns

sns.set_theme(style="darkgrid", palette="muted")


def read_ruggedness_data(dataset_filepath: str, sheet: str) -> pd.DataFrame:
    """
    Reads the ruggedness Scales 2020 excel sheet as a DataFrame.
    """
    return pd.read_excel(dataset_filepath, sheet_name=sheet, header=1)
    


def missing_values(df: pd.DataFrame) -> int:
    """
    Takes in a DataFrame df, returns
    any rows with missing values.
    """
    row_length = len(df)
    dropped_row_length = len(df.dropna())
    missing_rows = row_length - dropped_row_length
    return missing_rows


def check_rows(df: pd.DataFrame) -> int:
    """
    Takes in a DataFrame df of the ruggedness file and 
    returns any rows that have a 0 value in both the RoadTRI_Min
    and RoadTRI_Count columns.
    """
    zero_min_rows = df[df['RoadTRI_Min'] == 0]
    zero_count_rows = (zero_min_rows['RoadTRI_Count'] == 0).sum()
    return zero_count_rows


def test_ruggedness_count(df: pd.DataFrame) -> None:
    """
    Testing function for check_rows.
    """
    assert 0 == check_rows(df)


def main():
    df = read_ruggedness_data('(read)ruggedness-scales-2020-tracts.xlsx',
                              'Ruggedness Scales 2020 Data')
    test_ruggedness_count(df)
    print("All tests passed!")
    print(f'There are {missing_values(df)} rows with missing values.')


if __name__ == '__main__':
    main()
