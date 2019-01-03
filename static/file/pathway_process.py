import argparse
import os
#from fisher import pvalue
import scipy.stats as stats

parser = argparse.ArgumentParser(description='Get Gene List and MSIGDB -> Generate (pathway,count,p-value,gene_list)')
parser.add_argument('gene_list_file',type=str,help='Gene List file')

args = parser.parse_args()

gene_file = open(args.gene_list_file,'r')
gene_data = gene_file.read().splitlines()
db_path = os.path.join(os.getcwd(), 'MSIGDB', 'KEGG_and_GO')
db_file = open(db_path,'r') # TODO Put the file location of KEGG_and_GO
db_data = db_file.read().splitlines()

total_gene_count = 17179 # Total number of genes in Database
user_gene_count = len(gene_data) # Total number of genes in User Gene List

pathway_list = [] # All Pathways in Database
path_gene_total_count = {} # Number of total gene in Pathway
path_gene_count = {} # Number of gene in Pathway
path_gene_list = {} # Gene List of Pathway
path_p_value = {} # p_value of Pathway

for data in db_data:
	tokens = data.split("	")
	for idx in range(2,len(tokens)-2): # In DB, from index (2 to length - 2) is Gene list
		if tokens[idx] in gene_data:
			if not tokens[0] in pathway_list: # If Pathway is not added, Add to pathway list and count = 1, gene list = [node]
				pathway_list.append(tokens[0])
				path_gene_count[tokens[0]] = 1
				path_gene_list[tokens[0]] = [tokens[idx],]
				path_gene_total_count[tokens[0]] = int(tokens[len(tokens)-1])
			else: # If Pathway has been added, count += 1, append node to gene list
				path_gene_count[tokens[0]] += 1
				path_gene_list[tokens[0]].append(tokens[idx])


# Caculate P-value ( According to Fisher's Exact Test )
for elem in pathway_list:
	comp = [len(path_gene_list[elem]),path_gene_total_count[elem],user_gene_count-len(path_gene_list[elem]),total_gene_count-path_gene_total_count[elem]]
	oddsratio, path_p_value[elem] = stats.fisher_exact([[comp[0]-1,comp[1]],[comp[2],comp[3]]])
		
# Make output file & Write it
output_file_path = "./pathway_result.txt"
if os.path.isfile(output_file_path): # If output file already exists, remove it.
	os.remove(output_file_path)
output_file = open(output_file_path,'w')

for elem in pathway_list:
	temp = elem
	temp += "	count : " + str(path_gene_count[elem]) + " p_value : " + str(path_p_value[elem])
	#temp += "	count : %d	p_value : %.9f	[ " % (path_gene_count[elem],path_p_value[elem])
	for x in path_gene_list[elem]:
		temp += (x + " ")
	temp += "]\n"

	output_file.write(temp)

gene_file.close()
db_file.close()
output_file.close()
