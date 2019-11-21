"""
Program to build am A2L file.
Author: Ximu Zhang
Date: 11/21/2019
"""


def info_extract(symbol_info):
	"""
	This function extracts the useful information of the symbols to be written in the A2L.
	:param symbol_info: information of the symbols
	:return: extracted information
	"""
	extracted_symbol_info = []
	for symbol in symbol_info:
		name = symbol['name']
		addr = symbol['address']
		size = symbol['size']
		extracted_symbol_info.append([name, addr, size])
	return extracted_symbol_info


def a2l_variable_section_write(symbol_info):
	"""
	This function writes the variable section in a2l file
	:param symbol_info: information of the symbols
	:return: None
	"""
	extracted_symbol_info = info_extract(symbol_info)
	sym_type = 'NO_TYPE'
	sym_conversion_method = 'NO_COMPU_METHOD'
	sym_standard_limits_lower = '0'
	sym_standard_limits_upper = '0'

	with open('.\\out\\file.a2l', 'w') as f:
		for item in extracted_symbol_info:
			sym_name = item[0]
			if sym_name != '':
				sym_addr = str(hex(item[1]))  # convert the address to hex format
				sym_size = item[2]

				# regard all the variables as measurements
				f.write("    /begin MEASUREMENT %s \"\"\n" % sym_name)
				f.write("      %s %s 0 0 %s %s\n" % (
					sym_type, sym_conversion_method, sym_standard_limits_lower, sym_standard_limits_upper))
				f.write("      ECU_ADDRESS %s\n" % sym_addr)
				f.write("      SYMBOL_LINK %s 0\n" % sym_name)
				f.write("    /end MEASUREMENT\n\n")
	f.close()
