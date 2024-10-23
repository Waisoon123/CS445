import pandas as pd

# Read the CSV file
file_path = 'IncRansom\IncRansom.csv'  # Update with file path
df = pd.read_csv(file_path)

# Function to check if Country matches Country Code
def check_country_match(country, country_code):
    country_code_mapping = {
        'United States': 'US',
        'Great Britain': 'GB',
        'Canada': 'CA',
        'Germany': 'DE',
        'South Africa': 'ZA',
        'Switzerland': 'CH',
        'Peru': 'PE',
        'Malaysia': 'MY',
        'Belgium': 'BE',
        'Australia': 'AU',
        'Ireland': 'IE',
        'France': 'FR',
        'Portugal': 'PT',
        'The Netherlands': 'NL',
        'Czechia': 'CZ',
        'Pakistan': 'PK',
        'The Philippines': 'PH',
        'United Kingdom': 'UK'
    }
    
    if country in country_code_mapping:
        return country_code_mapping[country] == country_code
    else:
        return False

# Apply the function to create a new column for country match check
df['Country Match'] = df.apply(lambda row: check_country_match(row['Country'], row['Country Code']), axis=1)

# Function to infer the industry based on description
def infer_industry(description):
    if isinstance(description, str):  # Check if description is a string
        if 'education' in description.lower() or 'school' in description.lower():
            return 'Education'
        elif 'health' in description.lower() or 'medical' in description.lower() or 'hospital' in description.lower():
            return 'Healthcare'
        elif 'construction' in description.lower() or 'building' in description.lower():
            return 'Construction'
        elif 'transport' in description.lower() or 'logistics' in description.lower():
            return 'Transportation'
        elif 'government' in description.lower() or 'public' in description.lower():
            return 'Government'
        elif 'finance' in description.lower() or 'insurance' in description.lower():
            return 'Finance'
        elif 'technology' in description.lower() or 'software' in description.lower():
            return 'Technology'
        elif 'manufacturing' in description.lower() or 'production' in description.lower():
            return 'Manufacturing'
        elif 'retail' in description.lower() or 'store' in description.lower():
            return 'Retail'
        elif 'law' in description.lower() or 'legal' in description.lower():
            return 'Legal'
        elif 'security' in description.lower() or 'defense' in description.lower():
            return 'Security'
        else:
            return 'Other'
    else:
        return 'Other'  # If the description is not a string (e.g., NaN), return 'Other'

# Apply the industry inference function
df['Industry'] = df.apply(lambda row: infer_industry(row['Description']), axis=1)

# Export the updated DataFrame to an Excel file
output_file_path = 'updated_file.xlsx'  # Update with desired output path
df.to_excel(output_file_path, index=False)

print(f"File has been saved to {output_file_path}")
