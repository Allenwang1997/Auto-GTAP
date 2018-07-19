__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-7-19"

import os
from AutoGTAP.ImportCSV_SL4.ImportCsvSl4 import ImportCsvSl4
from AutoGTAP.ModifyDatabase.ModifyDatabase import ModifyDatabase
from AutoGTAP.ExportDictionary.ExportDictionary import ExportDictionary
from AutoGTAP.CreateOutput.CreateOutput import CreateOutput


class ExportResults(object):
    """Runs the GTAP model itself"""

    __slots__ = ["config"]

    def __init__(self, config) -> None:
        # Import simulation results into a single database
        old_work_directory = os.getcwd()
        os.chdir("WorkFiles")
        # load the various CSV files created by the experiment simulation into a database
        databaseSL4 = ImportCsvSl4(config.csv_paths()).create()
        # Modify the database to make it more readable
        databaseMod = ModifyDatabase(databaseSL4).create()
        # Export the database to a results csv file
        ExportDictionary("Results.csv", databaseMod)
        # Copy results.csv to the OutputFiles directory, and rename it with a timestamp
        os.chdir(old_work_directory)
        CreateOutput()
