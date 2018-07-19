import os
import subprocess
# noinspection PyPep8Naming
import AutoGTAP as ag

# Call Methods
# Load config files that will control program
config = ag.CreateConfig("config.yaml")
# Delete working files directory
ag.CleanWorkFiles()
# For each simulation, perform the different subparts (data aggregation, splitting,
# experiment simulation, etc) that make up that simulation
for simulation_name in config.simulation_list:
    # Add one to final range so that python will run the last part too
    for part_num in range(1, config.num_parts(simulation_name) + 1):

        # Load configuration information for this particular part
        part_type = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["type"]
        part_input_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["input_folder"]
        part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["work_folder"]

        # Copy input files for this part to the appropriate work directory
        ag.CopyInputFiles(config, simulation_name, part_num).copy()

        # Copy Work files from the previous part to the work directory for this part, unless this is the first part
        if part_num != 1:
            ag.MoveFilesBetweenSteps(config, simulation_name, part_num)

        # Run the actual work for this part, depending on which type of part it is
        if part_type == "GTPAg2":
            ag.AggregateModelData(config, simulation_name, part_num)

        elif part_type == "MSplitCom-Exe":
            ag.SplitCommodities(simulation_name)

        elif part_type == "modify_har":
            # Modify_HAR directly modifies a HAR file
            # This module should be rarely used
            parameter_mod_description = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "parameter_mod_description"]
            parameter_modification_list = config.yaml_file["parameter_modifications"][parameter_mod_description]
            old_work_directory = os.getcwd()
            os.chdir("WorkFiles\\{0}\\{1}".format(simulation_name, part_work_folder))
            ag.ModifyHAR("olddefault", "default", parameter_modification_list)
            os.rename("default.prm", "olddefault.har")
            subprocess.call("modhar -sti cmd_modify_har.sti")
            os.chdir(old_work_directory)

        elif part_type == "GTPVEW-V6" or part_type == "Shocks-V6":
            model_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["model_file_name"]
            cmf_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["cmf_file_name"]
            work_directory = "WorkFiles\\{0}\\{1}".format(simulation_name, part_work_folder)

            part_sim_environment = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "sim_environment"]

            old_work_directory = os.getcwd()
            os.chdir(work_directory)
            if part_sim_environment == "gemsim":
                # Create GSS and GST files for shocks and model gemsim
                subprocess.call("tablo -sti {0}.sti".format(model_file_name))
                subprocess.call("gemsim -cmf {0}.cmf".format(cmf_file_name))
            if part_sim_environment == "fortran":
                subprocess.call("{0} -cmf {1}.cmf".format(model_file_name, cmf_file_name))
            os.chdir(old_work_directory)

        elif part_type == "GTAP-Adjust":
            # Load additional configuration information specific to GTAP simulations
            part_shock = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["shock"]

            ag.GTAPAdjustCMF(simulation_name, part_work_folder, part_shock)

            # Change working directory to WorkFiles so all output (and logs)
            # will go there when gemsim or sltoht is called
            work_directory = "WorkFiles\\{0}\\{1}".format(simulation_name, part_work_folder)
            old_work_directory = os.getcwd()
            os.chdir(work_directory)
            subprocess.call("adjust.bat")
            os.chdir(old_work_directory)

        elif part_type == "GTAP-V6" or part_type == "GTAP-E":
            # Load additional configuration information specific to GTAP simulations
            part_shock = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["shock"]
            part_solution_method = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "solution_method"]
            model_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["model_file_name"]
            map_variables = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["map"]

            work_directory = "WorkFiles/{0}/{1}".format(simulation_name, part_work_folder)
            ag.SimulationCMF(work_directory, simulation_name, part_solution_method, part_work_folder, part_shock,
                             part_type)

            part_sim_environment = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "sim_environment"]
            old_work_directory = os.getcwd()
            os.chdir(work_directory)
            if part_sim_environment == "gemsim":
                # Create GSS and GST files for shocks and model gemsim
                subprocess.call("tablo -sti {0}.sti".format(model_file_name))
                subprocess.call("gemsim -cmf {0}.cmf".format(model_file_name))
            if part_sim_environment == "fortran":
                subprocess.call("{0} -cmf {0}.cmf".format(model_file_name))
            os.chdir(old_work_directory)

            # Use SLtoHT export the results of the simulation from sl4 to a CSV file
            ag.CreateMAP(work_directory, "sim", simulation_name,
                         map_variables)  # Map file determines which variables to export
            ag.CreateSTI(work_directory, model_file_name, simulation_name,
                         "sltoht")  # STI file controls running of sltoht
            old_work_directory = os.getcwd()
            os.chdir(work_directory)
            subprocess.call("sltoht -sti {0}_sltoht.sti".format(model_file_name))
            os.chdir(old_work_directory)

        else:
            raise ValueError('Unexpected part type: %s' % part_type)

# Import simulation results into a single database
old_work_directory = os.getcwd()
os.chdir("WorkFiles")
# load the various CSV files created by the experiment simulation into a database
databaseSL4 = ag.ImportCsvSl4(config.csv_paths()).create()
# Modify the database to make it more readable
databaseMod = ag.ModifyDatabase(databaseSL4).create()
# Export the database to a results csv file
ag.ExportDictionary("Results.csv", databaseMod)
# Copy results.csv to the OutputFiles directory, and rename it with a timestamp
os.chdir(old_work_directory)
ag.CreateOutput()
