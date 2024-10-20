import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('scraped_data.csv')

# Filter the DataFrame to keep only rows where "Disclosed Links" contains "http://"
filtered_df = df[df['Disclosed Links'].str.contains('http://', na=False)]

# Further filter the DataFrame to remove rows where "Sector" or "Countries" contain the word "Error"
filtered_df = filtered_df[~filtered_df['Sector'].str.contains('Error', na=False)]
filtered_df = filtered_df[~filtered_df['Countries'].str.contains('Error', na=False)]

# Remove column [Description] from the DataFrame
filtered_df = filtered_df.drop(columns=['Description'])

# Save the cleaned DataFrame back to a CSV file
filtered_df.to_csv('RansomHub.csv', index=False)
