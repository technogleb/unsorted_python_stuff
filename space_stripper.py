"""Just a simple CLI script that replaces all space sequences in each line of a file
with a separator provided (defaults to tab).
Can be handy in parsing output of GNU tools such as ps aux or top command for example.
"""

import sys
import os
import re
import subprocess
import argparse


def replace_spaces(line, sep='\t'):
	line_new = line
	idxs = [match_obj.span() for match_obj in re.finditer(r"[^\S\n\t]+", line_new)]
	idxs = sorted(idxs, key=lambda x: x[1]-x[0], reverse=True)
	for start_idx, end_idx in idxs:
		line_new = line_new.replace(line[start_idx:end_idx], sep)
	return line_new


def replace_file(filename):
	body, ext = os.path.splitext(filename)
	subprocess.check_call(['rm', filename])
	subprocess.check_call(['mv', body+'_tmp'+ext, filename])

	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('filename', type=str)
	parser.add_argument('--sep', type=str, required=False, default='\t')
	args = parser.parse_args()
	filename = args.filename
	sep = args.sep

	body, ext = os.path.splitext(filename)
	f_w = open(body + '_tmp' + ext, 'w')
	f_r = open(filename, 'r')
	for line in f_r:
		line_clear = replace_spaces(line, sep=sep)
		f_w.write(line_clear+'\n')
	replace_file(filename)
	f_w.close()
	f_r.close()


if __name__ == "__main__":
	main()
