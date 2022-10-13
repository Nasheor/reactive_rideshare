# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------

# ------------------------------------------
# IMPORTS
# ------------------------------------------
import run_instance
#
import time
import os
import sys
import codecs
import shutil


# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_folder, output_folder):
    # 1. If the output folder already exists, we remove it and re-create it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We open a file called solution.csv for writing
    solution_csv_stream = codecs.open(output_folder + "solution.csv", "w", encoding="utf-8")

    list_of_files = os.listdir(input_folder)
    if (".DS_Store") in list_of_files:
        list_of_files.remove(".DS_Store")
    list_of_files.sort()



    # 4.3. We traverse the instances
    for file in list_of_files:
        # 4.3.1. We get the name of the input and output files
        input_file_name = input_folder + file
        output_file_name = output_folder + file

        # 4.3.2. We solve the instance
        num_trips_satisfied = run_instance.my_main(input_file_name, output_file_name)

        # 4.3.3. We write the result to the solution file
        my_str = input_file_name + ";" + str(num_trips_satisfied) + "\n"
        solution_csv_stream.write(my_str)

    # 5. close the solution.csv file
    solution_csv_stream.close()


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now its time to apply this knowledge.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer finally processes this PYTHON PROGRAM EXECUTION section, which:
# (i) Specifies the function F to be executed.
# (ii) Define any input parameter such this function F has to be called with.
#
# --------------------------------------------------------
if __name__ == '__main__':
    # 1. We get the name of the input and output folder
    input_folder = "./instance_generator/instances/"
    output_folder = "./output/"

    if (len(sys.argv) > 1):
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]

    # 2. We call to the function my_main
    start_time = time.time()

    my_main(input_folder, output_folder)

    total_time = time.time() - start_time
    print("Total time = " + str(total_time))
