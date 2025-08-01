
import os

from django.core.wsgi import get_wsgi_application
# sys.path.append(r"C:\Users\ml1451\OneDrive - USNH\CZ-Manager")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
# os.environ['DJANGO_SETTINGS_MODULE'] = 'templatesAndSettings.settings.developmentPREP10'
# module_name = './templatesAndSettings.settings.developmentPREP10'
# special_module = importlib.import_module(module_name)

application = get_wsgi_application()
import numpy as np

from django.core.exceptions import ObjectDoesNotExist
import datetime
from odm2admin.models import *

# from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from django.contrib.auth.models import User
# C:\Users\12672\Box\PREPDataShare\PREP_NHDES\dataFromEMD\FirstReports\Lamprey
from multiprocessing import Process

# tsrvs = Timeseriesresultvalues.objects.filter(resultid=18673)

import pandas as pd

####### GRBSQ didn't work!! ########
####### GRBSQ didn't work!! ########

# Load the datasets
# grbulb_xls_path = "./baddata/GRBULB 2022 EMD uploadshort.xls"
grbulb_csv_path = "./baddata/GRBUPRsensorsitesummaries.csv"
# grbulb_csv_path = "./baddata/GRBCRsensorsitesummaries.csv"
# grbulb_csv_path = "./baddata/GRBGBWsensorsitesummaries.csv"

# Reading the Excel file
# grbulb_xls = pd.read_excel(grbulb_xls_path)

# Reading the CSV file
grbulb_csv = pd.read_csv(grbulb_csv_path, header=0, skiprows=[1])

# Displaying the first few rows of each dataset to understand their structure
# rbulb_xls.head(), grbulb_csv.head()


# Now that the Excel file has been provided as a CSV, let's load the new CSV file
grbulb_csv_path_upload = "./baddata/GRBUPR 2022 EMD Upload.csv"

# Reading the newly provided CSV file
grbulb_csv_upload = pd.read_csv(grbulb_csv_path_upload)

# Displaying the first few rows of each dataset again to understand their structure


# Identifying matching columns based on 'variableEDM' in grbulb_csv
# First, let's create a mapping of 'variableEDM' to 'resultid' for easy lookup
variable_to_resultid = grbulb_csv.set_index('variableEDM')['resultid'].to_dict()

# Identifying matching columns again after correctly loading the CSV
# Initialize an empty list to hold the names of matching columns
# Revised approach based on the new understanding

# Creating a dictionary to store matching columns and their respective resultid
matching_columns_dict = {}

# Iterate over the columns in the corrected upload CSV
for i, col in enumerate(grbulb_csv_upload.columns):
    # Check if the column name is in the variable_to_resultid mapping
    if col in variable_to_resultid:
        # Attempt to get the next column as the "RESULTS VALID" column
        # Need to check if the next column actually exists and is a "RESULTS VALID" column
        if i + 1 < len(grbulb_csv_upload.columns) and "RESULTS VALID" in grbulb_csv_upload.columns[i + 1]:
            # Store the column and its associated resultid in the dictionary
            # Also include the next column which is assumed to be the "RESULTS VALID" column
            matching_columns_dict[col] = {
                'resultid': variable_to_resultid[col],
                'validation_column': grbulb_csv_upload.columns[i + 1]
            }
            # Print for debugging
            print(f"Match found for {col} with resultid {variable_to_resultid[col]} and validation column {grbulb_csv_upload.columns[i + 1]}")
        else:
            # If there is no valid next column or it's not a "RESULTS VALID" column, just add the column with its resultid
            # This handles cases where we might not have a corresponding "RESULTS VALID" column right next to it
            matching_columns_dict[col] = {
                'resultid': variable_to_resultid[col],
                'validation_column': None
            }
            # Print for debugging
            print(f"Match found for {col} with resultid {variable_to_resultid[col]}, but no adjacent 'RESULTS VALID' column.")

# Now, matching_columns_dict contains the needed mappings and validation column info
# Initialize an empty DataFrame for filtered data
filtered_data = pd.DataFrame()

# Iterate through the matching_columns_dict to apply filters based on "RESULTS VALID" column
for col, info in matching_columns_dict.items():
    # Check if there's a validation column for the current data column
    if info['validation_column']:
        # Filter rows where the validation column is 'N'
        valid_rows = grbulb_csv_upload[info['validation_column']] == 'N'
        # If there are any valid rows, select them along with the DATE, TIME, and current column
        if valid_rows.any():
            # If filtered_data is empty, initialize it with the filtered rows
            if filtered_data.empty:
                filtered_data = grbulb_csv_upload.loc[valid_rows, ['DATE', 'TIME', col]].copy()
                # Add a column for the resultid
                filtered_data[f"{col} resultid"] = info['resultid']
            else:
                # If filtered_data is not empty, add only the new column for the current filter
                filtered_data.loc[valid_rows, col] = grbulb_csv_upload.loc[valid_rows, col]
                # Add a column for the resultid if it doesn't already exist
                if f"{col} resultid" not in filtered_data.columns:
                    filtered_data.loc[valid_rows, f"{col} resultid"] = info['resultid']

# Note: This code assumes you want to retain rows where ANY of the "RESULTS VALID" checks is 'N'.
# If you need to handle it differently, adjust the logic accordingly.

# Display the head of the filtered data
print(filtered_data.head())
filtered_data.to_csv('./baddata/GRBUPR_filtered_data.csv', index=False)

import pandas as pd

# Assuming 'filtered_data' is already defined and has 'DATE' and 'TIME' columns

# Convert 'DATE' and 'TIME' into a single datetime column
filtered_data['DATETIME'] = pd.to_datetime(filtered_data['DATE'] + ' ' + filtered_data['TIME'])

# Prepare a list to hold tuples of (datetime, resultid, value) for database operation
database_entries = []

# Iterate through each row in the filtered data
for index, row in filtered_data.iterrows():
    # For each column that represents a data value and has an associated resultid
    for col in matching_columns_dict.keys():
        if col in filtered_data.columns:
            # Extract the datetime, resultid, and value
            datetime = row['DATETIME']
            resultid = row[f"{col} resultid"]
            value = row[col]

            # Append the tuple to the list for database operation
            database_entries.append((datetime, resultid, value))
# Iterate through each row in the filtered data
qualitycodebad = CvQualitycode.objects.filter(name='Bad').get()
qualitycodeGood = CvQualitycode.objects.filter(name='Good').get()

for datetime, resultid, value in database_entries:
    if np.isnan(resultid):
        print(f"Skipping due to NaN ResultID for DateTime: {datetime}, Value: {value}")
        continue  # Skip to the next iteration

    try:
        # Attempt to retrieve the record
        print(datetime, resultid, value)
        trv = Timeseriesresultvalues.objects.filter(
            resultid=resultid,
            valuedatetime=datetime,
            datavalue=value
        ).get()
        trv.qualitycodecv = qualitycodebad
        trv.save()
        # If the record is found, you can proceed with your logic
        # For example, you might want to update the record or simply note that it exists
        # print("Record found:", trv)

    except ObjectDoesNotExist:
        # If the record does not exist, print a message to the console
        print(f"Record not found for ResultID: {resultid}, DateTime: {datetime}, Value: {value}")

print("done ", grbulb_csv_path)