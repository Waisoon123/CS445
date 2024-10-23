import pandas as pd

csv_files = ['RansomHub\RansomHub.csv', 'Play\Play.csv', 'IncRansom\IncRansom_cleaned.csv', 'Blackbasta\BlackBasta_Cleaned_Standardized.csv']  # replace with your actual file paths

dfs = [pd.read_csv(file) for file in csv_files]

merged_df = pd.concat(dfs, ignore_index=True)

merged_df['Date'] = pd.to_datetime(merged_df['Date'], errors='coerce', format='%d/%m/%Y')

# Sort the DataFrame by the 'Date' column from oldest to newest
sorted_df = merged_df.sort_values(by='Date')

sorted_df['Date'] = sorted_df['Date'].dt.strftime('%d/%m/%Y')

sorted_df.to_csv('merged_output.csv', index=False)