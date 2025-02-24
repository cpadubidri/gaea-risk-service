import requests
import pandas as pd
from tqdm import tqdm

def get_lat_lon_from_community(community_name, country="Cyprus", API_KEY="AIzaSyBeobPO1mYVi1R1f4UKpitzyepPQmRBdgE"):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    # Include the country to help narrow down results
    query = f"{community_name}, {country}"
    params = {
        "address": query,
        "key": API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            # Extract latitude and longitude
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"API Response: {data}")  # Debug the full response
            print(f"Error: {data['status']}. No results found for the community.")
            return None, None
    except Exception as e:
        print("Error during API call:", e)
        return None, None


def get_lat_lon(filepath):
    # Load the postal codes data
    pincode_data = pd.read_excel('/home/cpp/SUPER-NAS/USERS/Chirag/PROJECTS/202501-EY-Bank/data/GIS-LAYERS/postal_codes_v2.xlsx')

    # print(pincode_data)
    # Load the request data
    request_data = pd.read_excel(filepath, sheet_name="locations")

    # Prepare an empty list to store rows for the new DataFrame
    results = []

    for index, row in tqdm(request_data.iterrows(), total= len(request_data)):
        # print(f"Processing Postal Code: {row['Postal Codes:']}")
        print(row)
        # Find the community name for the given postal code
        if type(row['Postal Code/ Location'])!="str":
            community_info = pincode_data[pincode_data['Ταχυδρομικός Κώδικας / Postal Code'] == row['Postal Code/ Location']]
        # else:

        print(community_info)

        
        if not community_info.empty:
            com_name = community_info['Municipality / Community'].values[0]
            # print(f"Found Community: {com_name}")
            
            # Get latitude and longitude
            lat, lon = get_lat_lon_from_community(com_name)
            # print(f"Coordinates: {lat}, {lon}")
            
            # Extract relevant columns from `pincode_data`
            extracted_data = {
                'Municipality / Community': community_info['Municipality / Community'].values[0],
                'District': community_info['District'].values[0] if 'District' in community_info else None,
                'Postal Service through Post Office/Postal Agency': community_info['Postal Service through Post Office/Postal Agency'].values[0] if 'Postal Service through Post Office/Postal Agency' in community_info else None,
            }

            # Add the original row data, extracted columns, and coordinates
            result_row = row.to_dict()
            result_row.update(extracted_data)
            result_row['Latitude'] = lat
            result_row['Longitude'] = lon
            results.append(result_row)
        else:
            print(f"No community found for Postal Code: {row['Postal Codes:']}")
        
        if index==2:
            break

    # Create a new DataFrame from the results
    results_df = pd.DataFrame(results)
    print(results_df)
    # # Save the results to an Excel file
    # output_filepath = '/home/cpp/SUPER-NAS/USERS/Chirag/PROJECTS/202501-EY-Bank/src/temp/PhysicalRiskUniquePostalCodesAddresses_issue_NEWVERSION_latlon.xlsx'
    # results_df.to_excel(output_filepath, index=False)
    # print(f"Results saved to {output_filepath}")


if __name__ == "__main__":
    get_lat_lon('/home/cpp/SUPER-NAS/USERS/Chirag/PROJECTS/202501-EY-Bank/data/prperty-data_v2/PhysicalRiskUniquePostalCodesAddresses_issue_NEWVERSION.xlsx')
