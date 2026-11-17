import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme()


DATA = "September 2026 Complete Monthly Ridership (with adjustments and estimates)_261102.xlsx"
FIRST = 2016
LAST = 2025

KEEP_COLUMNS = ["NTD ID", "Agency", "Mode/Type of Service Status",
                "Reporter Type", "Mode", "TOS", "3 Mode"]


def read_transit(data: str) -> pd.DataFrame:
    """Yearly ridership per agency/mode with HQ state, FIRST to LAST."""
    master = pd.read_excel(data, sheet_name="Master")
    years = pd.read_excel(data, sheet_name="Calendar Year UPT")
    years = years.dropna(subset=["NTD ID"])
    states = master[["NTD ID", "Mode", "TOS", "HQ State"]]
    merged = years.merge(states, on=["NTD ID", "Mode", "TOS"], how="left")
    return merged[KEEP_COLUMNS + ["HQ State"] + list(range(FIRST, LAST + 1))]


def state_year_totals(df: pd.DataFrame, first: int, last: int) -> pd.DataFrame:
    years = list(range(first, last + 1))
    return df.groupby("HQ State")[years].sum(min_count=1)


def plot_national_trend(table: pd.DataFrame) -> None:
    totals = table.sum() / 1e9 #to keep the axis numbers readable
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(totals.index, totals.values, marker="o")
    ax.set_title("Total US transit ridership by year, 2015-2025")
    ax.set_xlabel("Year")
    ax.set_ylabel("Unlinked passenger trips (billions)")
    ax.set_ylim(bottom=0)
    fig.savefig('transit_ridership_by_year.png', bbox_inches="tight")
    plt.close(fig)


def plot_top_states(table: pd.DataFrame, year: int, n: int) -> None:
    ridership = table[year].dropna()
    top_states = sorted(ridership.index,
                        key=lambda state: ridership[state],
                        reverse=True)[:n]
    top = ridership[top_states] / 1e6
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top.index, y=top.values, ax=ax, color="blue")
    ax.set_title(f"Top {n} states by transit ridership, {year}")
    ax.set_xlabel("HQ state")
    ax.set_ylabel("Unlinked passenger trips (millions)")
    fig.savefig('top_states.png', bbox_inches="tight")
    plt.close(fig)


def missing_by_year(df: pd.DataFrame, first: int, last: int) -> pd.Series:
    """Percent of agency/mode rows with no ridership value, per year."""
    years = list(range(first, last + 1))
    return df[years].isna().mean() * 100


def summarize_ridership(df: pd.DataFrame, first: int,
                        last: int) -> pd.DataFrame:
    """Summary statistics (count, mean, std, quartiles) per year."""
    years = list(range(first, last + 1))
    return df[years].describe()


def main() -> None:
    df = read_transit(DATA)
    table = state_year_totals(df, FIRST, LAST)

    print("Shape (rows, columns):", df.shape)
    print("Missing % by year:")
    print(missing_by_year(df, FIRST, LAST).round(1))
    print("Missing cells in state-by-year table:", table.isna().sum().sum())
    print(summarize_ridership(df, FIRST, LAST))
    print(df["3 Mode"].value_counts())
    print(df["Reporter Type"].value_counts())

    plot_national_trend(table)
    plot_top_states(table, LAST, 10)


if __name__ == "__main__":
    main()