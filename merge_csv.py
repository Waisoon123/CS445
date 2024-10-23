import pandas as pd

csv_files = {
    'RansomHub\RansomHub.csv': 'RansomHub',
    'Play\Play.csv': 'Play',
    'IncRansom\IncRansom.csv': 'IncRansom',
    'Blackbasta\BlackBasta.csv': 'BlackBasta'
}

dfs = []
for file, group in csv_files.items():
    df = pd.read_csv(file)
    df['Ransomware Group'] = group
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True)

merged_df['Date'] = pd.to_datetime(merged_df['Date'], errors='coerce', format='%d/%m/%Y')

# Sort the DataFrame by the 'Date' column from oldest to newest
sorted_df = merged_df.sort_values(by='Date')

sorted_df['Date'] = sorted_df['Date'].dt.strftime('%d/%m/%Y')

sorted_df.to_csv('merged_output.csv', index=False)
