import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, Region

def update_universities():
    excel_file = "university_details_template.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Faili la {excel_file} halijapatikana!")
        return

    print("Ninasoma taarifa za vyuo kutoka kwenye Excel...")
    df = pd.read_excel(excel_file)
    
    updated_count = 0
    for index, row in df.iterrows():
        uni_name = str(row['University Name']).strip()
        
        try:
            uni = University.objects.get(name=uni_name)
            
            # Update fields
            # Region
            region_name = str(row['Region']).strip()
            if region_name and region_name != 'nan':
                region, created = Region.objects.get_or_create(name=region_name)
                uni.region = region
                
            # Type
            type_val = str(row['Type (University/Institute/College)']).strip()
            if type_val and type_val != 'nan':
                uni.type = type_val
                
            # Umiliki
            umiliki_val = str(row['Umiliki (Private/Government)']).strip()
            if umiliki_val and umiliki_val != 'nan':
                uni.umiliki = umiliki_val
                
            # Website
            website = str(row['Website']).strip()
            if website and website != 'nan':
                uni.website = website
                
            # Email
            email = str(row['Email']).strip()
            if email and email != 'nan':
                uni.email = email
                
            # Phone
            phone = str(row['Phone Number']).strip()
            if phone and phone != 'nan':
                uni.phone_number = phone
                
            # Description
            desc = str(row['Description']).strip()
            if desc and desc != 'nan':
                uni.description = desc
                
            uni.save()
            updated_count += 1
            
        except University.DoesNotExist:
            print(f"Chuo hakijapatikana kwenye database: {uni_name}")
            
    print(f"Tumemaliza! Tumefanikiwa kuweka taarifa (Update) vyuo {updated_count}.")

if __name__ == '__main__':
    update_universities()
