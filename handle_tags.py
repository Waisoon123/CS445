import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv("merged_output.csv")

# Split the "Tags" column into a list of tags
df['Tags'] = df['Tags'].str.split(',')

# Create a new DataFrame by exploding the list of tags
df_exploded = df.explode('Tags')

# Remove leading and trailing whitespace from the "Tags" column
df_exploded['Tags'] = df_exploded['Tags'].str.strip().str.lower()

# Create a new column "Data Group" and assign "Customer" if the tag contains "client" or "customer"
df_exploded['Data Type'] = df_exploded['Tags'].apply(lambda x: 'Customer data' if ('client' in x or 'customer' in x) 
                                                    else 'Company data' if ('corporate' in x or 'company' in x or 'department' in x or 'business' in x) 
                                                    else 'Financial data' if ('finance' in x or 'financial' in x or 'investment' in x) 
                                                    else 'Personal/User data' if ('personal' in x or 'user' in x) 
                                                    else 'Tax data' if ('tax' in x) 
                                                    else 'Employee data' if ('employee' in x or 'staff' in x) 
                                                    else 'School/Student data' if ('student' in x or 'school' in x)
                                                    else 'Product data' if ('product' in x)
                                                    else 'Legal data' if ('legal' in x or 'law' in x) 
                                                    else 'HR data' if ('hr' in x or 'human resource' in x) 
                                                    else 'Insurance data' if ('insurance' in x) 
                                                    else 'Bank data' if ('bank' in x) 
                                                    else 'Accounting/Audit data' if ('accounting' in x or 'audit' in x or 'account' in x) 
                                                    else 'Patient/Medical data' if ('patient' in x or 'medical' in x) 
                                                    else 'Sales data' if ('sales' in x or 'sale' in x) 
                                                    else 'Contract data' if ('contract' in x) 
                                                    else 'Admin data' if ('admin' in x)
                                                    else 'Marketing data' if ('marketing' in x or 'advertisement' in x)
                                                    else 'Confidential data' if ('confidential' in x or 'non disclosure' in x or 'non-disclosure' in x or 'nda' in x) 
                                                    else x)

# Save the exploded DataFrame to a new CSV file
df_exploded.to_csv("tags_handled.csv", index=False)






