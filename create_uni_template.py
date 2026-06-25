import pandas as pd

# Load existing universities
df = pd.read_excel('tcu/tcu_data.xlsx')
unis = df['University'].unique()

# Create a template DataFrame
template_df = pd.DataFrame({
    'University Name': unis,
    'Region': ['Dar es Salaam'] * len(unis), # Default region to avoid errors, user can change it
    'Type (University/Institute/College)': ['University'] * len(unis),
    'Umiliki (Private/Government)': ['Government'] * len(unis),
    'Website': [''] * len(unis),
    'Email': [''] * len(unis),
    'Phone Number': [''] * len(unis),
    'Description': [''] * len(unis)
})

template_df.to_excel('university_details_template.xlsx', index=False)
print("Template created successfully!")
