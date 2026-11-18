"""
Tests vehicle_registration_analysis.py
"""
import pandas as pd
import vehicle_registration_analysis as vra


def test_statistics(data: dict[pd.DataFrame], year):
    return vra.statistics(data[year])


def main():
    data = vra.main()
    assert round(test_statistics(data, 2020).loc['mean', 'PHEV'], 3) == \
        11654.902
    assert round(test_statistics(data, 2020).loc['std', 'EV'], 3) == \
        59547.384
    assert test_statistics(data, 2020).loc['max', 'PHEV'] == \
        265500.0
    assert test_statistics(data, 2025).loc['50%', 'Gasoline'] == \
        3379700.0
    assert test_statistics(data, 2025).loc['25%', 'EV'] == \
        13500.0
    assert test_statistics(data, 2025).loc['max', 'PHEV'] == \
        490900.0
    print('All tests passed?!')


if __name__ == '__main__':
    main()
