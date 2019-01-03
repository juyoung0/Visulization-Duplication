d3.sankey = function(){
    var sankey = {};
    var nodeWidth = 20, nodePadding = 5, sankeyHeight = 400, size = [1, 1];
    var data, nodes = [], links = [], linkBackground = [];

    sankey.nodeWidth = function(_){
        if(!arguments.length) return nodeWidth;
        nodeWidth = _;
        return sankey;
    };

    sankey.nodePadding = function(_){
        if(!arguments.length) return nodePadding;
        nodePadding = _;
        return sankey;
    };

    sankey.sankeyHeight = function(_){
        if(!arguments.length) return sankeyHeight;
        sankeyHeight = _;
        return sankey;
    };

    sankey.size = function(_){
        if(!arguments.length) return size;
        size = _;
        return sankey;
    };

    sankey.data = function(_){
        if(!arguments.length) return data;
        data = _;
        return sankey;
    };

    sankey.nodes = function(){
        return nodes;
    };

    sankey.links = function(){
        return links;
    };

    sankey.linkBackground = function(){
        return linkBackground;
    };

    sankey.link = function(){
        var  curvature = .5;

        var area = d3.area()
                    .x0(function(d){ return d.x0;})
                    .x1(function(d){ return d.x1;})
                    .y0(function(d){ return d.y0;})
                    .y1(function(d){ return d.y1;})
                    .curve(d3.curveBasis);

        function link(d){
            var area_data = [
                {'x0': d.source.x0, 'y0': d.source.y0,
                 'x1': d.source.x1, 'y1': d.source.y1},
                {'x0': d.source.x0, 'y0': (3*d.source.y0+d.target.y0)/4,
                 'x1': d.source.x1, 'y1': (3*d.source.y1+d.target.y1)/4},
                {'x0': d.target.x0, 'y0': (d.source.y0+3*d.target.y0)/4,
                 'x1': d.target.x1, 'y1': (d.source.y1+3*d.target.y1)/4},
                {'x0': d.target.x0, 'y0': d.target.y0,
                 'x1': d.target.x1, 'y1': d.target.y1}
            ];

            return area(area_data);
        }

        return link;
    };

    sankey.layout = function(){
        computeSankey(data, nodes, links, sankeyHeight, nodePadding, linkBackground);
    };

    sankey.sessionLayout = function(){
	    computeSessionSankey(data, nodes, links, sankeyHeight, nodePadding, linkBackground);
    };

    // ------------------ functions

    function computeSankey(data, nodes, links, height, margin, linkBackground){
	    //nodes
        computeNodeXDS(data, nodes, 0, null, height);
        computeNodeYH(nodes, height, margin);

        nodes.forEach(function(node){
            node['y'] += 200;
        });

        //links
        computeLink(nodes, links, nodeWidth, height, linkBackground);

        //parent nodes
        nodes.forEach(function(node){
            if(node.source != -1)
                node['parent'] = nodes[node.source];
            else
                node['parent'] = null;
        })
    }

    function computeSessionSankey(data, nodes, links, height, margin, linkBackground){
        //nodes
        computeSessionNodeXDS(data, nodes, 0, null, height);
        computeSessionNodeYH(nodes, height, margin);

        //links
        computeSessionLink(nodes, links, nodeWidth, height, linkBackground);

        nodes.forEach(function(node){
            if(node.source != -1)
                node['parent'] = nodes[node.source];
            else
                node['parent'] = null;
        })
    }

    function computeNodeXDS(data, nodes, depth, parent, height){
        var y = depth * 100;
        var source;

        if(parent == null) source = -1;
        else source = parent;

        nodes.push({
            'id': data.id,
            'name': data.name,
            'total_action_num': data.total_action_num,
            'action_num': data.action_num,
            'last_date': data.last_date,
            'ver': data.ver,
            'save_ver': data.save_ver,
            'anno_num': data.anno_num,
            'action_list': data.action_list,
	        'children': data.children,
            'y': y,
            'depth': depth,
            'source': source,
            'is_broken': data.is_broken,
            'bookmark': data.bookmark,
            'vis_type': data.vis_type
        });

        if(data.children){
            var tmp = nodes.length-1;
            for(var i = 0; i < data.children.length; i++){
                computeNodeXDS(data.children[i], nodes, depth+1, tmp, height);
            }
        }
    }

    function computeSessionNodeXDS(data, nodes, depth, parent, height){
        var y = depth * 100;
        var source;

        if(parent == null) source = -1;
        else source = parent;

        nodes.push({
            'id': data.id,
	        'name': data.name,
            'total_action_num': data.total_action_num,
            'action_num': data.action_num,
            'last_date': data.last_date,
            'ver': data.ver,
            'anno_num': data.anno_num,
            'action_list': data.action_list,
	        'children': data.children,
            'y': y,
            'depth': depth,
            'source': source,
            'bookmark': data.bookmark
        });

        if(data.children){
            var tmp = nodes.length-1;
            for(var i = 0; i < data.children.length; i++){
                computeSessionNodeXDS(data.children[i], nodes, depth+1, tmp, height);
            }
        }
    }

    function computeNodeYH(nodes, height, margin){

        var heightest = 0;
        var depthSum = [];
        var y_tmp = [];

        nodes.forEach(function(node){
            if(depthSum[node.depth] == undefined)
                depthSum[node.depth] = node.action_num;
            else
                depthSum[node.depth] += node.action_num;
        });

        depthSum.forEach(function(d){
            if(d > heightest) heightest = d;
        });

        nodes.forEach(function(node){
            var node_height;
            if(node.action_num == 0){
                if(node.depth == 0)
                    node_height = height;
                else
                    node_height = height / heightest;
            }
            else
                node_height = height * node.action_num / heightest;

            if(y_tmp[node.depth] == undefined){
                node['x'] = 0;
                y_tmp[node.depth] = node_height;
            }
            else {
                node['x'] = y_tmp[node.depth];
                y_tmp[node.depth] += node_height;
            }

            if(node['depth'] == 0)
                node['height'] = 1;
            else if (node_height - margin <= 0)
                node['height'] = 1;
            else
                node['height'] = node_height - margin;
        });

        // centerization
        nodes.forEach(function(node){
            if(heightest != 0)
                node['x'] += (height/2 - height * depthSum[node.depth]/(2*heightest));
            else
                node['x'] += height/2;
        });
    }

    function computeSessionNodeYH(nodes, height, margin){

        var heightest = 0;
        var depthSum = [];
        var y_tmp = [];

        nodes.forEach(function(node){
            if(depthSum[node.depth] == undefined)
                depthSum[node.depth] = node.action_num;
            else
                depthSum[node.depth] += node.action_num;
        });

        depthSum.forEach(function(d){
            if(d > heightest) heightest = d;
        });

        nodes.forEach(function(node){
            var node_height;
            if(node.action_num == 0){
                if(node.depth == 0)
                    node_height = height;
                else {
                    node_height = height / heightest;
                }
            }
            else
                node_height = height * node.action_num / heightest;

            if(y_tmp[node.depth] == undefined){
                node['x'] = 0;
                y_tmp[node.depth] = node_height;
            }
            else {
                node['x'] = y_tmp[node.depth];
                y_tmp[node.depth] += node_height;
            }

            if(node['depth'] == 0)
                node['height'] = 1;
            else if (node_height - margin <= 0)
                node['height'] = 1;
            else
                node['height'] = node_height - margin;
        });

        // centerization
        nodes.forEach(function(node){
            if(heightest != 0)
                node['x'] += (height/2 - height * depthSum[node.depth]/(2*heightest));
            else
                node['x'] += height/2;
        });
    }

    function computeLink(nodes, links, nodeWidth, height, linkBackground){

        var sourceDepthSum = [];
        var source_sum = [];

        nodes.forEach(function(node){
            if(sourceDepthSum[node.source] == undefined)
                sourceDepthSum[node.source] = node.action_num;
            else
                sourceDepthSum[node.source] += node.action_num;
        });

        nodes.forEach(function(node){
            var source = node.source;

            if(source != -1){
                var source_y1 = nodes[source].height * node.action_num / sourceDepthSum[node.source];

                if(source_sum[source] == undefined)
                    source_sum[source] = 0;

                var actionList = node.action_list;

                // link background
                linkBackground.push({
                    'source':{
                        'x0': nodes[source].x + source_sum[source],
                        'y0': nodes[source].y + nodeWidth + 1,
                        'x1': nodes[source].x + source_sum[source] + source_y1,
                        'y1': nodes[source].y + nodeWidth + 1
                    },
                    'target':{
                        'x0': node.x, 'y0': node.y - 1,
                        'x1': node.x + node.height, 'y1': node.y - 1
                    }
                });

                var j = 0;
                actionList.forEach(function(action){
                    links.push({
                        'action': action.action,
                        'source':{
                            'x0': (nodes[source].x + source_sum[source] + source_y1 * j / actionList.length+nodes[source].x + source_sum[source] + source_y1 * (j+1) / actionList.length)/2-0.01,
                            'y0': nodes[source].y + nodeWidth + 1,
                            'x1': (nodes[source].x + source_sum[source] + source_y1 * j / actionList.length+nodes[source].x + source_sum[source] + source_y1 * (j+1) / actionList.length)/2,
                            'y1': nodes[source].y + nodeWidth + 1
                        },
                        'target':{
                            'x0': (node.x + node.height * j / actionList.length+node.x + node.height * (j+1) / actionList.length)/2-0.01,
                            'y0': node.y-1,
                            'x1': (node.x + node.height * j / actionList.length+node.x + node.height * (j+1) / actionList.length)/2,
                            'y1': node.y-1
                        }
                    });

                    j++;
                });

                source_sum[source] += source_y1
            }
        })
    }

    function computeSessionLink(nodes, links, nodeWidth, height, linkBackground){

        var sourceDepthSum = [];
        var source_sum = [];

        nodes.forEach(function(node){
            if(sourceDepthSum[node.source] == undefined)
                sourceDepthSum[node.source] = node.action_num;
            else
                sourceDepthSum[node.source] += node.action_num;
        });

        nodes.forEach(function(node){
            var source = node.source;

            if(source != -1){
                    var source_y1 = nodes[source].height * node.action_num / sourceDepthSum[node.source];

                    if(source_sum[source] == undefined)
                        source_sum[source] = 0;

                    var actionList = node.action_list;
                    console.log('node')
                    console.log(node)

                    // link background
                    linkBackground.push({
                        'source':{
                            'x0': nodes[source].x + source_sum[source],
                            'y0': nodes[source].y + nodeWidth + 1,
                            'x1': nodes[source].x + source_sum[source] + source_y1,
                            'y1': nodes[source].y + nodeWidth + 1
                        },
                        'target':{
                            'x0': node.x, 'y0': node.y - 1,
                            'x1': node.x + node.height, 'y1': node.y - 1
                        }
                    });

                    var j = 0;
                    actionList.forEach(function(action){
                        links.push({
                            'action': action.action,
                            'source':{
                                'x0': (nodes[source].x + source_sum[source] + source_y1 * j / actionList.length+nodes[source].x + source_sum[source] + source_y1 * (j+1) / actionList.length)/2-0.01,
                                'y0': nodes[source].y + nodeWidth + 1,
                                'x1': (nodes[source].x + source_sum[source] + source_y1 * j / actionList.length+nodes[source].x + source_sum[source] + source_y1 * (j+1) / actionList.length)/2,
                                'y1': nodes[source].y + nodeWidth + 1
                            },
                            'target':{
                                'x0': (node.x + node.height * j / actionList.length+node.x + node.height * (j+1) / actionList.length)/2-0.01,
                                'y0': node.y-1,
                                'x1': (node.x + node.height * j / actionList.length+node.x + node.height * (j+1) / actionList.length)/2,
                                'y1': node.y-1
                            }
                        });

                        j++;
                    });

                source_sum[source] += source_y1;
            }
        })
    }

    sankey.console = function(){
        console.log(data);
        console.log(nodes);
        console.log(links);
    };


    return sankey;
};
