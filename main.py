"""
Program to read .elf file, auto create A2L and merge A2L files.
Author: Ximu Zhang
Date: 11/17/2019
"""

# import libraries
from __future__ import print_function
from elf_reader import *
from a2l_generator import *
from a2l_merge import *


def process_file(filename):
	"""
	:param filename: the path of the .elf file
	:return: elf_header_info, elf_section_info, global_symbol_set
	"""
	elf_file, elf_header_info = get_elf_header(filename)
	elf_section_info = get_section_info(elf_file)  # retrieve the section information
	# get_debug_info(elf_file)  # TODO: need to be finished
	global_symbol_set = get_global_symbols(elf_file)  # retrieve section info
	a2l_variable_section_write(global_symbol_set)
	return elf_header_info, elf_section_info, global_symbol_set


if __name__ == '__main__':
	# read elf file
	file_path = '.\\input\\sample.elf'
	elf_header_info, elf_section_info, global_symbol_set = process_file(file_path)

	# merge a2l files
	a2l_file_path = '.\\input\\xx.a2l'
	a2l_file_path2 = '.\\input\\xx.a2l'
	combined_a2l_file = merge_a2l(a2l_file, a2lfile2)
