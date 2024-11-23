""" THIS TURNS THE XML FILES INTO
import pandas as pd
from lxml import etree


# Parse the XML file
tree = etree.parse("UNdata_Export_20241122_130805571.xml")

# Extract records
records = []
for record in tree.xpath("//record"):
    # Create a dictionary for each record
    record_data = {}
    for field in record.xpath(".//field"):
        # Use the 'name' attribute as the key, and text as the value
        record_data[field.attrib['name']] = field.text
    records.append(record_data)

# Convert the list of dictionaries to a DataFrame
data = pd.DataFrame(records)

# Display the DataFrame structure
print(data.head())

# Optional: Save the cleaned data to a CSV file
data.to_csv("cleaned_data_6.csv", index=False)
"""
"""FOR THE FIRST TWO XML FILES
import pandas as pd

# Load the CSV file
data = pd.read_csv("cleaned_data_3.csv")

# Display initial structure and summary of the dataset
print("Initial dataset shape:", data.shape)
print("Initial columns:", data.columns.tolist())
print("Sample data:\n", data.head())

# Step 1: Normalize column names
data.columns = (
    data.columns.str.strip()  # Remove leading/trailing spaces
    .str.lower()  # Convert to lowercase
    .str.replace(" ", "_")  # Replace spaces with underscores
    .str.replace("[^a-z0-9_]", "")  # Remove non-alphanumeric characters
)

# Step 2: Handle missing values
# Replace NaN or missing strings in critical columns
data.fillna("Missing", inplace=True)

# Alternatively, drop rows with critical missing fields if required:
# data.dropna(subset=['observation_value'], inplace=True)

# Step 3: Ensure proper data types
# Convert numeric fields to appropriate types
data["observation_value"] = pd.to_numeric(data["observation_value"], errors="coerce")
data["time_period"] = pd.to_numeric(data["time_period"], errors="coerce")

# Step 4: Drop unnecessary or redundant columns
# Example: Drop "age_group" if it's always "Not applicable"
if "age_group" in data.columns and data["age_group"].nunique() == 1:
    data.drop(columns=["age_group"], inplace=True)

# Step 5: Remove duplicates (if applicable)
data.drop_duplicates(inplace=True)

# Step 6: Optional - Aggregate data
# Example: Aggregate observation values by 'reference_area' and 'time_period'
aggregated_data = data.groupby(
    ["reference_area", "time_period"]
)["observation_value"].sum().reset_index()

# Step 7: Save cleaned data to a new file
cleaned_file_name = "cleaned_simplified_data_3.csv"
aggregated_data.to_csv(cleaned_file_name, index=False)

print(f"Cleaned data saved to {cleaned_file_name}")

"""
import pandas as pd
import numpy as np

# Load the XML data into a DataFrame
data = pd.read_csv("cleaned_data_6.csv")


# 1. Remove redundant columns
if 'Sex' in data.columns and data['Sex'].nunique() == 1:
    data.drop(columns=['Sex'], inplace=True)

if 'Age group' in data.columns and data['Age group'].nunique() == 1:
    data.drop(columns=['Age group'], inplace=True)

if 'Units of measurement' in data.columns and data['Units of measurement'].nunique() == 1:
    data.drop(columns=['Units of measurement'], inplace=True)

# 2. Handle missing or placeholder values
# Replace "…" or blanks in 'Value' with NaN
data['Observation Value'] = pd.to_numeric(data['Observation Value'].replace({'…': np.nan, '': np.nan}), errors='coerce')

# 4. Remove rows with entirely missing values
data.dropna(subset=['Observation Value'], inplace=True)

# 5. Standardize "Value Footnotes"
# Replace blanks with "No footnotes"
#data['Value Footnotes'] = data['Value Footnotes'].fillna("No footnotes")

# 6. Save cleaned data
cleaned_file = "final_cleaned_data_6.csv"
data.to_csv(cleaned_file, index=False)

print(f"Cleaned data saved to {cleaned_file}")
