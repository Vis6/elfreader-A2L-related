"""
Program to read .elf file, auto create A2L and merge A2L files.
Author: Ximu Zhang
Date: 11/17/2019
"""

# import libraries
from __future__ import print_function
import os

from elf_reader import *
from a2l_generator import *
from a2l_merge import *


def process_file(filename):
	"""
	:param filename: the path of the .elf file
	:return: elf_header_info, elf_section_info, global_symbol_set
	"""
	elf_file, elf_header = get_elf_header(filename)
	elf_section = get_section_info(elf_file)  # retrieve the section information
	# get_debug_info(elf_file)  # TODO: need to be finished
	global_symbols = get_global_symbols(elf_file)  # retrieve section info
	a2l_variable_section_write(global_symbols)
	return elf_header, elf_section, global_symbols


def merge_a2l_process(a2l_file_path):
	"""
	Function to merge a2l files.
	:param a2l_file_path: the directory of a2l files
	:return: None
	"""
	combined_measurement_variables = []
	combined_parameter_variables = []

	# r = root, d = directories, f = files
	for r, d, f in os.walk(a2l_file_path):
		for file in f:
			if '.a2l' in file:
				path = os.path.join(r, file)
				combined_measurement_variables, combined_parameter_variables = merge_a2l(
					combined_measurement_variables, combined_parameter_variables, path)

	# combine the variables
	combined_variables = combined_measurement_variables + combined_parameter_variables

	# modify the addresses using values from MAP file
	new_combined_variables = modify_address(combined_variables, global_symbol_set)

	# form combined a2l file
	form_combined_a2l(new_combined_variables)


if __name__ == '__main__':
	# read elf file
	file_path = '.\\input\\sample.elf'
	elf_header_info, elf_section_info, global_symbol_set = process_file(file_path)

	# merge a2l
	file_path = '.\\a2l_ring\\'
	merge_a2l_process(file_path)
