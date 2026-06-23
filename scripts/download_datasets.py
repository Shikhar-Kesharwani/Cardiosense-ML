import os
import zipfile
import urllib.request
import pandas as pd

def download_and_process_brfss():
    print("Downloading raw BRFSS 2015 dataset from official CDC servers...")
    url = "https://www.cdc.gov/brfss/annual_data/2015/files/LLCP2015XPT.zip"
    zip_path = "Notebook_Experiments/Data/LLCP2015XPT.zip"
    
    if not os.path.exists(zip_path):
        urllib.request.urlretrieve(url, zip_path)
        print("Download complete.")
    else:
        print("Zip file already exists.")

    print("Unzipping...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("Notebook_Experiments/Data/")
    
    xpt_path = "Notebook_Experiments/Data/LLCP2015.XPT"
    if not os.path.exists(xpt_path):
        xpt_path = "Notebook_Experiments/Data/LLCP2015.xpt"
        
    print(f"Reading XPT file from {xpt_path}. This will consume a lot of RAM...")
    
    df = pd.read_sas(xpt_path)
    print(f"Original shape: {df.shape}")
    
    cols_to_keep = [
        '_MICHD', 'BPHIGH4', 'TOLDHI2', 'CHOLCHK', 'BMI5', 'SMOKE100', 'CVDSTRK3', 
        'DIABETE3', '_TOTINDA', '_FRTLT1', '_VEGLT1', '_RFDRHV4', 'HLTHPLN1', 
        'MEDCOST', 'GENHLTH', 'MENTHLTH', 'PHYSHLTH', 'DIFFWALK', 'SEX', '_AGEG5YR', 
        'EDUCA', 'INCOME2', 'SLEPTIM1', 'ASTHMA3', 'CHCSCNCR', 'CHCOCNCR', 'CHCCOPD1', 
        'HAVARTH3', 'ADDEPEV2', 'CHCKIDNY', 'DIABAGE2', 'WEIGHT2', 'HEIGHT3', 
        'ALCDAY5', 'EXERANY2', 'SEATBELT', 'FLUSHOT6', 'PNEUVAC3', 'HIVTST6', 
        'QSTVER', 'QSTLANG', '_STATE', 'MSCODE', 'MARITAL', 'VETERAN3', 'PREGNANT', 
        'DECIDE', 'DIFFALON'
    ]
    
    cols_available = [c for c in cols_to_keep if c in df.columns]
    df = df[cols_available]
    
    if '_MICHD' in df.columns:
        df['_MICHD'] = df['_MICHD'].replace(2.0, 0.0)
        df.rename(columns={'_MICHD': 'target'}, inplace=True)
    
    df = df.dropna(subset=['target'])
    df = df.dropna(thresh=len(df)*0.5, axis=1)
    df = df.fillna(df.median())
    
    print(f"Final shape after filtering: {df.shape}")
    df.to_csv("Notebook_Experiments/Data/brfss_full_processed.csv", index=False)
    print("Saved to Notebook_Experiments/Data/brfss_full_processed.csv")

if __name__ == "__main__":
    download_and_process_brfss()
