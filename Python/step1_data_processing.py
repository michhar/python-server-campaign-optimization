"""

Campaign optimization step 1

Prerequisites:
  - SQL Server 2017 with Python Services installed
  - SQL Server Management Studio
  - A database created called 'Campaign' (use SSMS to create)
  - Visual Studio 2015/2017 or Visual Studio Code or similar code editor
  - Python path or Path env variables set to Python Services python or
      a virtual environment with Python Services python version
      (set system Path variable and add to Visual Studio Python
      Environments or create a virtual environment on the command line
      with 'virtualenv <python version path>' and 'activate' to begin using)
  - Command line or equivalent access

What these scripts do:
* Reads data into dataframe
* Imports dataframe to SQL Server Campaign database
* Processes in-database with revoscalepy stats and ML methods
* Report metrics
* Visualize with Python plotting tools

Micheleen Harris
"""

from revoscalepy.computecontext.RxComputeContext import  RxComputeContext
from revoscalepy.computecontext.RxInSqlServer import RxSqlServerData, RxInSqlServer
from revoscalepy.etl.RxImport import rx_import_datasource
# from revoscalepy.etl.RxImport import RxDataSource
from revoscalepy.functions.RxDataStep import rx_data_step_ex

from config import CONNECTION_STRING, BASE_DIR, LOCAL
import os
import pandas as pd

# The following is simple proof of concept and will be 
#   refactored into functions for release

computeContext = RxInSqlServer(
    connectionString = CONNECTION_STRING,
    numTasks = 1,
    autoCleanup = False
    )

# Create the file path to the csv data
file_path = os.path.join(BASE_DIR, 'Data')

# Read in data into a pandas df from a file
# TODO:  look into dask for holding chunks of data for import
campaign_detail_df = pd.read_csv(os.path.join(file_path, 'Campaign_Detail.csv'))

# Create table in SQL server
print("Creating tables...")
Campaign_Detail = RxSqlServerData(table = "Campaign_Detail", connectionString = CONNECTION_STRING)

# Read data into the SQL server table just created
print("Reading data into tables...")

# This is not working unfortunately
#help(RxDataSource)
#data = RxDataSource(open(os.path.join(file_path, 'Campaign_Detail.csv'), 'r'))

# The method rx_import_datasource expects a pandas df or an 
#   RxDataSource object
rx_import_datasource(inData=campaign_detail_df, \
    outFile=Campaign_Detail, overwrite=True)
# NB: overwrite param not accepting bool values!