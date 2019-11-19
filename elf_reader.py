"""
This program contains the functions used in main.py.
Author: Ximu Zhang
Date: 11/19/2019
"""

from elftools.elf.elffile import ELFFile
import pandas as pd
from tabulate import tabulate


def get_elf_header(file_path):
	"""
	This function reads the .elf file and return the information of the elf file
	:param file_path: the path of the .elf file
	:return: the information of the .elf file header
	"""
	f = open(file_path, 'rb')  # open .elf file
	f.seek(0)
	elf_file = ELFFile(f)  # create an ELFFILE object

	# extract the info from the header
	elf_magic = elf_file['e_ident']['EI_MAG']
	elf_class = elf_file['e_ident']['EI_CLASS']
	elf_data = elf_file['e_ident']['EI_DATA']
	elf_version_current = elf_file['e_ident']['EI_VERSION']
	elf_os = elf_file['e_ident']['EI_OSABI']
	elf_abi_version = elf_file['e_ident']['EI_ABIVERSION']
	elf_type = elf_file['e_type']
	elf_machine = elf_file['e_machine']
	elf_version = elf_file['e_version']
	elf_entry_point_address = elf_file['e_entry']
	start_of_program_headers = elf_file['e_phoff']
	start_of_section_headers = elf_file['e_shoff']
	elf_flags = elf_file['e_flags']
	size_of_this_header = elf_file['e_ehsize']
	size_of_program_headers = elf_file['e_phentsize']
	number_of_program_headers = elf_file['e_phnum']
	size_of_section_headers = elf_file['e_shentsize']
	number_of_section_headers = elf_file['e_shnum']
	section_header_string_table_index = elf_file['e_shstrndx']

	# build the elf header info dict
	elf_header_info = {'Magic': elf_magic, 'Class': elf_class, 'Data': elf_data, 'Version current': elf_version_current,
	                   'OS/ABI': elf_os, 'ABI Version': elf_abi_version, 'Type': elf_type, 'Machine': elf_machine,
	                   'Version': elf_version, 'Entry point address': elf_entry_point_address,
	                   'Start of program headers': start_of_program_headers,
	                   'Start of section headers': start_of_section_headers, 'Flags': elf_flags,
	                   'Size of this header': size_of_this_header, 'Size of program headers': size_of_program_headers,
	                   'Number of program headers': number_of_program_headers,
	                   'Size of section headers': size_of_section_headers,
	                   'Number of section headers': number_of_section_headers,
	                   'Section header string table index': section_header_string_table_index}

	# print
	# print("----------------------------------------------------\nELF Header:")
	# for keys, values in elf_header_info.items():
	# 	keys = 'Version' if keys == 'Version current' else keys
	# 	print("    " + keys + ":\t" + str(values))
	# print("----------------------------------------------------")

	# save elf header info
	with open('.\\out\\elf_header_info', 'w') as f:
		for keys, values in elf_header_info.items():
			f.write("%s:\t%s\n" % (keys, str(values)))

	return elf_file, elf_header_info


def get_section_info(elf_file):
	"""
	This function gets the information of each sections and save to a .txt file.
	:param elf_file: the .elf file
	:return: None (will print the section information)
	"""
	num_sections = elf_file.num_sections()  # the number of sections
	section_info = []  # define a list to store dicts
	for i in range(num_sections):
		section = {}  # construct a dict for each section
		section_header = elf_file.get_section(i)  # section header

		# extract the content in the section header
		section['name'] = section_header.name
		section['type'] = section_header['sh_type']
		section['flags'] = section_header['sh_flags']
		section['address'] = section_header['sh_addr']
		section['offset'] = section_header['sh_offset']
		section['size'] = section_header['sh_size']
		section['link'] = section_header['sh_link']
		section['info'] = section_header['sh_info']
		section['addr_align'] = section_header['sh_addralign']
		section['entsize'] = section_header['sh_entsize']

		# add the section dict to the list
		section_info.append(section)

	# convert the list to dataframe and print
	section_info_pd = pd.DataFrame(section_info,
	                               columns=['name', 'type', 'flags', 'address', 'offset', 'size', 'link', 'info',
	                                        'addr_align', 'entsize'])
	print("----------------------------------------------------\nSection Headers:")
	print(tabulate(section_info_pd, showindex=False, headers=section_info_pd.columns))
	print("----------------------------------------------------")

	# save the section information
	section_info_pd.to_csv('.\\out\\section_info.txt', sep='\t', index=False)

	return section_info


def get_symbols(elf_file):
	"""
	Retrieve the symbols from the .elf file
	:param elf_file: .elf file
	:return: symbols in the .elf file
	"""
	# grab symbol table
	sym_table = elf_file.get_section_by_name('.symtab')
	if not sym_table:
		print('No symbol table found.')
		return
	else:
		symbol_name_set = []

		# loop for every symbole in the table
		for i in range(sym_table.num_symbols()):
			symbol = sym_table.get_symbol(i)
			symbol_name = symbol.name
			symbol_name_offset = symbol['st_name']
			symbol_addr = symbol['st_value']
			symbol_size = symbol['st_size']
			symbol_info = symbol['st_info']
			symbol_other = symbol['st_other']  # unused: 0 by default
			symbol_sec = symbol['st_shndx']
			symbol_name_set.append(symbol_name)
	return symbol_name_set
