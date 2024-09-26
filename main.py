import pandas as pd
import requests
from bs4 import BeautifulSoup

# Download CSV file from the web
def download_csv(url, local_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV file downloaded successfully to {local_path}")
    except Exception as e:
        print(f"Error downloading the CSV file: {e}")

# Scrape population data from City-Data.com
def scrape_population_data():
    url = "https://www.city-data.com/city/Texas.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    cities = []
    populations = []

    # Extract city names and population from the table
    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) >= 3:
            city = columns[1].get_text().strip().lower()  # Ensure lowercase city names for consistency
            population = columns[2].get_text().strip().replace(',', '')

            # Skip non-city data and ensure population is a number
            if population.isdigit():
                cities.append(city)
                populations.append(int(population))
    
    # Create a DataFrame
    df_population = pd.DataFrame({'City': cities, 'Population': populations})
    
    return df_population

# Clean and polish the CSV data
def clean_csv(df_schools):
    # Ensure City column is a string and remove leading/trailing spaces
    df_schools['City'] = df_schools['City'].astype(str).str.strip().str.lower()

    # Convert population to integer (assuming population column exists and has valid values)
    if 'Population' in df_schools.columns:
        df_schools['Population'] = pd.to_numeric(df_schools['Population'], errors='coerce')

    # Fill missing values for numerical columns with 0 and text columns with 'Unknown'
    for col in df_schools.columns:
        if df_schools[col].dtype == 'float64' or df_schools[col].dtype == 'int64':
            df_schools[col] = df_schools[col].fillna(0)
        else:
            df_schools[col] = df_schools[col].fillna('Unknown')

    # Remove any duplicate rows
    df_schools = df_schools.drop_duplicates()

    return df_schools

# Main logic to process the dataset
def process_dataset(school_csv_url, output_path):
    # Define local path for the downloaded school CSV
    local_school_csv_path = './downloaded_schools_data.csv'

    # Step 1: Download the school CSV
    download_csv(school_csv_url, local_school_csv_path)

    # Step 2: Load and clean the school CSV data
    df_schools = pd.read_csv(local_school_csv_path, low_memory=False)
    df_schools = clean_csv(df_schools)


    # Step 4: Scrape population data from City-Data.com
    df_population = scrape_population_data()

    # Step 5: Merge the school data with population data on 'City'
    df_final = pd.merge(df_schools, df_population, on='City', how='left')

    # Step 6: Fill missing population values with a default of 1 to avoid division by zero
    df_final['Population'] = df_final['Population'].fillna(1)

    # Step 7: Calculate metrics like schools per capita and average population per school
    df_final['Number_of_Schools'] = df_final.groupby('City')['City'].transform('count')
    df_final['Schools_per_Capita'] = df_final['Number_of_Schools'] / df_final['Population']
    df_final['Avg_Population_per_School'] = df_final['Population'] / df_final['Number_of_Schools']

    # Handle cases where population or number of schools is zero
    df_final['Schools_per_Capita'] = df_final['Schools_per_Capita'].replace([float('inf'), -float('inf')], 0)
    df_final['Avg_Population_per_School'] = df_final['Avg_Population_per_School'].replace([float('inf'), -float('inf')], 0)

    # Step 8: Select only the necessary columns (adjust this based on available columns)
    necessary_columns = [
        'City', 'USER_School_Name', 'USER_District_Name', 'USER_School_Enrollment_as_of_', 
        'USER_District_Enrollment_as_of_', 'School_Type', 'Population', 'Number_of_Schools', 
        'Schools_per_Capita', 'Avg_Population_per_School'
    ]
    
    # Filter only columns that exist in the dataset
    df_final = df_final[[col for col in necessary_columns if col in df_final.columns]]

    # Step 9: Save the final dataset to a new CSV file
    try:
        df_final.to_csv(output_path, index=False)
        print(f"Final dataset saved to {output_path}")
    except Exception as e:
        print(f"Error saving the final CSV file: {e}")

# URL of the school data CSV file stored on the web
school_csv_url = 'https://hub.arcgis.com/api/v3/datasets/3bbafea2252246bb887cf28336a2ca69_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1'

# Define the output path for the cleaned and merged dataset
output_path = './final_school_population_dataset.csv'

# Run the process
process_dataset(school_csv_url, output_path)