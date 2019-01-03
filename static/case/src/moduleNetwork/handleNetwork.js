/**
 * Created by dryji on 2017-03-19.
 */
(function (parent) {
    _.extend(parent, {
        getGesa: function (gene_list, species) {
            return $.ajax({
                url: "gsea.html",
                method: "POST",
                data: {
                    gene_list: gene_list.join("\n"),
                    species: species
                },
                error: moduleNetwork.failAjax,
                success: visualizer.createNetworkTable
            });
        },
        getGraph: function (gene_list, species, $unit, $parent) {
            var $n = $unit;
            var $svg = $n.find('svg');
            if ($unit == null) {
                $n = $('#network-edge');
            }
            var w = 640*6;
            var h = 480*6;
            return $.ajax({
                url: "graph.html",
                method: "POST",
                data: {
                    project_name: userManager.PROJECT,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    parent_block_iden: $parent.attr('id'),
                    block_iden: $unit.attr('id'),
                    block_name: $unit.data().req.block_name,
                    gene_list: gene_list.join("\n"),
                    species: species,
                    username: userManager.USERNAME,
                    width: w,
                    height: h
                },
                error: moduleNetwork.failAjax
            }).done(function (data, status) {
                $.get(data.output.edge_path).done(function (edges) {
                    $.get(data.output.node_path).done(function (nodes) {
                        $n.data().req.data = gene_list.join("\n");
                        $n.data().req.data_name = species;
                        visualizer.createPPINetworkGraph({
                            nodes: JSON.parse(nodes).output,
                            edges: JSON.parse(edges).output
                        }, $n.attr('id'));
                    });
                })

            });
        },
        updateSelection: function ($block) {
            console.log($block.find('.gene-selector').val());
        }, loadGraph: function (node_path, edge_path, $block) {
            $.get(edge_path).done(function (edges) {
                $.get(node_path).done(function (nodes) {
                    visualizer.createPPINetworkGraph({
                        nodes: JSON.parse(nodes).output,
                        edges: JSON.parse(edges).output
                    }, $block.attr('id'));
                });
            })
        }
    })
})(moduleNetwork);
