import requests
import pandas as pd
import json
from tqdm import tqdm

URL = 'http://10.0.10.25:5000/v2.0/'
SERVICES = ['wildfire-risk', 'flooding-risk', 'subsidence-risk', 'landslides-risk', 'Seismic-Zone']

def get_risk_data(coord, url=URL, services=SERVICES):
    params = {
        "lat": coord[0],
        "lon": coord[1]
    }
    risk_data = {}
    
    for service in services:
        # print(f"Fetching data for: {service}")
        response = requests.get(url=f"{url}/{service}", params=params)
        
        try:
            response_txt = json.loads(response.text)  # Using json.loads to safely parse response
        except json.JSONDecodeError:
            print(f"Error decoding JSON for {service}, setting default values.")
            response_txt = {}
        
        for key, value in response_txt.items():
            if key != "Coordinates":  # Ignoring Coordinates as requested
                risk_data[f"{service}_{key}"] = value if value is not None else 'N/A'  # Handling null values
    
    return risk_data

def process_risk(property_filepath, output_filepath):
    prop_data = pd.read_excel(property_filepath)
    
    risk_scores = []
    for index, row in tqdm(prop_data.iterrows(), total=len(prop_data)):
        # print((row['Latitude'], row['Longitude']))
        risk_data = get_risk_data((row['Latitude'], row['Longitude']))
        risk_scores.append(risk_data)
        # break
    
    risk_df = pd.DataFrame(risk_scores)
    prop_data = pd.concat([prop_data, risk_df], axis=1)
    
    prop_data.to_excel(output_filepath, index=False)
    print(f"Data saved to {output_filepath}")

if __name__ == "__main__":
    file_path = 'src/temp/PhysicalRiskUniquePostalCodesAddresses_issue_NEWVERSION_latlon.xlsx' 
    output_file = 'src/temp/PhysicalRiskUniquePostalCodesAddresses_issue_NEWVERSION_risk.xlsx'
    process_risk(file_path, output_file)
