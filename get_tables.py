"""
usage: get_tables.py <file>

This program generates a csv files with the fitness and evaluations of
the algorithm indicated into the file name. The file must exist, and
it should contains the string 'F<fun>D<dim>' the fun is only required
for commodity, the program extract the results for all functions.
"""
import pandas as pd
import numpy as np
import subprocess
from docopt import docopt
import glob
import sys
import io
import os
import re
arguments = docopt(__doc__, version='Get tables 1.0')
ftemplate = arguments['<file>']
regexp = re.search(r'F(\d+).*', ftemplate, re.IGNORECASE)

if regexp:
    ftemplate = ftemplate.replace('F' + regexp.groups()[0], '*', 1)
    ftemplate = ftemplate.replace('f' + regexp.groups()[0], '*', 1)
else:
    sys.exit("Error, file name must contains the expression F<number>")

regexp_dir = re.search(r'D(\d+)(.*)', arguments['<file>'], re.IGNORECASE)
dim = 0

if regexp_dir:
    dim = regexp_dir.groups()[0]
else:
    sys.exit("Error, file name must contains the expression D<dimension>")

alg = os.path.basename(ftemplate[:regexp.start()])
alg = alg.rstrip('_')
foutput = "{}_d{}_fitness.csv".format(alg, dim)

if os.path.exists(foutput):
    sys.exit(0)

print(ftemplate)
fnames = glob.glob(ftemplate)
fitness = pd.DataFrame()
current = pd.DataFrame()
print(fnames)

# Sort one frame by each name
def sortFrame(df):
    """Sort the dataframe by its second value."""
    return df.reindex_axis(sorted(df.columns, key=lambda x: int(x[1:])), axis=1)

for fname in fnames:
    exp = re.match(".*F(\d+)D{}.*".format(dim), fname, re.IGNORECASE)

    if not exp:
        msg = "Error:file name %s must contains the expression F<function>D<dimension>" % fname
        print(msg)
        continue

    (fun) = exp.group(1)
#    assert dim2==dim
    fun_str = 'f{}'.format(fun)
    # Read the values
    proc = subprocess.Popen(["cut", "-d:", "-f2", fname], stdout=subprocess.PIPE)

    (values, err) = proc.communicate()
    # Create a frame with the output
    frame = pd.read_csv(io.BytesIO(values), skipinitialspace=True,
                        names=['fitness', 'evals'])

    # Ignoring values lower than 1e-8
    frame.fitness = frame.fitness.clip(lower=1e-8)

    # Check that all run obtains the optimum
    found = np.all(frame.fitness <= 1e-8)
    runs = len(frame)

    # If found is obtained it
    if found:
        fitness[fun_str] = frame.fitness
        current[fun_str] = frame.evals
    else:
        fitness[fun_str] = frame.fitness
        current[fun_str] = frame.evals

# Sort the frame
fitness = sortFrame(fitness)
current = sortFrame(current)
fitness.to_csv("{}_d{}_fitness.csv".format(alg, dim),
               header=True, sep=' ',
               index=False)

current.to_csv("{}_d{}_eval.csv".format(alg, dim), header=True, sep=' ',
               index=False)

print "{}_d{} csv files (fitness and eval) created".format(alg, dim)
