import pandas as pd

# Function to extract industry based on keywords from the 'Company Info'
def extract_industry(info):
    info_lower = info.lower()

    # Dictionary of common industries and associated keywords
    industries = {
        'Maritime': ['shipping', 'vessel', 'cargo', 'maritime', 'marine'],
        'Commodities': ['commodities', 'grain', 'agriculture', 'trading'],
        'Construction': ['construction', 'building', 'supplies'],
        'Manufacturing': ['manufacturing', 'manufacturer', 'industries', 'industrial', 'manufactures', 'fabrics'],
        'Environmental': ['environmental', 'waste', 'recycling'],
        'Technology': ['technology', 'software', 'it', 'tech', 'networking'],
        'Healthcare': ['healthcare', 'medical', 'pharma', 'biotech'],
        'Retail': ['retail', 'wholesale', 'consumer', 'barber', 'products', 'newspaper'],
        'Financial': ['financial', 'banking', 'insurance', 'investments', 'accountancy', 'accounting', 'collection'],
        'Energy': ['energy', 'oil', 'gas', 'mining', 'electrical'],
        'Transport': ['transport'],
        'Media': ['newspaper', 'media', 'broadcast'],
        'Food and Beverage': ['food', 'beverage', 'beef', 'pork'],
        'Automotive': ['automotive'],
        'Real Estate': ['real estate', 'estate'],
        'Logistics': ['logistics'],
        'Legal Service': ['legal services']
        }

    for industry, keywords in industries.items():
        if any(keyword in info_lower for keyword in keywords):
            return industry

    return 'Unknown'

def add_industry_column(file_path, output_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Fill missing values in 'Company Info' column with an empty string
    data['Company Info'] = data['Company Info'].fillna('')

    # Apply the extraction function to the 'Company Info' column
    data['Industry'] = data['Company Info'].apply(extract_industry)

    # Save the updated data with the 'Industry' column to a new CSV file
    data.to_csv(output_path, index=False)

if __name__ == '__main__':
    input_file = 'play_ransomware_data.csv'  # Replace with your input file path
    output_file = 'output_with_industry.csv'  # Replace with your desired output file path
    add_industry_column(input_file, output_file)
