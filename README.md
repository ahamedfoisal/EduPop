

# EduPop: Mapping Texas Schools and Populations for Smarter Planning

## Project Overview

**EduPop** is a data pipeline project designed to combine education-related data from Texas schools with population data for cities across Texas. By using web scraping and API integrations, this project provides insights into the relationship between city populations and school density, a dataset not readily available for free online. The goal is to help urban planners, educational policymakers, and researchers better understand how well school systems in different cities cater to their populations.

## Data Sources

1. **School Data (API)**: 
   - We used the Texas Schools dataset available via ArcGIS, which contains data on school names, district names, enrollment, and more.
   - The API link: [ArcGIS Schools Data](https://hub.arcgis.com/api/v3/datasets/3bbafea2252246bb887cf28336a2ca69_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1)

2. **Population Data (Web Scraping)**: 
   - Population data for Texas cities was scraped from [City-Data.com](https://www.city-data.com/city/Texas.html), a website that doesn't provide a publicly accessible API but offers detailed population figures for cities in Texas.

## Key Features

- **Schools per Capita**: This dataset reveals the number of schools available per person in each city, helping identify areas with potential school shortages.
- **Average Population per School**: This shows the average number of people that a school in a city serves, which can highlight overcrowded school systems or underpopulated areas with excess school capacity.

## Why is This Dataset Valuable?

The **EduPop** dataset provides a unique combination of data that isn't available online for free. It gives stakeholders in education and urban planning the ability to:

- **Identify school accessibility gaps** in cities where populations are underserved by existing educational infrastructure.
- **Assist in planning future educational infrastructure** by helping decision-makers understand which cities require additional school investments.
- **Optimize resource allocation** by providing a clear view of how educational resources are distributed in relation to population size.

This dataset not only helps in educational policy but can also be used to assist urban planning in rapidly growing cities or in identifying rural areas that might need additional resources.

## Installation and Usage

To run this project locally, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/ahamedfoisal/EduPop.git
   ```

2. Navigate into the project directory:
   ```bash
   cd EduPop
   ```

3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the main Python script to generate the dataset:
   ```bash
   python main.py
   ```

6. The final dataset will be saved as `final_school_population_dataset.csv` in the project directory.

## Project Structure

```
EduPop/
│
├── main.py                 # The main Python script for the project
├── requirements.txt        # Python dependencies
├── README.md               # Project overview
├── ETHICS.md               # Ethical considerations
├── final_school_population_dataset.csv   # Example of the cleaned dataset output
└── .gitignore              # To exclude unnecessary files like virtual env
```

---

