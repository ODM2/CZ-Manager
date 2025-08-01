
import os
import pandas as pd

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
directory_path = './baddata/'
current_directory = os.getcwd()

# Print the current directory
print(f"The current working directory is: {current_directory}")
# List files in the specified directory
files = os.listdir(directory_path)
print('here')
# Print each file name

for file_name in files:
    print(file_name)
# Load the datasets
# grbulb_xls_path = "./baddata/GRBULB 2022 EMD uploadshort.xls"
# grbulb_csv_path = "./baddata/HHHRsensorsitesummaries.csv"
# grbulb_csv_path = "./baddata/GRBCRsensorsitesummaries.csv"
grbulb_csv_path = "./baddata/GRBORsensorsitesummaries.csv"

# Reading the Excel file
# grbulb_xls = pd.read_excel(grbulb_xls_path)

# Reading the CSV file
grbulb_csv = pd.read_csv(grbulb_csv_path, header=0, skiprows=[1])

# Displaying the first few rows of each dataset to understand their structure
# rbulb_xls.head(), grbulb_csv.head()


# Now that the Excel file has been provided as a CSV, let's load the new CSV file
grbulb_csv_path_upload = "./baddata/GRBOR_2019_EMD_upload.csv"

# Reading the newly provided CSV file
grbulb_csv_upload = pd.read_csv(grbulb_csv_path_upload)

# Displaying the first few rows of each dataset again to understand their structure


# Identifying matching columns based on 'variableEDM' in grbulb_csv
# First, let's create a mapping of 'variableEDM' to 'resultid' for easy lookup
variable_to_resultid = grbulb_csv.set_index('variableEDM')['resultid'].to_dict()

# Identifying matching columns again after correctly loading the CSV
# Initialize an empty list to hold the names of matching columns
# Revised approach based on the new understanding
matching_columns_dict = {}
resultid_to_col = {}  # Reverse mapping from resultid to column details

# Creating a dictionary to store matching columns and their respective resultid
for i, col in enumerate(grbulb_csv_upload.columns):
    if col in variable_to_resultid:
        resultid = variable_to_resultid[col]
        validation_column = None
        if i + 1 < len(grbulb_csv_upload.columns) and "RESULTS VALID" in grbulb_csv_upload.columns[i + 1]:
            validation_column = grbulb_csv_upload.columns[i + 1]
            print(f"Match found for {col} with resultid {resultid} and validation column {validation_column}")
        else:
            print(f"Match found for {col} with resultid {resultid}, but no adjacent 'RESULTS VALID' column.")

        # Update matching_columns_dict with column information
        matching_columns_dict[col] = {
            'resultid': resultid,
            'validation_column': validation_column
        }

        # Update reverse mapping
        # Note: This assumes a 1:1 mapping of resultid to columns. If one resultid can correspond to multiple columns,
        # you may want to store lists of columns under each resultid key instead.
        resultid_to_col[resultid] = {
            'column_name': col,
            'validation_column': validation_column
        }
# Now, matching_columns_dict contains the needed mappings and validation column info
# Initialize an empty DataFrame for filtered data
filtered_data = pd.DataFrame()
filtered_data_dict = {}
# Iterate through the matching_columns_dict to apply filters based on "RESULTS VALID" column
for col, info in matching_columns_dict.items():
    # Select all rows, but keep only the specified columns along with the validation column
    selected_columns = ['DATE', 'TIME', col]
    if info['validation_column']:
        selected_columns.append(info['validation_column'])
    df = grbulb_csv_upload[selected_columns].copy()

    # Add the resultid as a new column, with the same value for all rows
    df['resultid'] = info['resultid']
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'],
                                               format='%m/%d/%Y %H:%M:%S', errors='coerce')

    # Store this DataFrame in the dictionary using the resultid as the key
    filtered_data_dict[info['resultid']] = df

# Display the head of the filtered data
resultid_key = 79011  # Ensure this key matches the type used in your dictionary keys

if resultid_key in filtered_data_dict:
    df_to_save = filtered_data_dict[resultid_key]
    if 'DATE' in df_to_save.columns and 'TIME' in df_to_save.columns:
        # Combine 'DATE' and 'TIME' into 'DATETIME', assuming this operation is necessary before saving
        df_to_save.to_csv('./baddata/GRBOR_all2019_data.csv', index=False)
    else:
        print("'DATE' or 'TIME' column not found in DataFrame.")
else:
    print(f"Key {resultid_key} not found in filtered_data_dict.")

# Assuming 'filtered_data' is already defined and has 'DATE' and 'TIME' columns

qualitycodebad = CvQualitycode.objects.filter(name='Bad').get()
qualitycodeGood = CvQualitycode.objects.filter(name='Good').get()
# Not censored
censorercode = CvCensorcode.objects.filter(name='Not censored').get()
timeaaggunits = Units.objects.filter(unitsid=14).get()

error_log_path = './baddata/GRBGOR2019error_log.csv'
error_log = []  # To keep track of rows that don't meet the expected validation column values
i = 0
for resultid, df in filtered_data_dict.items():
    for index, row in df.iterrows():
        i +=1
        if i == 1:
            continue
        print(row)
        print(index)
        datetime = row['DATETIME']  # Assuming 'DATETIME' is already in your DataFrame
        col = resultid_to_col[resultid]['column_name']
        print(col)
        value = row[col]  # The column with your measurement value
        validation_col = resultid_to_col[resultid]['validation_column']
        validation_value = row[validation_col]  # Assuming this column exists in your DataFrame

        # Determine the quality code based on the validation column's value
        if validation_value == 'N':
            qualitycodecv = qualitycodebad
        elif validation_value == '' or pd.isna(validation_value):
            qualitycodecv = qualitycodeGood
        else:
            error_log.append((resultid, datetime, value, validation_value))
            continue  # Skip to the next iteration

        # The rest of your logic for retrieving or creating the database entry
        try:
            print(datetime, resultid, value)
            trv = Timeseriesresultvalues.objects.filter(
                resultid=resultid,
                valuedatetime=datetime,
                datavalue=value
            ).get()
            trv.qualitycodecv = qualitycodecv
            trv.timeaggregationinterval = 15
            trv.save()
        except ObjectDoesNotExist:
            # Insert the new record since it does not exist
            result = Timeseriesresults.objects.filter(resultid=resultid).get()
            Timeseriesresultvalues.objects.create(
                resultid=result,
                valuedatetime=datetime,
                datavalue=value,
                valuedatetimeutcoffset=-5,
                censorcodecv=censorercode,
                timeaggregationinterval=15,
                timeaggregationintervalunitsid=timeaaggunits,
                qualitycodecv=qualitycodecv
            ).save()
            print(f"Inserted new record for ResultID: {resultid}, DateTime: {datetime}, Value: {value}")

# Optionally, handle the error_log as needed

# Open the file for writing
with open(error_log_path, 'w') as file:
    # Write a header row (optional)
    file.write('ResultID,DateTime,Value,ValidationValue\n')

    # Iterate over the error log and write each entry
    for error in error_log:
        # Format the error log entry as a CSV row
        # Note: Assuming that none of the error components contain commas. If they do, you'll need to handle them accordingly (e.g., by quoting the fields).
        row = f"{error[0]},{error[1]},{error[2]},{error[3]}\n"
        file.write(row)

print(f"Error log written to {error_log_path}")
# database_entries.to_csv('./baddata/GRBGBW_all_datav2.csv', index=False)