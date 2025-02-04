### GAEA Risk Service


#### Folder structure 

    gis_service_project/
    │── src/                        # Main source code
    │   │── api/                    # API handling (requests, responses)
    │   │   │── __init__.py
    │   │   │── client.py           # Handles API calls to web server
    │   │   
    │   │── core/                   # Core functionality of the project
    │   │   │── __init__.py
    │   │   │── gis_search.py       # Handles GIS database search logic
    │   │   │── location_parser.py  # Extracts address/location details
    │   │── data/                   # Data handling (reading, writing)
    │   │   │── __init__.py
    │   │   │── file_handler.py     # Reads/Writes data to/from input files
    │   │   │── preprocess.py       # Preprocesses input files (future-proofing)
    │   │── utils/                  # Utility functions/helpers
    │   │   │── __init__.py
    │   │   
    │── data/                       # Sample input/output data (ignored in version control)
    │   │── <datafolders>
    │── requirements.txt            # Dependencies
    │── .gitignore                  # Ignore unnecessary files
    │── README.md                   # Project documentation
    │── main.py                      # Entry point for the application
