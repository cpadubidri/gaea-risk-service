import requests
import pandas as pd
from tqdm import tqdm

def get_lat_lon_from_pincode(pincode, country="Cyprus", API_KEY="AIzaSyBeobPO1mYVi1R1f4UKpitzyepPQmRBdgE"):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    # Build the query using the pincode and country
    query = f"{pincode}, {country}"
    params = {
        "address": query,
        "key": API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            # Extract latitude and longitude from the first result
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"API Response: {data}")  # Debug: print full response details
            print(f"Error: {data['status']}. No results found for the pincode.")
            return None, None
    except Exception as e:
        print("Error during API call:", e)
        return None, None

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
    # Load the request data
    request_data = pd.read_excel(filepath, sheet_name="locations")

    # Prepare an empty list to store rows for the new DataFrame
    results = []
    for index, row in tqdm(request_data.iterrows(), total= len(request_data)):
        results_row = {}

        # print(f"Processing Postal Code: {row['Postal Codes:']}")

        if type(row['Postal Code/ Location'])!="str":
            lat, lon = get_lat_lon_from_pincode(row['Postal Code/ Location'])
            if lat!="None":
                # print(lat, lon)
                # Add the original row data, extracted columns, and coordinates
                results_row['Postal Code/ Location'] = row['Postal Code/ Location']
                results_row['Latitude'] = lat
                results_row['Longitude'] = lon
            else:
                print(f"No community found for Postal Code: {row['Postal Code/ Location']}")
                results_row['Postal Code/ Location'] = row['Postal Code/ Location']
                results_row['Latitude'] = "None"
                results_row['Longitude'] = "None"
        else:
            lat, lon = get_lat_lon_from_community(row['Postal Code/ Location'])
            if lat!="None":
                # print(lat, lon)
                # Add the original row data, extracted columns, and coordinates
                results_row['Postal Code/ Location'] = row['Postal Code/ Location']
                results_row['Latitude'] = lat
                results_row['Longitude'] = lon
            else:
                print(f"No community found for Postal Code: {row['Postal Code/ Location']}")
                results_row['Postal Code/ Location'] = row['Postal Code/ Location']
                results_row['Latitude'] = "None"
                results_row['Longitude'] = "None"
        
        results.append(results_row)
        
        # if index==10:
        #     break

    # Create a new DataFrame from the results
    results_df = pd.DataFrame(results)
    print(results_df)
    # Save the results to an Excel file
    output_filepath = '/home/cpp/SUPER-NAS/USERS/Chirag/PROJECTS/202501-EY-Bank/src/temp/PhysicalRiskUniquePostalCodesAddresses_issue_NEWVERSION_latlon.xlsx'
    results_df.to_excel(output_filepath, index=False)
    print(f"Results saved to {output_filepath}")


if __name__ == "__main__":
    get_lat_lon('/home/cpp/SUPER-NAS/USERS/Chirag/PROJECTS/202501-EY-Bank/data/prperty-data_v2/PhysicalRiskUniquePostalCodesAddresses_issue_NEWVERSION.xlsx')
