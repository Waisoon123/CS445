import os
import csv
from dotenv import load_dotenv
from jigsawstack import JigsawStack, JigsawStackError

# Load API key from .env file
load_dotenv()
my_api_key = os.getenv("JIGSAWSTACK_API_KEY")

# Initialize JigsawStack with the API key
jigsawstack = JigsawStack(api_key=my_api_key)

# Read the descriptions from the CSV file
csv_file_path = 'scraped_data_with_sectors_cleaned.csv'  # Update with your CSV file path
output_file_path = 'scraped_data_with_sectors2.csv'  # Output CSV file path
rows = []
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for i, row in enumerate(csvreader):
        # Skip the header and process only the first two rows
        if i < 2:  # First two rows after header (0-indexed)
            try:
                rows.append(row)  # Append only the first two rows
            except UnicodeDecodeError:
                print(f"Skipping row due to encoding error: {row}")
        else:
            break  # Stop after appending the first two rows

# Process each description and add the sector to the row
for row in rows:
    description = row['Description']  # Update with the correct column name
    params = {
        "prompt": f"Based on the following description, what business sector or industry does it suggest? {description}",
        "return_prompt": "Return exactly one business sector / industry based on the description provided without any filler sentences",
        "prompt_guard": ["sexual_content", "defamation"],
    }

    try:
        result = jigsawstack.prompt_engine.run_prompt_direct(params)
        row['Sector'] = result['result']  # Extract the 'result' from the response
    except JigsawStackError as e:
        print(f"Error processing description: {description}")
        print(f"Error message: {e}")
        row['Sector'] = "Error"

# Write the updated rows to a new CSV file
if rows:  # Check if rows were processed
    fieldnames = rows[0].keys()  # Get field names from the first row
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(rows)

    print(f"Results have been written to {output_file_path}")
else:
    print("No rows were processed.")
