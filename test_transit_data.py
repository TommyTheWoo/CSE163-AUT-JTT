import numpy as np
import pandas as pd

from transit_data import state_year_totals


def test_state_year_totals() -> None:
    df = pd.DataFrame({
        "HQ State": ["WA", "WA", "OR", "OR"],
        2015: [10.0, 5.0, np.nan, np.nan],
        2016: [1.0, np.nan, 2.0, 3.0],
    })
    table = state_year_totals(df, 2015, 2016)
    assert 15 == table.loc["WA", 2015]
    assert 1 == table.loc["WA", 2016]
    assert 5 == table.loc["OR", 2016]
    assert pd.isna(table.loc["OR", 2015])


def main() -> None:
    test_state_year_totals()
    print("All tests passed!")


if __name__ == "__main__":
    main()