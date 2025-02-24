import geopandas as gpd
import pandas as pd
from tqdm import tqdm

def get_coord_sheetplanparcel(prop_path, gis_file='data/GIS-LAYERS/dls_parcels_geojson.geojson'):
    # Load the GIS data
    geo_data = gpd.read_file(gis_file)

    # Convert 'SHEET' column to string for safer comparison
    geo_data['SHEET'] = geo_data['SHEET'].astype(str)

    # Load the property data from the Excel file
    property_data = pd.read_excel(prop_path, sheet_name='preprocessed')

    # Initialize lists to store matched and unmatched data
    matched_rows = []
    unmatched_rows = []

    # Iterate through each row in the property data
    for index, row in tqdm(property_data.iterrows(), total=len(property_data)):
        # Split the Sheet_Plan column to get sheet and plan
        if isinstance(row['Sheet_Plan_v2'], str):
            sp_data = row['Sheet_Plan_v2'].split('/')
        else:
            # If not a string, treat it as a float/int with PLAN as the value and Sheet as 0
            sp_data = ['0', str(row['Sheet_Plan_v2'])]

        # Ensure sp_data has at least two elements; fill with '0' if not
        if len(sp_data) < 2:
            sp_data = ['0', '0']

        sheet = sp_data[0]
        plan = sp_data[1]
        parcel_nbr = str(row['Parcel'])

        # Filter the geo_data based on sheet, plan, and parcel_nbr
        filt_data = geo_data[
            (geo_data['PLANS'] == plan) &
            (geo_data['SHEET'] == sheet) #&  # No longer converting to int
            # (geo_data['PARCEL_NBR'].astype(str) == parcel_nbr)
        ]
        # print(plan, sheet)
        # print(filt_data)

        # Check if a match was found
        if not filt_data.empty:
            # Extract lat and lon from the matched row in geo_data
            lat = filt_data.iloc[0]['y']  # Assuming 'y' is the latitude column
            lon = filt_data.iloc[0]['x']  # Assuming 'x' is the longitude column

            # Append the matched row with lat and lon to the matched_rows list
            matched_row = row.to_dict()
            matched_row['lat'] = lat
            matched_row['lon'] = lon
            matched_rows.append(matched_row)
        else:
            # Append the unmatched row to the unmatched_rows list
            unmatched_rows.append(row.to_dict())

        # if index==10:
        #     break

    # Convert the matched and unmatched rows to DataFrames
    matched_df = pd.DataFrame(matched_rows)
    unmatched_df = pd.DataFrame(unmatched_rows)

    # Save the matched data to an Excel file
    if not matched_df.empty:
        matched_df.to_excel('src/temp/matched_data_v4.xlsx', index=False)
    else:
        print("No matched data found.")

    # Save the unmatched data to an Excel file
    if not unmatched_df.empty:
        unmatched_df.to_excel('src/temp/unmatched_data_v4.xlsx', index=False)
    else:
        print("No unmatched data found.")

    return matched_df, unmatched_df

if __name__ == '__main__':
    # Example usage
    prop_path = 'src/temp/unmatched_data_v3.xlsx'
    matched_data, unmatched_data = get_coord_sheetplanparcel(prop_path)
