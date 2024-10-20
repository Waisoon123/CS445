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
csv_file_path = 'scraped_data.csv'  # Update with your CSV file path
rows = []
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        try:
            rows.append(row)
        except UnicodeDecodeError:
            print(f"Skipping row due to encoding error: {row}")

# Process each description and add the sector to the row
for row in rows:
    description = row['Description']  # Update with the correct column name
    params = {
        "prompt": f"Based on the following description, identify the country the business if from {description}",
        "return_prompt": "Return the country identified based on the description provided.",
        "prompt_guard": ["sexual_content", "defamation"],
    }

    try:
        result = jigsawstack.prompt_engine.run_prompt_direct(params)
        row['Countries'] = result['result']  # Extract the 'result' from the response
    except JigsawStackError as e:
        print(f"Error processing description: {description}")
        print(f"Error message: {e}")
        row['Countries'] = "Error"

# Write the updated rows to the same CSV file
fieldnames = rows[0].keys()  # Get field names from the first row
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writeheader()
    csvwriter.writerows(rows)

print(f"Results have been written to {csv_file_path}")
