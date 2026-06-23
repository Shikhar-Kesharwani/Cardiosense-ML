import zipfile
import os
import pandas as pd

zip_path = r'C:\Users\HP\Downloads\Compressed\archive_3.zip'
extract_path = 'Notebook_Experiments/Data/nhanes_100k/'

os.makedirs(extract_path, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    files_to_extract = ['demographics_clean.csv', 'questionnaire_clean.csv', 'chemicals_clean.csv', 'response_clean.csv', 'dictionary_nhanes.csv']
    for file in files_to_extract:
        if file in zip_ref.namelist():
            zip_ref.extract(file, extract_path)

print('Extracted specific files.')

demo = pd.read_csv(extract_path + 'demographics_clean.csv')
quest = pd.read_csv(extract_path + 'questionnaire_clean.csv')

# Look for lab data
if os.path.exists(extract_path + 'chemicals_clean.csv'):
    chem = pd.read_csv(extract_path + 'chemicals_clean.csv')
    print("Chemicals cols:", len(chem.columns))
else:
    print("No chemicals file.")
    
if os.path.exists(extract_path + 'response_clean.csv'):
    resp = pd.read_csv(extract_path + 'response_clean.csv')
    print("Response cols:", len(resp.columns))

print('Demographic cols:', len(demo.columns), 'Rows:', len(demo))
print('Quest cols:', len(quest.columns), 'Rows:', len(quest))

print("Demo columns:", demo.columns.tolist()[:20])
print("Quest columns:", quest.columns.tolist()[:20])
