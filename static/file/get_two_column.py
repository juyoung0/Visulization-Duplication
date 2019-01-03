import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file_name')
args = parser.parse_args()

file_name = args.file_name

input_file = open(file_name,'r')
input_data = input_file.read().splitlines()

output_file_name = file_name + ".twocol"
output_file = open(output_file_name,'w')

for elem in input_data:
	tokens = elem.split("	")
	output_file.write(tokens[0] + "	" + tokens[1].upper() + "\n")

input_file.close()
output_file.close()
