/**
 * Created by dryji on 2017-02-20.
 * Unit Heatmap, Left dendrogram, Top dendrogram, pathway overview
 */
(function (parent) {
    _.extend(parent,
        {
            createTaperedNetworkGraph: function (svg_id) {
                var svg;
                if (svg_id == undefined)
                    svg = d3.select("#network-edge");
                else
                    svg = d3.select('#' + svg_id);


                //var width = window.innerWidth / 3;
                //var height = 529;
                //svg.attr("viewBox", "0 0 " + width + " " + height);
                svg.attr("width", "100%");
                svg.attr("height", "100%");
                svg.attr('class', 'popup-svg');
                //svg = svg.append('g');
                var width = $('#network-edge').width();
                var height = $('#network-edge').height();
                var viewBox = [0, 0, width, height].join(" ");
                svg.attr("viewBox", viewBox);
                var simulation = d3.forceSimulation()
                    .force("link", d3.forceLink().id(function (d) {
                        return d.id;
                    }))
                    .force("center", d3.forceCenter(width / 2, height / 2))
                    .force("charge", d3.forceManyBody().distanceMax([130]));

                d3.json("static/json/network.json", function (error, graph) {
                    if (error) throw error;

                    var bothLinks = _.intersectionWith(_.cloneDeep(graph.links), _.map(_.cloneDeep(graph.links), function (item, idx) {
                        return {source: item.target, target: item.source};
                    }), _.isEqual);

                    graph.links = _.map(graph.links, function (item, idx) {
                        //console.log(item);
                        if (_.find(bothLinks, item)) {
                            item.both = true;
                        }
                        return item;
                    });

                    var link = svg
                        .selectAll("path")
                        .data(graph.links)
                        .enter().append("path")
                        .attr("class", "graph-edge")
                        .style("fill", "darkgreen")
                        .style("stroke", function (d) {
                            return d.both ? "#0028FF" : "black";
                        })
                        .style("stroke-width", function (d) {
                            return d.both ? 5 : 1;
                        })
                        .style("opacity", 0.75);

                    var gnodes = svg
                        .selectAll("g")
                        .data(graph.nodes)
                        .enter()
                        .append("g")
                        .attr("class", "gnodes")
                        .call(d3.drag()
                            .on("start", dragstarted)
                            .on("drag", dragged)
                            .on("end", dragended));


                    var node = gnodes
                        .attr("class", "graph-node")
                        .append("circle")
                        .attr("r", 4.5).attr("fill", "#333");

                    var labels = gnodes.append("text")
                        .attr("dx", "-10")
                        .attr("dy", "-10")
                        .text(function (d) {
                            return d.name;
                        });

                    var titles = gnodes.append("title")
                        .text(function (d) {
                            return d.id;
                        });

                    simulation
                        .nodes(graph.nodes)
                        .on("tick", ticked);

                    simulation.force("link")
                        .links(graph.links);

                    function ticked() {
                        link
                            .attr("x1", function (d) {
                                return d.source.x;
                            })
                            .attr("y1", function (d) {
                                return d.source.y;
                            })
                            .attr("x2", function (d) {
                                return d.target.x;
                            })
                            .attr("y2", function (d) {
                                return d.target.y;
                            })
                            .attr("d", function (d) {
                                //console.log(d)
                                return d.both ? linkLine(d) : comet(d, 5);
                            })
                            .style("fill", "gold");

                        gnodes.attr("transform", function (d) {
                            return "translate(" + d.x + "," + d.y + ")";
                        });


                        function comet(d, nodeSize) {
                            var diffX = d.target.y - d.source.y;
                            var diffY = d.target.x - d.source.x;

                            var angle0 = ( Math.atan2(diffY, diffX) + ( Math.PI / 2 ) );
                            var angle1 = angle0 - ( Math.PI / 2 );
                            var angle2 = angle0 + ( Math.PI / 2 );

                            var x1 = d.target.x + (nodeSize * Math.cos(angle1));
                            var y1 = d.target.y - (nodeSize * Math.sin(angle1));
                            var x2 = d.target.x + (nodeSize * Math.cos(angle2));
                            var y2 = d.target.y - (nodeSize * Math.sin(angle2));

                            return "M" + x1 + "," + y1 + "L" + x2 + "," + y2 + " L " + d.source.x + "," + d.source.y + "z";
                        }

                        function linkLine(d) {
                            return "M" + d.target.x + " " + d.target.y + " L " + d.source.x + "," + d.source.y + "z";
                        }
                    }
                });

                function dragstarted(d) {
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }

                function dragged(d) {
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                }

                function dragended(d) {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }
            },
            createPPINetworkGraph: function (data, svg_id) {
                var svg = d3.select('#' + svg_id);
                var $svg = $('#' + svg_id);
                svg.selectAll("*").remove();
                var h = $svg.parent().height();
                var w = $svg.parent().width();

                var color = d3.scaleOrdinal(d3.schemeCategory20);

                svg.attr('viewBox', ['0', '0', w, h].join(" "));
                // test code
                var g_all = svg
                    .attr("width", "100%")
                    .attr("height", "100%")
                    .call(d3.zoom()
                        .scaleExtent([1 / 2, 4])
                        .on("zoom", zoomed))
                    .append("g")
                    .style("pointer-events", "all");

                var circle_g = g_all.selectAll("g")
                    .data(data.nodes)
                    .enter()
                    .append("g")
                    .attr("transform", function (d) {
                        return "translate(" + d.x + "," + d.y + ")";
                    });
                circle_g.append('circle')
                    .attr("r", function (d) {
                        return d.size;
                    })
                    .style('fill', function (d) {
                        return color(d.size);
                    })
                    .style('stroke', '#eee')
                    .style('stroke-width', "1.5px");

                circle_g.append('text').text(function (d) {
                    return d.label;
                }).attr('x', function (d) {
                    return d.size;
                }).attr('y', function (d) {
                    return -d.size / 2;
                });

                var line = g_all.selectAll("line")
                    .data(data.edges)
                    .enter()
                    .append("line")
                    .attr('x1', function (d) {
                        var source = _.find(data.nodes, {id: d.source});
                        d3.select(this).attr('y1', source.y);
                        return source.x;
                    }).attr('x2', function (d) {
                        var target = _.find(data.nodes, {id: d.target});
                        d3.select(this).attr('y2', target.y);
                        return target.x;
                    })
                    .attr("stroke-opacity", 0.6)
                    .attr("stroke", "#999");

                function zoomed() {
                    g_all.attr("transform", d3.event.transform);
                }
            }
        });
})(visualizer);