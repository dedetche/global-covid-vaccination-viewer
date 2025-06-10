import pandas as pd
import matplotlib.pyplot as plt

# download data from https://ourworldindata.org/covid-vaccinations
# and save it as "vaccinations_global.csv" in the same directory as this script
df = pd.read_csv("vaccinations_global.csv")

# Extracting the year from the date column
df["year"] = pd.to_datetime(df["date"]).dt.year

while True:
    country = input("\nEnter the country name (or type 'exit' to quit): ").strip()
    if country.lower() == "exit":
        print("Program closed. Goodbye!")
        break

    try:
        year = int(input("Enter the year (e.g., 2021, 2022): ").strip())
    except ValueError:
        print("Invalid year. Please enter a 4-digit number.")
        continue

    # Fiter the DataFrame for the specified country and yea
    df_country_year = df[
        (df["country"].str.lower() == country.lower()) &
        (df["year"] == year)
    ]

    if df_country_year.empty:
        print(f"No data found for '{country}' in {year}. Please try another.")
        continue

    # it gets the latest vaccination data for the specified country and year
    df_valid = df_country_year.dropna(subset=["people_vaccinated", "people_fully_vaccinated", "total_boosters"])

    if df_valid.empty:
        print(f"No valid vaccination data found for '{country}' in {year}.")
        continue

    latest = df_valid.sort_values(by="date", ascending=False).iloc[0]

    vaccinated = latest["people_vaccinated"]
    fully_vaccinated = latest["people_fully_vaccinated"]
    boosters = latest["total_boosters"]

    labels = ["At least one dose", "Fully vaccinated", "Boosters"]
    values = [
        vaccinated if not pd.isna(vaccinated) else 0,
        fully_vaccinated if not pd.isna(fully_vaccinated) else 0,
        boosters if not pd.isna(boosters) else 0
    ]

    print(f"\nVaccination data for {country.title()} in {year} (as of {latest['date']}):")
    print(f"• At least one dose: {int(vaccinated) if not pd.isna(vaccinated) else 'N/A'}")
    print(f"• Fully vaccinated : {int(fully_vaccinated) if not pd.isna(fully_vaccinated) else 'N/A'}")
    print(f"• Boosters         : {int(boosters) if not pd.isna(boosters) else 'N/A'}")

    # Graphical representation of the vaccination data
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color="mediumseagreen")
    plt.title(f"COVID-19 Vaccination in {country.title()} – {year}")
    plt.ylabel("People")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.show()
