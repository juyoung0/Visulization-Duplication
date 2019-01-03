from heatmap import *

@ensure_csrf_cookie
def make_gsea(request):
    errors = []
    if request.method == 'POST':
        # check information
        param_list = ['gene_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            gene_list = request.POST['gene_list']

            gene_data = gene_list.splitlines()
            db_path = os.path.join(os.getcwd(), 'static', 'file', 'MSIGDB', 'KEGG_and_GO')
            db_file = open(db_path, 'r')  # TODO Put the file location of KEGG_and_GO
            db_data = db_file.read().splitlines()

            total_gene_count = 17179  # Total number of genes in Database
            user_gene_count = len(gene_data)  # Total number of genes in User Gene List

            pathway_list = []  # All Pathways in Database
            path_gene_total_count = {}  # Number of total gene in Pathway
            path_gene_count = {}  # Number of gene in Pathway
            path_gene_list = {}  # Gene List of Pathway
            path_p_value = {}  # p_value of Pathway

            for data in db_data:
                tokens = data.split("	")
                for idx in range(2, len(tokens) - 2):  # In DB, from index (2 to length - 2) is Gene list
                    if tokens[idx] in gene_data:
                        if not tokens[
                            0] in pathway_list:  # If Pathway is not added, Add to pathway list and count = 1, gene list = [node]
                            pathway_list.append(tokens[0])
                            path_gene_count[tokens[0]] = 1
                            path_gene_list[tokens[0]] = [tokens[idx], ]
                            path_gene_total_count[tokens[0]] = int(tokens[len(tokens) - 1])
                        else:  # If Pathway has been added, count += 1, append node to gene list
                            path_gene_count[tokens[0]] += 1
                            path_gene_list[tokens[0]].append(tokens[idx])

            # Caculate P-value ( According to Fisher's Exact Test )
            for elem in pathway_list:
                comp = [len(path_gene_list[elem]), path_gene_total_count[elem],
                        user_gene_count - len(path_gene_list[elem]), total_gene_count - path_gene_total_count[elem]]
                oddsratio, path_p_value[elem] = stats.fisher_exact([[comp[0] - 1, comp[1]], [comp[2], comp[3]]])

            """
            # Make output file & Write it
            output_file_path = "./pathway_result.txt"
            if os.path.isfile(output_file_path):  # If output file already exists, remove it.
                os.remove(output_file_path)
            output_file = open(output_file_path, 'w')
            """

            output = []
            for elem in pathway_list:
                output_elem = {}
                output_elem['pathway'] = elem
                output_elem['count'] = path_gene_count[elem]
                output_elem['p_value'] = path_p_value[elem]
                output.append(output_elem)

            db_file.close()
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Got gsea.", 'output' : output}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : True, 'detail' : "No gsea.", 'output' : None}) ,content_type="application/json")


