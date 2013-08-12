"""
Run simulations using GAMS and vSPD.
Will make a number of assumptions about the data
"""

# Import the modules
import subprocess
import glob
import shutil
import os
import sys

# Define global variables of the simulations

GAMS_PATH = '/home/nigel/Gams/24.1/gams'
VSPD_FILE_PATH = '/home/nigel/data/vSPD_GDX'
YEAR = "2009"
VSPD_PATH = '/home/nigel/python/vSPD'
VSPD_PROGRAM_PATH = os.path.join(VSPD_PATH, 'Programs')
VSPD_PROGRAM_INPUT = os.path.join(VSPD_PATH, 'Input')
VSPD_PROGRAM_OUTPUT = os.path.join(VSPD_PATH, 'Output')

# Define the simulation global variables
RESULTS_DIR = os.path.join(VSPD_FILE_PATH, "output_results", YEAR)
INPUT_DIR = os.path.join(VSPD_FILE_PATH, "input_files", "Sample")
COMPLETE_DIR = os.path.join(VSPD_FILE_PATH, "completed_files", YEAR)

# Solver files
OVERRIDE_FILE = "VSPDSolve.gms.override"
ORIG_FILE = "VSPDSolve.gms.bak"
SOLVE_NAME = "VSPDSolve.gms"


def get_gdx_files(input_dir=INPUT_DIR):
    """ Get the GDX files from the input directory"""
    return glob.glob(os.path.join(input_dir, "*.gdx"))


def run_vSPD(gams_path=GAMS_PATH, prog_path=VSPD_PROGRAM_PATH):
    """
    Call vSPD, note it will do a little directory changing to make the
    subprocess.call command work. Bit of a pain.
    """
    cwd = os.getcwd()
    os.chdir(prog_path)
    cmd = ['/usr/bin/wine', gams_path, 'runVSPD.gms']
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr,
            env={"PATH": "/"})

    with open(os.path.join(prog_path, "FileNameList.inc"), 'rb') as f:
        fName = f.read()

    print("-"*78)
    print("vSPD run on %s completed" % fName)
    print("-"*78)

    os.chdir(cwd)


def rename_results(output=VSPD_PROGRAM_OUTPUT, defaultname="Test",
                   fName=None, runtype=None):
    """
    Rename the results directory away from the defaultname
    """

    # Get the Directory
    basefName, ext = os.path.splitext(os.path.basename(fName))
    directory = os.path.join(output, defaultname)
    new_directory = os.path.join(os.path.dirname(directory),
                '_'.join([basefName, runtype]))

    shutil.move(directory, new_directory)

    return new_directory


def move_results(directory_name, results_dir=RESULTS_DIR):
    """
    Move the results between
    """
    dst_dir = os.path.join(results_dir, os.path.basename(directory_name))
    shutil.move(directory_name, dst_dir)


def change_solve_file(override=True, prog_path=VSPD_PROGRAM_PATH):
    """
    Simple conditional statement to change the solve parameter used
    by overwriting a couple files
    """
    if override:
        shutil.copy(os.path.join(prog_path, OVERRIDE_FILE),
                    os.path.join(prog_path, SOLVE_NAME))
    else:
        shutil.copy(os.path.join(prog_path, ORIG_FILE),
                    os.path.join(prog_path, SOLVE_NAME))


def move_input_to_complete(fName, complete_dir=COMPLETE_DIR):
    """ Move the input file to the Compelte DIR so that it doesn't get
    run again
    """

    shutil.move(fName, complete_dir)


def update_file_paths(fName, prog_path=VSPD_PROGRAM_PATH):
    """
    Update the file which contains the GDX file names
    """

    sole_name, ext = os.path.splitext(os.path.basename(fName))
    with open(os.path.join(prog_path, "FileNameList.inc"), 'wb') as f:
        f.write(sole_name)


def move_input_to_vSPD(fName, input_path=VSPD_PROGRAM_INPUT):
    """
    Move the appropriate GDX file to the input directory of vSPD
    Prevents munging around with vSPD paths
    """

    dst = os.path.join(input_path, os.path.basename(fName))
    shutil.move(fName, dst)
    return dst



def run_simulations():
    """
    Runs the simulations using the specified global variables
    This will take a long time as it needs to make two passes per
    input file to conduct both the control and the over ride
    Spits out the results to the
    """

    # Get the input files
    gdx_files = get_gdx_files()

    # Iterate through the files
    for f in gdx_files:

        # Move the input to the appropriate directory
        gdx_file = move_input_to_vSPD(f)

        # Add it to the file paths
        update_file_paths(gdx_file)

        # Run the control simulations
        # Update the control solve file
        change_solve_file(override=False)

        # run vSPD
        run_vSPD()

        # Rename the results
        control_name = rename_results(fName=gdx_file, runtype="Control")
        move_results(control_name)


        # Run the over ride simulation
        # Update the override solve file
        change_solve_file(override=True)

        # run vSPD
        run_vSPD()

        # Rename the results
        override_name  = rename_results(fName=gdx_file, runtype="Override")
        move_results(override_name)

        # Clean up the input files
        move_input_to_complete(gdx_file)







