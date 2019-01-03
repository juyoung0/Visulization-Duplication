/**
 * Created by dryji on 2017-02-20.
 * Unit Heatmap, Left dendrogram, Top dendrogram, pathway overview
 */
(function (parent) {
    _.extend(parent,
        {
            createPPINetworkGraph: function (data, unit_id) {
                var $svg = d3.select("#" + unit_id).select("div.block-display")
                    .append("svg")
                    .attr("width", "100%")
                    .attr("viewBox", "0 0 640 480");
                $('#' + unit_id).width(640);


                var h = 480;
                var w = 640;
                //console.log('network', typeof data.nodes[0].x);
                if (typeof data.nodes[0].x == "string") {
                    _.forEach(data.nodes, function (node) {
                        node.x = parseFloat(node.x);
                        node.y = parseFloat(node.y);
                        node.bc = parseFloat(node.bc);
                    })
                }
                if (typeof data.nodes[0].bc == "string") {
                    _.forEach(data.nodes, function (node) {
                        node.bc = parseFloat(node.bc);
                    })
                }
                var bc = _.map(data.nodes, function (item) {
                    return item.bc;
                });
                var domain = [_.min(bc), _.max(bc)];
                console.log(domain);
                //var range = ['#009DE5', '#0291D7', '#0486C9', '#067ABB', '#096FAD', '#0B639F', '#0D5892', '#0F4C84', '#124176', '#143568', '#162A5A', '#191F4D'];
                var range = ['#ccccff', '#000066'];
                var color = d3.scaleLinear(domain).range(range);
                //svg.attr('viewBox', ['0', '0', w, h].join(" "));

                var zoomfun = d3.zoom()
                    .scaleExtent([1 / 100, 10])
                    .on("zoom", zoomed);

                // test code
                $svg
                    .attr("width", "100%")
                    .attr("height", "100%")
                    .call(zoomfun);

                var g_all = $svg
                    .append("g")
                    .style("pointer-events", "all");

                // legend
                var svg_width = 640; // viewbox size
                legended($svg, domain, color, svg_width, unit_id);

                // path
                var line = g_all.selectAll("line")
                    .data(data.edges)
                    .enter()
                    .append("line")
                    .classed('network-edges', true)
                    .attr('x1', function (d) {
                        var source = _.find(data.nodes, {gene: d.src});
                        d3.select(this).attr('y1', source.y);
                        return source.x
                    }).attr('x2', function (d) {
                        var target = _.find(data.nodes, {gene: d.tgt});
                        d3.select(this).attr('y2', target.y);
                        return target.x;
                    })
                    .attr("stroke-opacity", 0.3)
                    .attr("stroke", "#333")
                    .attr("stroke-width", 1);
                //.style('display', 'none');


                var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
                    //console.log('tooltip', d)
                    return "<div class='d3-tip-rect' style='z-index: 99999999'>" +
                        "<span> Gene : " + d.gene + "</span><br>" +
                        "<span> Degree : <span class='d3-tip-value'>" + d.degree + "</span></span><br>" +
                        "<span> Betweenness : " + Math.round(d.bc * 1000)/1000+ "</span>" +
                        "</div>";
                });
                tip.direction('e');

                var circle_g = g_all.selectAll("g")
                    .data(data.nodes)
                    .enter()
                    .append("g")
                    .attr("transform", function (d) {
                        return "translate(" + d.x+ "," + d.y  + ")";
                    });

                circle_g.call(tip)
                    .on('mouseover', function (d) {
                        tip.show(d);
                    }).on('mouseout', function (d) {
                    tip.hide(d);
                });

                circle_g.append('circle')
                    .attr("r", function (d) {
                        return _.max([d.degree*6*2,6]);
                    })
                    .classed('network-nodes', true)
                    .style('fill', function (d) {
                        //console.log(color(d.bc));
                        return color(d.bc);
                    })
                    .style('stroke', '#eee')
                    .style('stroke-width', 0.3);


                circle_g.append('text').text(function (d) {
                    return d.gene;
                }).attr('x', function (d) {
                    return _.max([d.degree*6,1])*(-1);
                }).attr('y', function (d) {
                    return _.max([d.degree*6,1])*(-1);
                }).attr('font-size','80px');
                //translate(87.14991591335115,-15.731719482984715) scale(0.42044820762685714)
                var s = 0.25;
                zoomfun.scaleTo($svg, s);
                var g_bbox = g_all.node().getBoundingClientRect();
                zoomfun.translateBy($svg, (w - g_bbox.width) / (2 * s), (h - g_bbox.height +25) / (2 * s));

                function zoomed() {
                    //d3.event.transform.k > 1 ? line.style('display', null) : line.style('display', 'none');
                    //console.log(d3.event.transform);
                    g_all.attr("transform", d3.event.transform);
                }

                function legended(mySVG, data, colorScale, width, blockId) {
                    var legendSvg = mySVG.append('g').attr('transform', 'translate(0, 0)').classed('legend',true);

                    //console.log(legendSvg.data());
                    //legendSvg.attr('width', legendWidth).attr('height', legendHeight);
                    // Create the svg:defs element and the main gradient definition.
                    var svgDefs = legendSvg.append('defs');
                    var lh = 25;
                    var lw = (width) - 60 * 2;
                    var lx = 60; // legend text width
                    var ly = 20; // legend text height
                    var margin = 5;
                    var g_id = blockId + "mainGradient";
                    var mainGradient = svgDefs.append('linearGradient')
                        .attr('id', g_id).attr("x1", "0%").attr("y1", "0%").attr("x2", "100%").attr("y2", "0%");
                    var stops = mainGradient.selectAll('stop')
                        .data(colorScale.domain())
                        .enter()
                        .append('stop');
                    stops.attr('offset', function (d, i) {
                        var arr = ["0%", "50%", "100%"];
                        return arr[i];
                    })
                        .attr('stop-color', function (d, i) {
                            return colorScale(d);
                        });
                    legendSvg.append("rect")
                        .attr("fill", "url(#" + g_id + ")")
                        .attr("x", lx + margin)
                        .attr("y", 0)
                        .attr("width", lw)
                        .attr("height", lh)
                        .attr("rx", 10)  //rounded corners, of course!
                        .attr("ry", 10);

                    var textY = ly + lh * 2 - 15;
                    legendSvg.append("text")
                        .attr("class", "legendText")
                        .attr("text-anchor", "middle")
                        .attr("x", lx)
                        .attr("y", ly)
                        .attr("dy", 0)
                        .style("font-size", '25px')
                        .style("text-anchor", 'end')
                        .text(data[0].toFixed(2));

                    legendSvg.append("text")
                        .attr("class", "legendText")
                        .attr("text-anchor", "left")
                        .attr("x", lx + 2 * margin + lw)
                        .attr("y", ly)
                        .attr("dy", 0)
                        .style("font-size", '25px')
                        .text(data[1].toFixed(2));
                }
            }
        });
})(visualizer);