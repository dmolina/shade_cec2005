#!/usr/bin/python
from __future__ import print_function
import sys
from os.path import isfile
import argparse

parser = argparse.ArgumentParser(description="Prepare the config file for run in server")

parser.add_argument("-n", required=True, type=str, dest="name", help='Name')
parser.add_argument("-e", required=True, type=str, dest="filename", help='Executable name')
parser.add_argument("-o", dest="output", help='Output name')
 
args = parser.parse_args()

runfile = args.filename

if not isfile(runfile):
    parser.print_help()
    sys.exit(1)

if args.output:
    output = open(args.output, 'w')
else:
    output = sys.stdout

name = args.name

funs = range(1, 25+1)
seeds = range(1, 6)
dims = [10, 30, 50]
dims = [50]
nrun = 5
total = len(funs)*len(dims)*len(seeds)
print("""\
#!/bin/bash
#
#SBATCH -J {name}
#SBATCH -o out_{name}.txt
#SBATCH -e err_{name}.txt
#SBATCH -a 1-{total}\

""".format(name=args.name, total=total), file=output)

count = 1

for fun in funs:
	for dim in dims:
		for seed in seeds:
			print("PARAMS[{0}]=\"-f {1} -d {2} -s {3} -r {4}\"".format(count, fun, dim, seed, nrun), file=output)
			count += 1


algname = './' +runfile
print(algname +' ${PARAMS[$SLURM_ARRAY_TASK_ID]}' +"\n", file=output)
#print("wait", file=output)
output.close()
