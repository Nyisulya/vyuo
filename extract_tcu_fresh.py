import pdfplumber
import pandas as pd
import re
import os

pdf_path = r"d:\projects\django1\university_portal\vyuofinder\tcu\Admission Guidebook for Holders of Secondary School Qualifications_2025_2026.pdf"
output_excel = r"d:\projects\django1\university_portal\vyuofinder\tcu_extracted_data.xlsx"

unique_headers = [
    "AbdulrahmanAl-SumaitUniversity(SUMAIT),Zanzibar",
    "AgaKhanUniversity(AKU),DaresSalaam",
    "ArchbishopMihayoUniversityCollegeofTabora(AMUCTA),Tabora",
    "ArdhiUniversity(ARU),DaresSalaam",
    "ArushaTechnicalCollege(ATC),Arusha",
    "CatholicUniversityofHealthandAlliedSciences(CUHAS),Mwanza",
    "CatholicUniversityofMbeya(CUoM),Mbeya",
    "CollegeofAfricanWildlifeManagement(CAWM),Mweka-Kilimanjaro",
    "CollegeofBusinessEducation(CBE),DaresSalaam",
    "CollegeofBusinessEducation(CBE),Dodoma",
    "CollegeofBusinessEducation(CBE),Mbeya",
    "CollegeofBusinessEducation(CBE),Mwanza",
    "DaresSalaamInstituteofTechnology(DIT),DaresSalaam",
    "DaresSalaamInstituteofTechnology(DIT)-MwanzaCampus",
    "DaresSalaamMaritimeInstitute(DMI),DaresSalaam",
    "DaresSalaamTumainiUniversity(DarTU),DaresSalaam",
    "EasternAfricaStatisticalTrainingCentre(EASTC),DaresSalaam",
    "InstituteofAccountancyArusha(IAA),Arusha",
    "InstituteofAccountancyArusha(IAA),DaresSalaamCampus",
    "InstituteofAdultEducation(IAE),DaresSalaam",
    "InstituteofFinanceManagement(IFM),DaresSalaam",
    "InstituteofFinanceManagement(IFM),Dodoma",
    "InstituteofFinanceManagement(IFM),Mwanza",
    "InstituteofFinanceManagement(IFS),Simiyu",
    "InstituteofPublicAdministration(IPA),Zanzibar",
    "InstituteofRuralDevelopmentPlanning(IRDP),Dodoma",
    "InstituteofRuralDevelopmentPlanning(IRDP),Mwanza",
    "InstituteofSocialWork(ISW),DaresSalaam",
    "InstituteofSocialWork(ISW)KisangaraCampus,Kilimanjaro",
    "InstituteofTaxAdministration(ITA),DaresSalaam",
    "JordanUniversityCollege(JUCo),Morogoro",
    "KCMCUniversity,Kilimanjaro",
    "KairukiUniversity(KU),DaresSalaam",
    "KampalaInternationalUniversityinTanzania(KIUT),DaresSalaam",
    "KarumeInstituteofScienceandTechnology(KIST),Zanzibar",
    "KizumbiInstituteofCo-operativeandBusinessEducation(KICoB),Shinyanga",
    "LocalGovernmentTrainingInstitute(LGTI),Dodoma",
    "MSTrainingCentreforDevelopmentCooperation(MS-TCDC),Arusha",
    "MarianUniversityCollege(MARUCo),Bagamoyo",
    "MbeyaUniversityofScienceandTechnology(MUST),Mbeya",
    "MbeyaUniversityofScienceandTechnology(MUST)RukwaCampusCollege",
    "MkwawaUniversityCollegeofEducation(MUCE),Iringa",
    "MoshiCo-operativeUniversity(MoCU),Kilimanjaro",
    "MuhimbiliUniversityofHealthandAlliedSciences(MUHAS),DaresSalaam",
    "MuslimUniversityofMorogoro(MUM),Morogoro",
    "MwalimuNyerereMemorialAcademy(MNMA),DaresSalaam",
    "MwalimuNyerereMemorialAcademy(MNMA),ZanzibarCampus",
    "MwalimuNyerereMemorialAcademy(MNMA)-PembaCampus",
    "MwalimuNyerereUniversityofAgricultureandTechnology(MNUAT),Musoma",
    "MwanzaUniversity(MzU),Mwanza",
    "MwengeCatholicUniversity(MWECAU),Kilimanjaro",
    "MzumbeUniversity(MU),Morogoro",
    "MzumbeUniversityDaresSalaamCampusCollege(MUDCCo),DaresSalaam",
    "MzumbeUniversityMbeyaCampusCollege(MUMCCo),Mbeya",
    "NationalInstituteofTransport(NIT),DaresSalaam",
    "OpenUniversityofTanzania(OUT),DaresSalaam",
    "RuahaCatholicUniversity(RUCU),Iringa",
    "SokoineUniversityofAgriculture(SUA),Morogoro",
    "SokoineUniversityofAgriculture-MizengoPindaCampusCollege(SUA-MPCCo),Katavi",
    "St.AugustineUniversityofTanzania(SAUT),Mwanza",
    "St.AugustineUniversityofTanzania(SAUT)ArushaCentre,Arusha",
    "St.FrancisUniversityCollegeofHealthandAlliedSciences(SFUCHAS),Ifakara",
    "St.John'sUniversityofTanzania(SJUT),Dodoma",
    "St.JosephUniversityCollegeofEngineeringandTechnology(SJCET),DaresSalaam",
    "St.JosephUniversityCollegeofHealthandAlliedSciences(SJCHAS),DaresSalaam",
    "StateUniversityofZanzibar(SUZA),Zanzibar",
    "StellaMarisMtwaraUniversityCollege(STEMMUCo),Mtwara",
    "TanzaniaInstituteofAccountancy(TIA),DaresSalaam",
    "TanzaniaInstituteofAccountancy(TIA),Kigoma",
    "TanzaniaInstituteofAccountancy(TIA),Mbeya",
    "TanzaniaInstituteofAccountancy(TIA),Mtwara",
    "TanzaniaInstituteofAccountancy(TIA),Mwanza",
    "TanzaniaInstituteofAccountancy(TIA),Singida",
    "TanzaniaInstituteofAccountancy(TIA),Tanga",
    "TanzaniaInstituteofProjectManagement(TIPM),DaresSalaam",
    "TanzaniaPublicServiceCollege(TPSC),DaresSalaam",
    "TengeruInstituteofCommunityDevelopment(TICD),Arusha",
    "TeofiloKisanjiUniversity(TEKU),Mbeya",
    "TumainiUniversityMakumira(TUMA),Arusha",
    "UniqueAcademyDaresSalaam(UAD)",
    "UnitedAfricanUniversityofTanzania(UAUT),DaresSalaam",
    "UniversityofArusha(UoA),Arusha",
    "UniversityofDaresSalaam(UDSM),DaresSalaam",
    "UniversityofDodoma(UDOM),Dodoma",
    "UniversityofIringa(UoI),Iringa",
    "WaterInstitute(WI),DaresSalaam",
    "ZanzibarUniversity(ZU),Zanzibar"
]

official_names_spaced = {
    "AgaKhanUniversity(AKU)": "Aga Khan University (AKU)",
    "AbdulrahmanAl-SumaitUniversity(SUMAIT)": "Abdulrahman Al-Sumait University (SUMAIT)",
    "ArchbishopMihayoUniversityCollegeofTabora(AMUCTA)": "Archbishop Mihayo University College of Tabora (AMUCTA)",
    "ArdhiUniversity(ARU)": "Ardhi University (ARU)",
    "ArushaTechnicalCollege(ATC)": "Arusha Technical College (ATC)",
    "CatholicUniversityofHealthandAlliedSciences(CUHAS)": "Catholic University of Health and Allied Sciences (CUHAS)",
    "CatholicUniversityofMbeya(CUoM)": "Catholic University of Mbeya (CUoM)",
    "CenterforForeignRelations(CFR)": "Dr. Salim Ahmed Salim Centre for Foreign Relations (CFR)",
    "CollegeofAfricanWildlifeManagement(CAWM)": "College of African Wildlife Management (CAWM)",
    "CollegeofBusinessEducation(CBE)": "College of Business Education (CBE)",
    "DaresSalaamInstituteofTechnology(DIT)": "Dar es Salaam Institute of Technology (DIT)",
    "DaresSalaamMaritimeInstitute(DMI)": "Dar es Salaam Maritime Institute (DMI)",
    "DaresSalaamTumainiUniversity(DarTU)": "Dar es Salaam Tumaini University (DarTU)",
    "DaresSalaamUniversityCollegeofEducation(DUCE)": "Dar es Salaam University College of Education (DUCE)",
    "EasternAfricaStatisticalTrainingCentre(EASTC)": "Eastern Africa Statistical Training Centre (EASTC)",
    "InstituteofAccountancyArusha(IAA)": "Institute of Accountancy Arusha (IAA)",
    "InstituteofAdultEducation(IAE)": "Institute of Adult Education (IAE)",
    "InstituteofFinanceManagement(IFM)": "Institute of Finance Management (IFM)",
    "InstituteofFinanceManagement(IFS)": "Institute of Finance Management (IFS)",
    "InstituteofPublicAdministration(IPA)": "Institute of Public Administration (IPA)",
    "InstituteofRuralDevelopmentPlanning(IRDP)": "Institute of Rural Development Planning (IRDP)",
    "InstituteofSocialWork(ISW)": "Institute of Social Work (ISW)",
    "InstituteofTaxAdministration(ITA)": "Institute of Tax Administration (ITA)",
    "JordanUniversityCollege(JUCo)": "Jordan University College (JUCo)",
    "KairukiUniversity(KU)": "Kairuki University (KU)",
    "KampalaInternationalUniversityinTanzania(KIUT)": "Kampala International University in Tanzania (KIUT)",
    "KarumeInstituteofScienceandTechnology(KIST)": "Karume Institute of Science and Technology (KIST)",
    "KCMCUniversity": "Kilimanjaro Christian Medical University College (KCMUCo)",
    "KizumbiInstituteofCo-operativeandBusinessEducation(KICoB)": "Kizumbi Institute of Co-operative and Business Education (KICoB)",
    "LocalGovernmentTrainingInstitute(LGTI)": "Local Government Training Institute (LGTI)",
    "MSTrainingCentreforDevelopmentCooperation(MS-TCDC)": "MS Training Centre for Development Cooperation (MS-TCDC)",
    "MarianUniversityCollege(MARUCo)": "Marian University College (MARUCo)",
    "MbeyaUniversityofScienceandTechnology(MUST)": "Mbeya University of Science and Technology (MUST)",
    "MkwawaUniversityCollegeofEducation(MUCE)": "Mkwawa University College of Education (MUCE)",
    "MoshiCo-operativeUniversity(MoCU)": "Moshi Co-operative University (MoCU)",
    "MuhimbiliUniversityofHealthandAlliedSciences(MUHAS)": "Muhimbili University of Health and Allied Sciences (MUHAS)",
    "MuslimUniversityofMorogoro(MUM)": "Muslim University of Morogoro (MUM)",
    "MwalimuNyerereMemorialAcademy(MNMA)": "Mwalimu Nyerere Memorial Academy (MNMA)",
    "MwalimuNyerereUniversityofAgricultureandTechnology(MNUAT)": "Mwalimu Nyerere University of Agriculture and Technology (MNUAT)",
    "MwanzaUniversity(MzU)": "Mwanza University (MzU)",
    "MwengeCatholicUniversity(MWECAU)": "Mwenge Catholic University (MWECAU)",
    "MzumbeUniversity(MU)": "Mzumbe University (MU)",
    "NationalInstituteofTransport(NIT)": "National Institute of Transport (NIT)",
    "OpenUniversityofTanzania(OUT)": "Open University of Tanzania (OUT)",
    "RuahaCatholicUniversity(RUCU)": "Ruaha Catholic University (RUCU)",
    "SokoineUniversityofAgriculture(SUA)": "Sokoine University of Agriculture (SUA)",
    "St.AugustineUniversityofTanzania(SAUT)": "St. Augustine University of Tanzania (SAUT)",
    "St.FrancisUniversityCollegeofHealthandAlliedSciences(SFUCHAS)": "St. Francis University College of Health and Allied Sciences (SFUCHAS)",
    "St.John'sUniversityofTanzania(SJUT)": "St. John's University of Tanzania (SJUT)",
    "St.JosephUniversityCollegeofEngineeringandTechnology(SJCET)": "St. Joseph University College of Engineering and Technology (SJCET)",
    "St.JosephUniversityCollegeofHealthandAlliedSciences(SJCHAS)": "St. Joseph University College of Health and Allied Sciences (SJCHAS)",
    "StateUniversityofZanzibar(SUZA)": "State University of Zanzibar (SUZA)",
    "StellaMarisMtwaraUniversityCollege(STEMMUCo)": "Stella Maris Mtwara University College (STeMMUCo)",
    "TanzaniaInstituteofAccountancy(TIA)": "Tanzania Institute of Accountancy (TIA)",
    "TanzaniaInstituteofProjectManagement(TIPM)": "Tanzania Institute of Project Management (TIPM)",
    "TanzaniaPublicServiceCollege(TPSC)": "Tanzania Public Service College (TPSC)",
    "TengeruInstituteofCommunityDevelopment(TICD)": "Tengeru Institute of Community Development (TICD)",
    "TeofiloKisanjiUniversity(TEKU)": "Teofilo Kisanji University (TEKU)",
    "TumainiUniversityMakumira(TUMA)": "Tumaini University Makumira (TUMA)",
    "UniqueAcademyDaresSalaam(UAD)": "Unique Academy Dar es Salaam (UAD)",
    "UnitedAfricanUniversityofTanzania(UAUT)": "United African University of Tanzania (UAUT)",
    "UniversityofArusha(UoA)": "University of Arusha (UoA)",
    "UniversityofDaresSalaam(UDSM)": "University of Dar es Salaam (UDSM)",
    "UniversityofDodoma(UDOM)": "University of Dodoma (UDOM)",
    "UniversityofIringa(UoI)": "University of Iringa (UoI)",
    "WaterInstitute(WI)": "Water Institute (WI)",
    "ZanzibarUniversity(ZU)": "Zanzibar University (ZU)"
}

start_keywords = [
    "two principal", "three principal", "a principal", "at least", "holders of", 
    "admission to", "an applicant", "diploma in", "ordinary diploma", "full technician", 
    "applicants must", "in order to", "for admission", "candidates must", "two passes", 
    "three passes", "entry requirements", "minimum institutional", "equivalent qualifications"
]
start_keywords_spaceless = [kw.replace(" ", "") for kw in start_keywords]

def get_region(header):
    header_clean = header.replace(" ", "").replace("-", "")
    if "PembaCampus" in header_clean:
        return "Pemba"
    if "Rukwa" in header_clean:
        return "Rukwa"
    if "Katavi" in header_clean:
        return "Katavi"
    if "Ifakara" in header_clean:
        return "Morogoro"
    if "Mweka" in header_clean or "Kilimanjaro" in header_clean:
        return "Kilimanjaro"
    if "Bagamoyo" in header_clean:
        return "Pwani"
    
    regions = [
        ('DaresSalaam', 'Dar es Salaam'),
        ('Dodoma', 'Dodoma'),
        ('Mwanza', 'Mwanza'),
        ('Mbeya', 'Mbeya'),
        ('Arusha', 'Arusha'),
        ('Morogoro', 'Morogoro'),
        ('Tanga', 'Tanga'),
        ('Tabora', 'Tabora'),
        ('Zanzibar', 'Zanzibar'),
        ('Iringa', 'Iringa'),
        ('Singida', 'Singida'),
        ('Mtwara', 'Mtwara'),
        ('Kigoma', 'Kigoma'),
        ('Shinyanga', 'Shinyanga'),
        ('Lindi', 'Lindi'),
        ('Ruvuma', 'Ruvuma'),
        ('Mara', 'Mara'),
        ('Geita', 'Geita'),
        ('Simiyu', 'Simiyu'),
        ('Njombe', 'Njombe'),
        ('Manyara', 'Manyara'),
        ('Pwani', 'Pwani'),
        ('Kagera', 'Kagera'),
        ('Musoma', 'Mara')
    ]
    for r_check, r_display in regions:
        if r_check.lower() in header_clean.lower():
            return r_display
    return "Tanzania"

def get_type(name):
    name_clean = name.lower()
    if "university" in name_clean:
        return "University"
    else:
        return "Institute"

def get_ownership(name):
    name_clean = name.lower()
    private_phrases = [
        "aga khan", "sumait", "abdulrahman", "mihayo", "amucta", "cuhas", "cuom", 
        "tumaini", "dartu", "tuma", "jordan", "juco", "kairuki", "kiut", "marian", 
        "maruco", "muslim university", "mwanza university", "ruaha", 
        "rucu", "mwenge", "mwecau", "st. augustine", "saut", "st. francis", 
        "sfuchas", "st. john", "sjut", "st. joseph", "sjcet", "sjchas", 
        "stella maris", "stemmuco", "teofilo kisanji", "teku", "unique academy", 
        "united african", "uaut", "university of arusha", "university of iringa", 
        "zanzibar university", "kcmc", "kcmuco", "kilimanjaro christian", "tipm", 
        "ms training", "ms-tcdc"
    ]
    private_abbrevs = ["mzu", "zu", "uoa", "uoi", "uad", "mum"]
    
    for phrase in private_phrases:
        if phrase in name_clean:
            return "Private"
            
    for abbrev in private_abbrevs:
        if re.search(r'\b' + re.escape(abbrev) + r'\b', name_clean):
            return "Private"
            
    return "Government"

def clean_header_name(header):
    parts = header.split(",")
    name_part = parts[0].strip()
    if "PembaCampus" in header:
        name_part = "MwalimuNyerereMemorialAcademy(MNMA)-PembaCampus"
    elif "MizengoPindaCampusCollege" in header:
        name_part = "SokoineUniversityofAgriculture-MizengoPindaCampusCollege(SUA-MPCCo)"
    elif "RukwaCampusCollege" in header:
        name_part = "MbeyaUniversityofScienceandTechnology(MUST)RukwaCampusCollege"
    return name_part

def resolve_spaced_name(name_clean):
    spaced_name = name_clean
    for o_spaceless, o_spaced in official_names_spaced.items():
        if o_spaceless.lower() in name_clean.lower() or name_clean.lower() in o_spaceless.lower():
            spaced_name = o_spaced
            break
            
    if spaced_name == name_clean:
        if "DIT" in name_clean and "Mwanza" in name_clean:
            spaced_name = "Dar es Salaam Institute of Technology (DIT) - Mwanza Campus"
        elif "IAA" in name_clean and "DaresSalaam" in name_clean:
            spaced_name = "Institute of Accountancy Arusha (IAA) - Dar es Salaam Campus"
        elif "MNMA" in name_clean and "Zanzibar" in name_clean:
            spaced_name = "Mwalimu Nyerere Memorial Academy (MNMA) - Zanzibar Campus"
        elif "MNMA" in name_clean and "Pemba" in name_clean:
            spaced_name = "Mwalimu Nyerere Memorial Academy (MNMA) - Pemba Campus"
        elif "SUA" in name_clean and "Mizengo" in name_clean:
            spaced_name = "Sokoine University of Agriculture (SUA) - Mizengo Pinda Campus College"
        elif "MUST" in name_clean and "Rukwa" in name_clean:
            spaced_name = "Mbeya University of Science and Technology (MUST) - Rukwa Campus College"
            
    return spaced_name

def clean_requirements_shift(courses):
    cleaned_courses = []
    
    for idx, course in enumerate(courses):
        reqs = course["Requirements"]
        lines = reqs.split("\n")
        
        split_idx = 0
        for i, line in enumerate(lines):
            line_spaceless = line.strip().lower().replace(" ", "")
            if any(line_spaceless.startswith(kw) for kw in start_keywords_spaceless):
                split_idx = i
                break
                
        if split_idx > 0 and idx > 0:
            prev_continuation = " ".join(lines[:split_idx]).strip()
            cleaned_courses[-1]["Requirements"] = (cleaned_courses[-1]["Requirements"] + " " + prev_continuation).strip()
            course["Requirements"] = " ".join(lines[split_idx:]).strip()
        else:
            course["Requirements"] = " ".join(lines).strip()
            
        cleaned_courses.append(course)
        
    return cleaned_courses

def run_extraction():
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return
        
    print("Mchakato umeanza: Kufungua kitabu cha TCU PDF...")
    all_raw_courses = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Jumla ya kurasa za PDF: {total_pages}")
        
        current_university = "Unknown University"
        
        # Scan from page 25 (index 24) to the end
        for idx in range(24, total_pages):
            page = pdf.pages[idx]
            text = page.extract_text()
            if not text:
                continue
                
            # Check if this page contains a new university header
            text_spaceless = text.replace(" ", "").replace("\n", "")
            found_header = None
            for h in unique_headers:
                h_spaceless = h.replace(" ", "")
                if h_spaceless in text_spaceless:
                    found_header = h
                    break
                    
            if found_header:
                current_university = found_header
                print(f"Pahala: Ukurasa {idx+1} | Chuo: {current_university}")
                
            tables = page.extract_tables(table_settings={"text_x_tolerance": 1.5})
            for table in tables:
                if not table or len(table) < 2:
                    continue
                    
                for row in table:
                    cleaned_row = [str(cell).strip() if cell else "" for cell in row]
                    if not cleaned_row or "Programme" in cleaned_row or "Requirements" in cleaned_row or "S/N" in cleaned_row:
                        continue
                        
                    sn = cleaned_row[0].replace('.', '').strip()
                    if sn.isdigit():
                        programme = cleaned_row[1]
                        code = cleaned_row[2]
                        reqs = cleaned_row[3]
                        duration = cleaned_row[-1] if len(cleaned_row) > 4 else ""
                        
                        all_raw_courses.append({
                            "UniversityHeader": current_university,
                            "Programme": programme,
                            "Code": code,
                            "Requirements": reqs,
                            "Duration": duration
                        })
                    elif all_raw_courses and len(cleaned_row) >= 4 and not sn:
                        # Continuation row (belongs to the last course)
                        if cleaned_row[1]:
                            all_raw_courses[-1]["Programme"] += "\n" + cleaned_row[1]
                        if cleaned_row[2]:
                            all_raw_courses[-1]["Code"] += " " + cleaned_row[2]
                        if cleaned_row[3]:
                            all_raw_courses[-1]["Requirements"] += "\n" + cleaned_row[3]
                            
            if (idx + 1) % 50 == 0:
                print(f"Kurasa {idx + 1} zimesomwa tayari...")
                
    print(f"\nJumla ya kozi zilizosomwa kabla ya usafi: {len(all_raw_courses)}")
    
    # Run shift cleaning
    print("Kusafisha na kupanga sifa za kujiunga (Requirements shift cleaning)...")
    cleaned_courses = clean_requirements_shift(all_raw_courses)
    
    # Map to final Excel format
    print("Tengeneza faili la Excel lenye safu zilizoombwa...")
    final_rows = []
    
    for c in cleaned_courses:
        header = c["UniversityHeader"]
        
        # Resolve names and columns
        raw_name = clean_header_name(header)
        jina_la_chuo = resolve_spaced_name(raw_name)
        mkoa = get_region(header)
        type_val = get_type(jina_la_chuo)
        umiliki = get_ownership(jina_la_chuo)
        
        course_name = c["Programme"].replace("\n", " ").strip()
        requirements = c["Requirements"].replace("\n", " ").strip()
        
        # Make sure spaces look good
        course_name = re.sub(r'\s+', ' ', course_name)
        requirements = re.sub(r'\s+', ' ', requirements)
        
        duration_val = c.get("Duration", "").replace("\n", " ").strip()
        duration_match = re.search(r'\d+', duration_val)
        duration_clean = duration_match.group(0) if duration_match else duration_val
        
        # If duration is empty or not in standard values (1 to 5), default to '3'
        if duration_clean not in ['1', '2', '3', '4', '5']:
            duration_clean = '3'
        
        final_rows.append({
            "Jina la chuo": jina_la_chuo,
            "Mkoa": mkoa,
            "Umiliki (private/government)": umiliki,
            "Courses": course_name,
            "Requirements": requirements,
            "Duration": duration_clean,
            "Type (university/institute)": type_val
        })
        
    df = pd.DataFrame(final_rows)
    
    # Save to Excel
    df.to_excel(output_excel, index=False)
    print(f"Kazi Imekamilika! Faili la Excel limehifadhiwa kama: {output_excel}")
    print(f"Jumla ya kozi zilizoandikwa kwenye Excel: {len(df)}")
    print(f"Jumla ya vyuo vilivyotambuliwa: {df['Jina la chuo'].nunique()}")

if __name__ == "__main__":
    run_extraction()
