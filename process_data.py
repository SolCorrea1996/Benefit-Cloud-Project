import pandas as pd

# Make Cleaned Outbound File for SSN Data
#1 Load inbound file
df = pd.read_csv('employees_inbound.csv')

#2 Remove all the non-digit from the dataframe
df['ssn'] = df['ssn'].str.replace(r'\D', '', regex=True)

#3 Ensure SSN is 9 digits 
df = df[df['ssn'].str.len() == 9]

#Make Cleaned Outbound File for Date YYYY-MM-DD Data
#4 Normalize date columns format to YYYY-MM-DD
date_columns = ['dob', 'hire_date', 'term_date', 'effective_date']
# Convert date columns to datetime and format to YYYY-MM-DD
for col in date_columns:
    df[col] = pd.to_datetime(
        df[col], 
        errors='coerce',
        format= 'mixed' # Accepts multiple date formats, coerces invalid parsing to NaT and also works with Pandas 2.0+
    )
    df[col] = df[col].dt.strftime('%Y-%m-%d')

#5 Mapping dictionary for messy plan names to clean plan names
plan_name_mapping = {
    #Medical PPO Plans
    'PPO-Med Plan': 'Medical PPO',
    'Med_PPO': 'Medical PPO',
    'PPO Medical': 'Medical PPO',
    'Medical PPO Core': 'Medical PPO',
    'MED PPO - Core': 'Medical PPO',
    
    #Medical HDHP Plans
    'Medical HDHP': 'Medical HDHP',
    'HDHP - Medical': 'Medical HDHP',
    'High Deductible Medical': 'Medical HDHP',
    
    #Dental Basic Plans
    'Dental - BASIC': 'Dental Basic',
    'Basic Dental Plan': 'Dental Basic',
    'Dental Basic': 'Dental Basic',
    
    #Dental Premium Plans
    'Premium Dental Coverage': 'Dental Premium',
    'Dental - Premium Plan': 'Dental Premium',
    'Dental Premium': 'Dental Premium',
    
    #Vision Core Plans
    'VISION Core Option': 'Vision Core',

    #Vision Premium Plans
    'VIS-BUYUP': 'Vision Premium',
    'vision-buy-up': 'Vision Premium',
    
    #FSA Plans setting none
    'fsa-variation-1': None,
    'FSA_VOYA': None
}

#6 Clean plan names using mapping dictionary
df['clean_name'] = df['plan_name'].map(plan_name_mapping)

#7 Remove rows with plan_name as None
df = df[df['clean_name'].notna()]

#8 Build Name column by concatenating first_name and last_name
df['Name'] = df['first_name'] + ' ' + df['last_name']

#Build the carrier outbound file
carrier_export_columns = pd.DataFrame({
    'MemberID': df['employee_id'],
    'Name': df['Name'],
    'DOB': df['dob'],
    'SSN': df['ssn'],
    'Plan': df['clean_name'],
    'Coverage': df['coverage_level'],
    'Effective Date': df['effective_date']
})

# Export the cleaned carrier file to CSV
carrier_export_columns.to_csv('carrier_export.csv', index=False)

# Print completion message
print("Data processing complete. Cleaned file saved as: 'carrier_export.csv' in the current directory.")