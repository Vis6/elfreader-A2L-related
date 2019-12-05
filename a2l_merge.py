"""
Program to merge A2L file and give address to each variable.
Author: Ximu Zhang
Date: 12/02/2019
"""


def merge_a2l(measurement, parameter, compu_method, compu_tab, function, record_layout, a2l_file_path):
	"""
	Function to merge a2l file. (currently only merge the characteristic and measurement parts)
	:param measurement: combination of measurement
	:param parameter: combination of parameter
	:param compu_method: combination of parameter
	:param compu_tab: combination of parameter
	:param function: combination of parameter
	:param record_layout: combination of parameter
	:param a2l_file_path: single a2l file path
	:return: combined measurement variables and combined parameter variables
	"""
	with open(a2l_file_path, 'r') as f:
		text = ''  # initial text
		measurement_flag = False
		parameter_flag = False
		compu_method_flag = False
		compu_tab_flag = False
		function_flag = False
		record_layout_flag = False
		line = f.readline()
		while line:
			if '/begin CHARACTERISTIC' in line:
				text += line
				parameter_flag = True
			elif '/end CHARACTERISTIC' in line:
				text += line
				parameter_flag = False
				parameter.append(text)
				text = ''  # clear

			elif '/begin MEASUREMENT' in line:
				text += line
				measurement_flag = True
			elif '/end MEASUREMENT' in line:
				text += line
				measurement_flag = False
				measurement.append(text)
				text = ''  # clear

			elif '/begin COMPU_METHOD' in line:
				text += line
				compu_method_flag = True
			elif '/end COMPU_METHOD' in line:
				text += line
				compu_method_flag = False
				compu_method.append(text)
				text = ''  # clear

			elif '/begin COMPU_VTAB' in line:
				text += line
				compu_tab_flag = True
			elif '/end COMPU_VTAB' in line:
				text += line
				compu_tab_flag = False
				compu_tab.append(text)
				text = ''  # clear

			elif '/begin FUNCTION' in line:
				text += line
				function_flag = True
			elif '/end FUNCTION' in line:
				text += line
				function_flag = False
				function.append(text)
				text = ''  # clear

			elif '/begin RECORD_LAYOUT' in line:
				text += line
				record_layout_flag = True
			elif '/end RECORD_LAYOUT' in line:
				text += line
				record_layout_flag = False
				record_layout.append(text)
				text = ''  # clear

			else:
				if measurement_flag or parameter_flag or compu_method_flag or compu_tab_flag or function_flag or record_layout_flag:
					text += line
				else:
					pass
			line = f.readline()
	f.close()
	return measurement, parameter, list(set(compu_method)), list(set(compu_tab)), list(set(function)), list(
		set(record_layout))


def form_combined_a2l(variable_list, compu_method_list, compu_tab_list, function_list, record_layout_list):
	"""
	Function to write a a2l file.
	:param variable_list: combined variables including measurements and parameters from all the rings
	:param compu_method_list: combined computation methods from all the rings
	:param compu_tab_list: combined computation tables from all the rings
	:param function_list: combined functions from all the rings
	:param record_layout_list: combined record layouts from all the rings
	:return: None
	"""

	f = open('.\\out\\combined.a2l', 'w')

	# write template - project, module - begin / A2ML - begin and end
	f.write('/begin PROJECT NONAME ""\n  /begin MODULE NONAME ""\n    /begin A2ML\n    /end A2ML\n')

	# component parts
	# for variable in variable_list:
	# 	f.write(variable)
	# 	f.write('\n')  # add blank line between each variable
	write_component(variable_list, f)
	write_component(compu_method_list, f)
	write_component(compu_tab_list, f)
	write_component(function_list, f)
	write_component(record_layout_list, f)

	# write template - project, module - end
	f.write('/end PROJECT\n  /end MODULE\n')
	f.close()


def write_component(parameter, output_file):
	"""
	Function to write the a2l components to the output file.
	:param parameter: a2l component
	:param output_file: output file
	:return: None
	"""
	for param in parameter:
		output_file.write(param)
		output_file.write('\n')  # add blank line between each variable


def modify_address(variable_list, symbol_set):
	"""
	Function to change variable addresses using the values from MAP file.
	:param variable_list: combined variables including measurements and parameters
	:param symbol_set: collection of symbols from MAP file
	:return: variable list with modified addresses
	"""
	new_variable_list = []  # store variables with modified address
	symbol_name_list = [symbol['name'] for symbol in symbol_set]
	variable_string = '\n'

	for variable in variable_list:  # loop for every variable in the variable list
		component_set = variable.split('\n')  # split the string
		for item in component_set:  # for every part in the component_set
			if 'ECU_ADDRESS' in item or 'Address' in item:  # get the location of address
				addr_index = component_set.index(item)  # index of address in the component_set

			if '/* Name */' in item:  # get variable name
				name_index = component_set.index(item)

		address = component_set[addr_index]  # get the address line
		name = component_set[name_index].strip().split('\t')[0]  # get the variable name
		sym_index = symbol_name_list.index(name)  # find the index of the variable in symbol_set
		real_addr = hex(symbol_set[sym_index]['address'])  # the address from MAP file
		new_address = address.replace('0x0000', str(real_addr))  # replace the temp address with real address
		component_set[addr_index] = new_address  # re-give the address to the component set
		new_variable = variable_string.join(component_set)  # join the list into a string
		new_variable_list.append(new_variable)  # append the content to the list

	return new_variable_list
