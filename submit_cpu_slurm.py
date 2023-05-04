import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-py", "--py_func", required=True, type=str)
parser.add_argument("-y", "--years", required=True, type=str, nargs="+")
parser.add_argument("-v", "--variable", type=str)
args = parser.parse_args()
variable_name = None
variable_value = None
if args.variable:
    variable_name = args.variable.split("=")[0]
    variable_value = args.variable.split("=")[1]

job_prefix = args.py_func.split(".")[0]
# write sh file
for year in args.years:
    filename=f"{job_prefix}-{year}"
    with open(f"./{filename}.sh", "w") as f:
        if not variable_value:
            f.write(
                f"""#!/bin/bash
    #echo "Activating huggingface environment"
    #source /share/apps/anaconda3/2021.05/bin/activate huggingface
    echo "Beginning script"
    cd /share/luxlab/reddit
    python3 {args.py_func} --t C --start-year {year} --end-year {year}
                """
            )
        else:
            f.write(
                f"""#!/bin/bash
                #echo "Activating huggingface environment"
                #source /share/apps/anaconda3/2021.05/bin/activate huggingface
                echo "Beginning script"
    		cd /share/luxlab/reddit
    		python3 {args.py_func} --t C --start-year {year} --end-year {year} --{variable_name} {variable_value}
                            """
        )

    with open(f"./{filename}.sub", "w") as f:
        f.write(
            f"""#!/bin/bash
#SBATCH -J {filename}                            # Job name
#SBATCH -o /share/luxlab/reddit/logs/{filename}_%j.out # output file (%j expands to jobID)
#SBATCH -e /share/luxlab/reddit/logs/{filename}_%j.err # error log file (%j expands to jobID)
#SBATCH --mail-type=ALL                        # Request status by email
#SBATCH --mail-user=aww66@cornell.edu          # Email address to send results to.
#SBATCH -N 1                                   # Total number of nodes requested
#SBATCH -n 4                                  # Total number of cores requested
#SBATCH --get-user-env                         # retrieve the users login environment
#SBATCH --mem=50G                             # server memory requested (per node)
#SBATCH -t 20:00:00                            # Time limit (hh:mm:ss)
#SBATCH --partition=default_partition          # Request partition
/share/luxlab/reddit/{filename}.sh
            """
        )
    os.system(f"chmod 775 {filename}.sh")
    os.system(f"sbatch --requeue {filename}.sub")