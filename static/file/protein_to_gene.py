import argparse

parser = argparse.ArgumentParser()
parser.add_argument('ppi_file')
parser.add_argument('alias_file')

args = parser.parse_args()

ppi_file = open(args.ppi_file,'r')
ppi_data = ppi_file.read().splitlines()
alias_file = open(args.alias_file,'r')
alias_data = alias_file.read().splitlines()

protein_gene_map = {}
for elem in alias_data:
	tokens = elem.split("	")
	if not tokens[0] in protein_gene_map.keys():
		protein_gene_map[tokens[0]] = tokens[1]


output_name = args.ppi_file + ".to_gene_symbol"
output_file = open(output_name,'w')

for elem in ppi_data:
	tokens = elem.split(" ")

	if (tokens[0] in protein_gene_map.keys()) and (tokens[1] in protein_gene_map.keys()):
		output_file.write(protein_gene_map[tokens[0]] + " " + protein_gene_map[tokens[1]] + " " + tokens[2] + "\n")

ppi_file.close()
alias_file.close()
output_file.close()
