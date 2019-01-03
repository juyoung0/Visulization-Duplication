/**
 * Created by dryji on 2017-02-20.
 * Unit Heatmap, Left dendrogram, Top dendrogram, pathway overview
 */
(function (parent) {
    // this.changedSelection = [];
    this.changedOrder = [];
    this.changedSelection = [];
    _.extend(parent,
        {
            /*createHeatmap : function(data, cols, rows, blockId, name){
             var $block = $('#' + blockId);
             var dataObj = $block.data();
             var length = data.length;
             var color = dataObj.req.colorType;
             var $clusterType = dataObj.req.cluster_type;
             var $clusterParam = dataObj.req.cluster_param;
             var basicUrl = "geromics/";
             var treeId = blockId + "-tree";
             var colTreeId = blockId + "-colTree";
             var heatmapId = blockId + "-heatmap";
             var heatmapRow;
             var heatmapRects;
             var legendWidth = 150,
             legendHeight = 400,
             padding = 5;
             colorArr = JSON.parse(dataObj.req.color_type);
             switch (dataObj.req.color_type) {
             case "Green, Black, Red":
             colorArr = ["#00ff00", "#000000", "#ff0000"];
             break;
             case "Blue, White, Red":
             colorArr = ["blue", "white", "red"];
             break;
             case "Red, Orange, Yellow":
             colorArr = ["#ffff00", "#ffa500", "#ff0000"];
             break;
             }

             var colorScale = d3.scaleLinear()
             .domain([dataObj.res.min, 0, dataObj.res.max])
             .range(colorArr);
             var currentColor = colorScale;
             var mytest = colorScale;
             var h = 50, w = 50;
             var height = (h * rows.length) + 300;
             var width = (w * cols.length) + 300;
             var loadContent = [];
             var treeWidth = (w * cols.length), treeHeight = h * rows.length;
             var maxRowLength = _.max(_.map(rows, function (item) { return item.length}));
             var colTreeWidth = width - maxRowLength*14, colTreeHeight = 80;
             d3.select("#" + blockId).select("div.block-display").html("");
             var originViewBox = "-20 -50 " + ((width) + 400) + " " + (height + 110);
             var mySVG = d3.select("#" + blockId).select("div.block-display")
             .append("svg")
             .attr("width", "100%")
             .attr("viewBox", originViewBox);
             $block.attr('originViewBox', originViewBox);
             var legendSvg = mySVG.append('g').attr('transform', 'translate(0, -250)');
             var svgDefs = legendSvg.append('defs');
             var lh = 50;
             var lw = (width) + 140;
             var lx = 100;
             var ly = 155;
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

             var heatmapG = mySVG.append('g')
             .attr("transform", "translate(350, 110)")
             .attr("id", heatmapId)
             .on('mouseover', function (d, i) {
             heatmapG.classed('state', true);
             }).on('mouseout', function (d, i) {
             heatmapG.classed('state', false);
             });

             var colTreeG = mySVG
             .append("g")
             .attr("id", colTreeId)
             .attr("transform", "translate(400, 30)");

             var treeG = mySVG
             .append("g")
             .attr("id", treeId)
             .attr("transform", "translate(20,163)");

             heatmapRow = heatmapG.selectAll(".heatmap")
             .data(data)
             .enter().append("g");

             // Draw the Heatmap
             var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
             return "<div class='d3-tip-rect' style='z-index: 99'>" +
             "<span> SOURCE : " + cols[d[2]] + "</span><br>" +
             "<span> GENE : <span class='d3-tip-value'>" + rows[d[1]] + "</span></span><br>" +
             "<span> VALUE : " + d[0] + "</span>" +
             "</div>";
             });
             tip.direction('e');

             var yCount = 0;
             heatmapRects = heatmapRow
             .selectAll(".rect")
             .data(function (d, i, self) {
             return d;
             })
             .enter()
             .append("svg:rect")
             .attr('width', w)
             .attr('height', h)
             .attr('x', function (d, i) {
             return (w * d[2]) + 50;
             })
             .attr('y', function (d, i, rowData) {
             return (h * d[1]) + 50;
             })
             .attr('class', 'bordered')
             .style('fill', function (d) {
             return colorScale(d[0]);
             })
             .on("click", function (d, i) {
             ////console.log(this);
             if (!d3.event.ctrlKey) {
             d3.selectAll('rect.selected').classed("selected", false);
             d3.select('.canvas-popup').classed('popup', false);
             var $menuSelector = $('#contextMenu');
             $menuSelector.hide();
             contextMenuShowing = false;
             }
             })
             .on('mouseover', function (e) {
             tip.show(e);
             $(this).css({
             'stroke': '#fff',
             'stroke-width': '9px'
             });

             var xPosition = parseFloat(d3.select(this).attr('x')) + w / 2;
             var yPosition = parseFloat(d3.select(this).attr('y')) / 2 + h / 2;

             var zoomTip = d3.select('#tooltip')
             .style({
             left: xPosition + 'px',
             top: yPosition + 'px'
             });
             })
             .on('mouseout', function (e) {
             $(this).css({
             'stroke': '#E6E6E6',
             'stroke-width': '0px'
             });
             tip.hide(e);
             if (d3.event.relatedTarget != null && d3.event.relatedTarget.tagName == 'HTML') {
             // remove selection frame
             heatmapG.selectAll("rect.selection").remove();

             // remove temporary selection marker class
             d3.selectAll('g.state.selection').classed("selection", false);
             }
             }).on("mousedown", function (d, i, data) {
             if (!d3.event.ctrlKey) {
             d3.selectAll('g.selected').classed("selected", false);
             }
             else {
             var e = d3.event,
             g = this,
             isSelected = d3.select(g).classed("selected");
             d3.select(g).classed("selected", !isSelected);
             // reappend dragged element as last
             // so that its stays on top
             g.parentNode.appendChild(g);
             }
             var p = d3.mouse(this);
             if (!d3.event.shiftKey) return;
             heatmapG.append("rect")
             .attrs({
             rx: 6,
             ry: 6,
             x: p[0],
             y: p[1],
             width: 0,
             height: 0
             }).attr('class', 'selection')
             })
             .on("mousemove", function () {
             if (!d3.event.shiftKey) return;
             var s = heatmapG.select("rect.selection");
             if (!s.empty()) {
             var p = d3.mouse(this),
             d = {
             x: parseInt(s.attr("x"), 10),
             y: parseInt(s.attr("y"), 10),
             width: parseInt(s.attr("width"), 10),
             height: parseInt(s.attr("height"), 10)
             },
             move = {
             x: p[0] - d.x,
             y: p[1] - d.y
             };
             //////console.log(p);

             if (move.x < 1 || (move.x * 2 < d.width)) {
             d.x = p[0];
             d.width -= move.x;
             if (d.width < 0) d.width -= d.width;
             } else {
             d.width = move.x;
             if (d.width < 0) d.width -= d.width;
             }

             if (move.y < 1 || (move.y * 2 < d.height)) {
             d.y = p[1];
             d.height -= move.y;
             if (d.height < 0) d.height -= d.height;
             } else {
             d.height = move.y;
             if (d.height < 0) d.height -= d.height;
             }
             s.attrs(d);

             // deselect all temporary selected state objects
             d3.selectAll('g.state.selection.selected').classed("selected", false);
             d3.select('g.state').selectAll('rect').nodes().forEach(function (state_data, i) {
             var rect = d3.select(state_data);
             var x = rect.attr('x');
             var y = rect.attr('y');
             if (
             !d3.select(state_data).classed("selected") &&
             // inner rect inside selection frame
             x <= d.x + d.width && x >= d.x - w &&
             y <= d.y + d.height && y >= d.y - h
             ) {
             d3.select(state_data)
             .classed("selected", true);
             }
             });
             }
             })
             .on("mouseup", function () {
             // remove selection frame
             heatmapG.selectAll("rect.selection").remove();
             if (d3.event.ctrlKey) {
             var blockId = d3.select('g.state').attr('id');
             ////console.log(blockId);
             ////console.log(d3.selectAll('rect.selected').data());
             var sources = d3.selectAll('rect.selected').data().map(function (d, i, data) {
             return cols[d[2]];
             });
             var genes = d3.selectAll('rect.selected').data().map(function (d, i, data) {
             //return {source: completecols[d[2]], gene: completerows[d[1]], value: d[0]}
             return rows[d[1]];
             });
             var values = d3.selectAll('rect.selected').data().map(function (d, i, data) {
             var col = cols[d[2]];
             var row = rows[d[1]];
             return [d[0], genes.indexOf(row), sources.indexOf(col)];
             });
             var obj = {id: blockId, values: values, rows: genes, cols: sources};
             unitManager.SELECTED = obj;
             }
             })
             .call(tip);




             },*/
            createHeatmap: function (data, cols, rows, blockId, name) {
                //console.log(blockId);
                var $block = $('#' + blockId);
                var dataObj = $block.data();
                var length = data.length;
                var colLabel_font_size = 10.5;
                var colLabel_length = cols[0].length * colLabel_font_size;
                var color = dataObj.req.colorType;
                var $clusterType = dataObj.req.cluster_type;
                var $clusterParam = dataObj.req.cluster_param;
                var basicUrl = "geromics/";

                var treeId = blockId + "-tree";
                var colTreeId = blockId + "-colTree";
                var heatmapId = blockId + "-heatmap";

                // Main createHeatmap SVG Information
                var heatmapRow;
                var heatmapRects;

                //var currentColor, currentData, currentCols, currentRows, currentCluster;
                var legendWidth = 150,
                    legendHeight = 400,
                    padding = 5;
                // chunggilee implementation
                colorArr = JSON.parse(dataObj.req.color_type);
                switch (dataObj.req.color_type) {
                    case "Green, Black, Red":
                        colorArr = ["#00ff00", "#000000", "#ff0000"];
                        break;
                    case "Blue, White, Red":
                        colorArr = ["blue", "white", "red"];
                        break;
                    case "Red, Orange, Yellow":
                        colorArr = ["#ffff00", "#ffa500", "#ff0000"];
                        break;
                }

                var colorScale = d3.scaleLinear()
                //.domain([dataObj.res.min, 0, dataObj.res.max])
                    .domain([-2, 0, 2])
                    .range(colorArr);
                var currentColor = colorScale;
                var mytest = colorScale;

                //height of each row in the createHeatmap
                var h = 50, w = 50;
                //width of each column in the createHeatmap
                //attach a SVG node to the document
                //height and width defined by the row/column lengths
                var height = (h * rows.length) + 300;
                var width = (w * cols.length) + 300;
                //d3.select("body").append("div").attr("id","createHeatmap");
                var loadContent = [];
                // Main Row Tree SVG Information
                var treeWidth = (w * cols.length), treeHeight = h * rows.length;
                // Main Column Tree SVG Information
                var maxRowLength = _.max(_.map(rows, function (item) {
                    return item.length
                }));
                var colTreeWidth = width - maxRowLength * 14, colTreeHeight = 80;
                d3.select("#" + blockId).select("div.block-display").html("");
                var originViewBox = "-20 -50 " + ((width) + 400) + " " + (height + 110);
                var mySVG = d3.select("#" + blockId).select("div.block-display")
                    .append("svg")
                    .attr("width", "100%")
                    .attr("viewBox", originViewBox);
                $block.attr('originViewBox', originViewBox);

                var legendSvg = mySVG.append('g').attr('transform', 'translate(0, -250)').classed('legend', true);

                //////console.log(legendSvg.data());
                //legendSvg.attr('width', legendWidth).attr('height', legendHeight);
                // Create the svg:defs element and the main gradient definition.
                var svgDefs = legendSvg.append('defs');
                var lh = 50;
                var lw = (width) + 140;
                var lx = 100;
                var ly = 155;
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
                    .attr("x", lx + 25)
                    .attr("y", ly + 50)
                    .attr("width", lw)
                    .attr("height", lh)
                    .attr("rx", 10)  //rounded corners, of course!
                    .attr("ry", 10);

                var textY = ly + lh * 2 - 15;
                legendSvg.append("text")
                    .attr("class", "legendText")
                    .attr("text-anchor", "middle")
                    .attr("x", lx)
                    .attr("y", textY)
                    .attr("dy", 0)
                    .style("font-size", '25px')
                    .style("text-anchor", 'end')
                    .text(dataObj.res.min.toFixed(2));

                legendSvg.append("text")
                    .attr("class", "legendText")
                    .attr("text-anchor", "left")
                    .attr("x", lx + lw + 40)
                    .attr("y", textY)
                    .attr("dy", 0)
                    .style("font-size", '25px')
                    .text(dataObj.res.max.toFixed(2));


                var heatmapG = mySVG.append('g')
                    .attr("transform", "translate(350, 110)")
                    .attr("id", heatmapId)
                    .on('mouseenter', function (d, i) {
                        heatmapG.classed('state', true);
                    }).on('mouseout', function (d, i) {
                        heatmapG.classed('state', false);
                    });
                //.attr("transform", "translate(500, 0)")
                var colTreeG = mySVG
                    .append("g")
                    .attr("id", colTreeId)
                    .attr("transform", "translate(400, 30)");
                //.attr("width", colTreeWidth)
                //.attr("height", colTreeHeight)
                //.attr("transform", "translate(-100, 0)")
                var treeG = mySVG
                    .append("g")
                    .attr("id", treeId)
                    .attr("transform", "translate(20," + (110 + colLabel_length) + ")");

                //.attr("width", treeWidth)

                //.attr("transform", "translate(40, 0)");
                //generate the Heatmap
                heatmapRow = heatmapG.selectAll(".heatmap")
                    .data(data)
                    .enter().append("g");

                // Draw the Heatmap
                var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
                    return "<div class='d3-tip-rect' style='z-index: 99'>" +
                        "<span> SOURCE : " + cols[d[2]] + "</span><br>" +
                        "<span> GENE : <span class='d3-tip-value'>" + rows[d[1]] + "</span></span><br>" +
                        "<span> VALUE : " + d[0] + "</span>" +
                        "</div>";
                });
                tip.direction('e');
                //tip.offset([0, w]);

                var yCount = 0;
                $('#content-list').on('click', function () {
                    //d3.selectAll('rect.selected').classed("selected", false);
                    d3.select('.canvas-popup').classed('popup', false);
                    var $menuSelector = $('#contextMenu');
                    $menuSelector.hide();
                    contextMenuShowing = false;
                });
                heatmapRects = heatmapRow
                    .selectAll(".rect")
                    .data(function (d, i, self) {
                        return d;
                    })
                    .enter()
                    .append("svg:rect")
                    .attr('width', w)
                    .attr('height', h)
                    .attr('x', function (d, i) {
                        return (w * d[2]) + 50;
                    })
                    .attr('y', function (d, i, rowData) {
                        return (h * d[1]) + colLabel_length;
                    })
                    //.attr('rx', 5)
                    //.attr('ry', 5)
                    .attr('class', 'bordered')
                    .style('fill', function (d) {
                        return colorScale(d[0]);
                    })
                    .on("click", function (d, i) {
                        if (!d3.event.ctrlKey) {
                            d3.selectAll('rect.selected').classed("selected", false);
                            d3.select('.canvas-popup').classed('popup', false);
                            var $menuSelector = $('#contextMenu');
                            $menuSelector.hide();
                            contextMenuShowing = false;
                        }
                    })
                    .on('mouseover', function (e) {
                        tip.show(e);
                        $(this).css({
                            'stroke': '#fff',
                            'stroke-width': '9px'
                        });

                        var xPosition = parseFloat(d3.select(this).attr('x')) + w / 2;
                        var yPosition = parseFloat(d3.select(this).attr('y')) / 2 + h / 2;

                        var zoomTip = d3.select('#tooltip')
                            .style({
                                left: xPosition + 'px',
                                top: yPosition + 'px'
                            });
                        //var svgClone = heatmapG.clone();
                        //zoomTip.append(svgClone);
                        //zoomTip.classed('hidden', false);

                    })
                    .on('mouseout', function (e) {
                        $(this).css({
                            'stroke': '#E6E6E6',
                            'stroke-width': '0px'
                        });
                        tip.hide(e);
                        if (d3.event.relatedTarget != null && d3.event.relatedTarget.tagName == 'HTML') {
                            // remove selection frame
                            heatmapG.selectAll("rect.selection").remove();
                            // remove temporary selection marker class
                            d3.selectAll('g.state.selection').classed("selection", false);

                        }
                        //$('#contextMenu').hide();
                    }).on("mousedown", function (d, i, data) {
                        if (!d3.event.ctrlKey) {
                            d3.selectAll('g.selected').classed("selected", false);
                        }
                        else {
                            var e = d3.event,
                                g = this,
                                isSelected = d3.select(g).classed("selected");
                            d3.select(g).classed("selected", !isSelected);
                            // reappend dragged element as last
                            // so that its stays on top
                            g.parentNode.appendChild(g);
                        }
                        var p = d3.mouse(this);
                        if (!d3.event.shiftKey) {
                            heatmapG.selectAll("rect.selection").remove();
                            return;
                        }
                        heatmapG.append("rect")
                            .attrs({
                                rx: 6,
                                ry: 6,
                                x: p[0],
                                y: p[1],
                                width: 0,
                                height: 0
                            }).attr('class', 'selection')
                    })
                    .on("mousemove", function () {
                        if (!d3.event.shiftKey) return;
                        var s = heatmapG.select("rect.selection");
                        if (!s.empty()) {
                            var p = d3.mouse(this),
                                d = {
                                    x: parseInt(s.attr("x"), 10),
                                    y: parseInt(s.attr("y"), 10),
                                    width: parseInt(s.attr("width"), 10),
                                    height: parseInt(s.attr("height"), 10)
                                },
                                move = {
                                    x: p[0] - d.x,
                                    y: p[1] - d.y
                                };
                            //////console.log(p);

                            if (move.x < 1 || (move.x * 2 < d.width)) {
                                d.x = p[0];
                                d.width -= move.x;
                                if (d.width < 0) d.width -= d.width;
                            } else {
                                d.width = move.x;
                                if (d.width < 0) d.width -= d.width;
                            }

                            if (move.y < 1 || (move.y * 2 < d.height)) {
                                d.y = p[1];
                                d.height -= move.y;
                                if (d.height < 0) d.height -= d.height;
                            } else {
                                d.height = move.y;
                                if (d.height < 0) d.height -= d.height;
                            }
                            s.attrs(d);

                            // deselect all temporary selected state objects
                            d3.selectAll('g.state.selection.selected').classed("selected", false);
                            d3.select('g.state').selectAll('rect').nodes().forEach(function (state_data, i) {
                                var rect = d3.select(state_data);
                                var x = rect.attr('x');
                                var y = rect.attr('y');
                                if (
                                    !d3.select(state_data).classed("selected") &&
                                    // inner rect inside selection frame
                                    x <= d.x + d.width && x >= d.x - w &&
                                    y <= d.y + d.height && y >= d.y - h
                                ) {
                                    //console.log(state_data);
                                    d3.select(state_data)
                                        .classed("selected", true);
                                }
                            });
                        }
                    })
                    .on("mouseup", function () {
                        // remove selection frame
                        heatmapG.selectAll("rect.selection").remove();
                        if (d3.event.ctrlKey) {
                            var blockId = d3.select('g.state').attr('id');
                            /*
                             var sources = d3.selectAll('rect.selected').data().map(function (d, i, data) {
                             //return {source: completecols[d[2]], gene: completerows[d[1]], value: d[0]}
                             return cols[d[2]];
                             });
                             var genes = d3.selectAll('rect.selected').data().map(function (d, i, data) {
                             //return {source: completecols[d[2]], gene: completerows[d[1]], value: d[0]}
                             return rows[d[1]];
                             });
                             var values = d3.selectAll('rect.selected').data().map(function (d, i, data) {
                             var col = cols[d[2]];
                             var row = rows[d[1]];
                             return [d[0], genes.indexOf(row), sources.indexOf(col)];
                             });
                             //var obj = {id: blockId, values: values, rows: genes, cols: sources};
                             //unitManager.SELECTED = obj;
                             */
                        }
                    })
                    .call(tip);

                // 히트맵 컨텍스트 메뉴
                var contextMenuShowing = false;
                heatmapG.on('contextmenu', function (d, i, self) {
                    if (contextMenuShowing) {
                        d3.event.preventDefault();
                        d3.select('.popup-svg').selectAll("*").remove();
                        d3.select('.canvas-popup').classed('popup', false);
                        contextMenuShowing = false;
                    } else {
                        if (d3.event.ctrlKey) return;
                        d3_target = d3.select(d3.event.target);
                        d3.event.preventDefault();
                        var $menuSelector = $('#contextMenu');
                        var mousePosition = d3.mouse(d3.select('body').node());
                        $menuSelector.show().css({
                            left: mousePosition[0] + 10 + 'px',
                            top: mousePosition[1] + 10 + 'px'
                        });
                        $menuSelector.find('a.context-menu-pathway').unbind('click');
                        $menuSelector.find('a.context-menu-pathway').on('click', function (e) {
                            if (d3_target.classed("selected")) {
                                contextMenuShowing = true;
                                d = d3_target.datum();
                                // Build the popup
                                $('.canvas-popup').css({
                                    "left": mousePosition[0] + 50
                                    , "top": mousePosition[1]
                                }).addClass('popup');
                                var popup = d3.select(".canvas-popup").select("svg").classed('popup-svg', true);
                                visualizer.createTaperedNetworkGraph(popup);
                                $menuSelector.hide();
                            }
                        });
                        $menuSelector.find('a.context-menu-new-block').unbind('click');
                        $menuSelector.find('a.context-menu-new-block').on('click', function (e) {
                            var data = $block.data().req.data.split('\n');
                            var header = cols;

                            var selection = _.sortBy(_.filter(d3.selectAll('rect.selected').data(), function (item) {
                                return item
                            }), [1, 2]);
                            if (selection.length == 0) {
                                alert('Please select data on the unit.');
                                return;
                            }
                            var map_row = _.map(selection, function (item) {
                                return item[1];
                            });
                            var map_col = _.map(selection, function (item) {
                                return item[2];
                            });
                            var min_col = _.min(map_col);
                            var max_col = _.max(map_col);
                            var sub_rows = [];
                            // data body
                            var r = null;
                            var sub_row =[];
                            _.forEach(selection, function (row, idx) {
                                if (r == null){
                                    sub_row.push(rows[row[1]]);
                                }
                                if (r != null && r != row[1]){
                                    sub_rows.push(_.cloneDeep(sub_row).join('\t'));
                                    sub_row = [];
                                    sub_row.push(rows[row[1]]);
                                }
                                sub_row.push(row[0]);
                                r = row[1];
                            });

                            var sub_col_data = _.map([cols], function (col, idx) {
                                var new_arr = col.slice(min_col, max_col + 1);
                                new_arr.unshift('');
                                return new_arr.join('\t');
                            });

                            var sub_data = [sub_col_data].concat(sub_rows);

                            var reqObj = _.cloneDeep($block.data().req);
                            reqObj.data = sub_data.join('\n');
                            unitManager.branchUnit(null, reqObj);
                            $menuSelector.hide();
                        });
                        //graph create
                        $menuSelector.find('a.species').unbind('click');
                        $menuSelector.find('a.species').on('click', function (e) {
                            ////console.log(this);
                            // open network tab
                            if (!$('.slider-network').hasClass('active')) {
                                $('.slider-network').trigger('click');
                            }
                            var species = $(this).text();
                            var genes = $block.find('select.gene-selector').val();
                            ////console.log(genes);
                            // show table
                            moduleNetwork.getGesa(genes, species);
                            // show netork

                            var dataObj = {
                                req: null,
                                res: null,
                                position: null,
                                gesa: {genes: genes, species: species}
                            };
                            blockId = unitManager.getBlockId();
                            // 블록 파라메터 생성

                            var g_count = _.filter($('.block'), function (item) {
                                    if ($(item).data().req.block_name.indexOf($block.data().req.block_name + "-G") != -1) return true
                                }).length + 1;
                            var reqObj = {
                                // django add color
                                block_iden: blockId,
                                block_name: $block.data().req.block_name + "-G" + g_count,
                                block_ver: 0,
                                username: userManager.USERNAME,
                                session_name: userManager.SESSION,
                                session_ver: userManager.SESSION_VER,
                                project_name: userManager.PROJECT,
                                position: {top: 0, left: 0}
                            };
                            dataObj.req = reqObj;
                            dataObj.position = {top: 0, left: 0};

                            var $newUnit = unitManager.addUnit(dataObj);
                            moduleNetwork.getGraph(genes, species, $newUnit, $block);
                            unitManager.logger('Create-Unit-Graph',unitManager.getLoggerObj({block_name:$newUnit.data().req.block_name, genes:JSON.stringify(genes), species: species}));
                            $menuSelector.hide();
                        });
                        $menuSelector.find('a.gesa-species').unbind('click');
                        $menuSelector.find('a.gesa-species').on('click', function (e) {
                            var species = $(this).text();
                            var genes = $block.find('select.gene-selector').val();
                            // show table
                            if (!$('.slider-network').hasClass('active')) {
                                $('.slider-network').trigger('click');
                            }
                            moduleNetwork.getGesa(genes, species);
                            $menuSelector.hide();
                        });
                    }
                });
                //label columns (Condition name)
                var colG = mySVG.append('g').attr('transform', 'translate(350, 110)');
                var columnLabel = colG.selectAll(".colLabel")
                    .data(cols)
                    .enter().append('svg:text')
                    .attr('transform', function (d, i) {
                        var x = w * i;
                        var y = 10;
                        return "translate(" + x + "," + y + ")rotate(45)";
                    })

                    //              .attr('x', function (d, i) {
                    //            return ((i + 0.5) * w + 75);
                    //          })
                    //        .attr('y', function (d, i) {
                    //      return 30;
                    //          })

                    .attr('class', 'label')
                    .style('text-anchor', 'middle')
                    .text(function (d) {
                        return d;
                    });

                //               columnLabel
                //             .on("mouseover", function () {
                //           d3.select(this).style("font-weight", "bold").style("font-size", "18")
                //         })
                //       .on("mouseout", function () {
                //     d3.select(this).style("font-weight", "").style("font-size", "12")
                //   });

                var drag_start = null;
                var $genes_select = $block.find('select.gene-selector');
                $genes_select.on('change', function (e) {
                    var list = $(this).val();
                    if (list != heatmapG.selectAll('.selected-row').data()) {
                        rowLabel.classed('selected-row', false);
                        rowLabel.filter(function (d, i) {
                            if (list.indexOf(d) != -1) return true;
                        }).classed('selected-row', true);
                    }
                });

                function dragSelectAll(start_gene, end_gene, rowLabel) {
                    $genes_select.off('change');
                    if (rows.indexOf(start_gene) > rows.indexOf(end_gene)) {
                        var temp = start_gene;
                        start_gene = end_gene;
                        end_gene = temp;
                    }
                    var s = false;
                    rowLabel.filter(function (d, i) {
                        if (d == start_gene) s = true;
                        if (d == end_gene) {
                            s = false;
                            return true;
                        }
                        return s;
                    }).classed('selected-row', true);
                    console.log(heatmapG.selectAll('.selected-row').data());
                    $genes_select.selectpicker('val', heatmapG.selectAll('.selected-row').data());
                    drag_start = null;
                    $genes_select.on('change', function (e) {
                        var list = $(this).val();
                        if (list != heatmapG.selectAll('.selected-row').data()) {
                            rowLabel.classed('selected-row', false);
                            rowLabel.filter(function (d, i) {
                                if (list.indexOf(d) != -1) return true;
                            }).classed('selected-row', true);
                        }
                    });
                }

                //label row (Gene name)
                var rowLabel = heatmapG.selectAll(".rowLabel")
                    .data(rows)
                    .enter()
                    .append('g')
                    .on('mouseover', function (d) {
                        var thisrow = d3.select(this);
                        var rect = thisrow.select('rect');
                        rect.attr('fill', 'darkviolet')
                        rect.style('opacity', 0.3);
                        rect.style('cursor', 'pointer');
                    }).on('mouseout', function (d) {
                        var thisrow = d3.select(this);
                        var rect = thisrow.select('rect');
                        rect.attr('fill', 'none');
                    });

                rowLabel
                    .append('svg:text')
                    .attr('x', function (d, i) {
                        return w * cols.length + 1 + 50 + 20;
                    })
                    .attr('y', function (d, i) {
                        return (i * h) + 30 + colLabel_length;
                    })
                    .attr('font-size', '20px')
                    //.attr('class', 'rowLabel')
                    .style('text-anchor', 'start')
                    .text(function (d) {
                        return d;
                    });

                rowLabel
                    .append('rect')
                    .attr('width', '100%')
                    .attr('x', function (d, i) {
                        return w * cols.length + 1 + 50 + 20
                    })
                    .attr('y', function (d, i) {
                        return (i * h) + colLabel_length;
                    })
                    .attr('height', 50)
                    .attr('fill', 'none')
                    .attr('stroke', 'none')
                    .on('click', function (d) {
                        ////console.log(d);
                        if (drag_start) {
                            dragSelectAll(drag_start, d, rowLabel);
                            drag_start = null;
                            return
                        }
                        if (drag_start == null) {
                            d3.select(this.parentNode).classed('selected-row', true);
                            drag_start = d;
                            return
                        }
                        //$(this).toggleClass('selected-row');
                        //moduleNetwork.updateSelection();
                    });


//                 rowLabel
                //               .on("mouseover", function () {
                //             d3.select(this).style("font-weight", "bold").style("font-size", "24").style('color','yellow')
                //           })
                //         .on("mouseout", function () {
                //       d3.select(this).style("font-weight", "").style("font-size", "12").style('color','black')
                //     });


                if (_.has(dataObj.res, 'dendro_path')) {
                    visualizer.makeTree($clusterParam, treeId, "tree", treeHeight, dataObj.res.dendro_path);
                }
                if (_.has(dataObj.res, 'dendro_col_path')) {
                    visualizer.makeColTree($clusterParam, colTreeId, "main", colTreeWidth, dataObj.res.dendro_col_path);
                }
            },
            makeTree: function (clusterName, treeId, treeType, makeTreeHeight, path) {
                //////console.log('makeTree', path);
                var g = d3.select("#" + treeId);
                //////console.log('makeTree', treeId, treeType, makeTreeHeight);
                var tree = d3.cluster()
                    .size([makeTreeHeight, 320])
                    .separation(separation);
                //.nodeSize([50, 15])
                //.separation(separation);

                function separation(a, b) {
                    return a.parent == b.parent ? 1 : 1;
                }

                //This code help to find the parent id in this hierarchy, so change this part.
                var stratify = d3.stratify().parentId(function (d) {
                    return d.id.substring(0, d.id.lastIndexOf("."));
                });
                /*
                 var path = "";
                 if (treeType == "tree") {
                 path = "static/csv/" + clusterName + "tree.csv";
                 } else if (treeType == "subTree") {
                 path = "static/csv/subtree.csv";
                 }
                 */
                //////console.log(path);

                d3.csv(path, function (error, data) {
                    //////console.log("#"+treeId);
                    if (error) throw error;

                    var root = stratify(data);
                    tree(root);

                    var link = g.selectAll(".link").data(root.descendants().slice(1))
                        .enter()
                        .append("path")
                        .attr("class", "link")
                        .style('fill', 'none')
                        .style('stroke', '#555')
                        .style('stroke-opacity', '0.4')
                        .style('stroke-width', '1.5px')
                        .attr("d", function (d) {
                            return "M" + d.y + "," + d.x
                                + " L " + d.parent.y + " " + d.x + " L " + d.parent.y + " " + d.parent.x;
                        });
                    //
                    // link
                    //     .on("mouseover", function (d, i) {
                    //         d3.select(d3.select(this)._groups[0][0]).style("stroke", "black").style("stroke-width", 2)
                    //     })
                    //     .on("mouseout", function () {
                    //         d3.select(this).style("stroke", "").style("stroke-width", "")
                    //     });


                    var node = g.selectAll(".node")
                        .data(root.descendants())
                        .enter().append("g")
                        .attr("class", function (d) {
                            return "node" + (d.children ? " node--internal" : " node--leaf");
                        })
                        .attr("transform", function (d) {
                            return "translate(" + d.y + "," + d.x + ")";
                        });

                    node.append("circle").attr("r", 2.5)
                        .attr("id", "node");
                    /*
                     .on("mouseover", function (d) {
                     d3.select(this).attr("r", 5)
                     })
                     .on("mouseout", function () {
                     d3.select(this).attr("r", 2.5)
                     })
                     .on("click", function (d) {
                     subSVG.selectAll("g").remove();
                     subSVG.selectAll("text").remove();
                     var smallHeatmapURL = basicUrl + "subcreateHeatmap.html";
                     var id = d.id.substring(d.id.lastIndexOf(".") + 1);
                     smallHeatmapURL = smallHeatmapURL + "?nodeId=" + id + "&length=" + rowlength + "&clusterName=" + clusterName;

                     var httpRequest;
                     if (window.XMLHttpRequest) { // 모질라, 사파리등 그외 브라우저, ...
                     httpRequest = new XMLHttpRequest();
                     } else if (window.ActiveXObject) { // IE 8 이상
                     httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
                     }
                     httpRequest.onreadystatechange = function () {
                     if (httpRequest.readyState === 4) {
                     visualizer.createHeatmap(subdata, subcols, subrows, subSVG, "sub");
                     }

                     };
                     httpRequest.open('GET', smallHeatmapURL);
                     ////console.log(smallHeatmapURL);
                     httpRequest.send();
                     location.reload();
                     });
                     */

                    node.append("text").attr("dy", 3).attr("x", function (d) {
                        return d.children ? -8 : 8;
                    })
                        .style("text-anchor", function (d) {
                            return d.children ? "end" : "start";
                        })
                        .text(function (d) {
                            return d.id.substring(d.id.lastIndexOf(".") + 1);
                        });
                    /*
                     .on("mouseover", function () {
                     d3.select(this).style("font-weight", "bold")
                     })
                     .on("mouseout", function () {
                     d3.select(this).style("font-weight", "")
                     })
                     */
                });
            },
            makeColTree: function (clusterName, treeId, treeType, treeWidth, path) {
                //////console.log(treeId);
                //////console.log(treeWidth);
                var g = d3.select("#" + treeId);
                /*
                 if (treeType == "main") {
                 var g = d3.select("#" + treeId);
                 var path = "static/csv/" + clusterName + "coltree.csv";
                 } else if (treeType == "sub") {
                 var g = d3.select("#" + treeId);
                 var path = "static/csv/subcoltree.csv"
                 }
                 */
                var tree = d3.cluster()
                //.nodeSize([50, 25])
                    .size([treeWidth, 50])
                    .separation(separation);

                function separation(a, b) {
                    return a.parent == b.parent ? 1 : 1;
                }

                var stratify = d3.stratify().parentId(function (d) {
                    return d.id.substring(0, d.id.lastIndexOf("."));
                });

                d3.csv(path, function (error, data) {
                    if (error) throw error;

                    var root = stratify(data);
                    tree(root);
                    var link = g.selectAll(".link").data(root.descendants().slice(1))
                        .enter()
                        .append("path")
                        .attr("class", "link")
                        .style('fill', 'none')
                        .style('stroke', '#555')
                        .style('stroke-opacity', '0.4')
                        .style('stroke-width', '1.5px')
                        .attr("d", function (d) {
                            return "M" + d.x + "," + d.y
                                + " L " + d.x + " " + d.parent.y + " L " + d.parent.x + " " + d.parent.y;
                        });
                });
            },
            createPCP: function (dataSet, blockId, $blockVer, $blockName, name, colOrder, selectedIndex) {
                var data = [];
                var colName = [];
                parseCSV(dataSet);

                var margin = {top: 30, right: 10, bottom: 10, left: 10},
                    width = 960 - margin.left - margin.right,
                    height = 500 - margin.top - margin.bottom;
                var $block = $('#' + blockId);
                var dimensions;
                var x = d3.scalePoint().range([0, width]),
                    y = {},
                    dragging = {};

                var brushes = [];
                var brushNum = 0;
                var PCPindexList = [];
                var prevList = [];
                var brushedCol = [];
                var line = d3.line(),
                    axis = d3.axisLeft(x),
                    background,
                    foreground,
                    highlightLine;

                d3.select("#" + blockId).select("div.block-display").html("");
                var originViewBox = "-50 -50 " + ((width) + 100) + " " + (height + 100);
                var svg = d3.select("#" + blockId).select("div.block-display")
                    .append("svg")
                    .attr("width", "100%")
                    .attr("viewBox", originViewBox);
                $block.attr('originViewBox', originViewBox);

                // Extract the list of dimensions and create a scale for each.
                x.domain(dimensions = d3.keys(data[0]).filter(function (d) {
                    return colName[d] !== "name" && (y[d] = d3.scaleLinear()
                            .domain(d3.extent(data, function (p) {
                                return +p[d];
                            }))
                            .range([height, 0]));
                }));


                // Add grey background lines for context.
                background = svg.append("g")
                    .selectAll("path")
                    .data(data)
                    .enter().append("path")
                    .attr("class", function (d, i) {
                        return "background ind_" + i;
                    })
                    .attr("d", path)
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                // Add blue foreground lines for focus.
                foreground = svg.append("g")
                    .selectAll("path")
                    .data(data)
                    .enter().append("path")
                    .attr("class", function (d, i) {
                        return "foreground " + blockId + " ind_" + i;
                    })
                    .attr("d", path)
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


                //Add red hightline
                highlightLine = svg.append("g")
                    .selectAll("path")
                    .data(data)
                    .enter().append("path")
                    .attr("class", function (d, i) {
                        return "highlight selected_" + i
                    })
                    .attr("d", path)
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                d3.selectAll(".highlight").style("opacity", 0);

                // Add a group element for each dimension.
                var g = svg.selectAll(".dimension")
                    .data(dimensions)
                    .enter().append("g")
                    .attr("class", "dimension")
                    .attr("transform", function (d) {
                        return "translate(" + x(d) + ")";
                    })
                    .call(d3.drag()
                        .on("start", function (d) {
                            dragging[d] = x(d);

                            background.attr("visibility", "hidden");
                            changedOrder = [];
                        })
                        .on("drag", function (d) {
                            dragging[d] = Math.min(width, Math.max(0, d3.event.x));
                            foreground.attr("d", path);
                            dimensions.sort(function (a, b) {

                                return position(a) - position(b);
                            });
                            x.domain(dimensions);
                            g.attr("transform", function (d) {
                                return "translate(" + position(d) + ")";
                            })
                        })
                        .on("end", function (d) {
                            delete dragging[d];
                            transition(d3.select(this)).attr("transform", "translate(" + x(d) + ")");
                            transition(foreground).attr("d", path);
                            background
                                .attr("d", path)
                                .transition()
                                .delay(500)
                                .duration(0)
                                .attr("visibility", null);

                            dimensions.forEach(function (d, i) {
                                changedOrder.push((colOrder[d - 1]));
                            })


                            unitManager.logger('Change-PCP-Column', unitManager.getLoggerObj({
                                block_iden: blockId,
                                block_ver: $blockVer,
                                block_name: $blockName,
                                column_order: JSON.stringify(changedOrder)
                            }));

                        })
                    );

                // Add an axis and title.
                g.append("g")
                    .attr("class", "axis")
                    .each(function (d) {
                        d3.select(this).call(d3.axisRight(y[d]));
                    })
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                g.append("text")
                    .style("text-anchor", "middle")
                    .attr("y", -6)
                    .text(function (d) {
                        return colName[colOrder[d - 1]];
                    });

                // Add and store a brush for each axis.
                g.append("g")
                    .attr("class", "brush")
                    .each(function (d) {
                        y[d].brushed = false;
                        brushes[d] = d3.brushY(y[d])
                            .extent([[-10, 0], [10, height]]).on("start", brushstart)
                            .on("brush", brush)
                            .on("end", brushend);

                        d3.select(this).call(brushes[d]);
                    })
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                    .selectAll("rect");


                function position(d) {
                    var v = dragging[d];
                    return v == null ? x(d) : v;
                }

                function transition(g) {
                    return g.transition().duration(500);
                }

                // Returns the path for a given data point.
                function path(d) {
                    return line(dimensions.map(function (p) {
                        return [position(p), y[p](d[p])];
                    }));
                }

                function brushstart(d) {
                    y[d].brushed = false;
                    d3.event.sourceEvent.stopPropagation();
                }


                function brushend(d) {
                    updatebrush();

                    changedSelection = [];

                    if (selectedIndex.length == 0) {
                        PCPindexList.forEach(function (d, i) {
                            changedSelection.push(d + 1);
                        })
                    } else {
                        PCPindexList.forEach(function (d, i) {
                            changedSelection.push(selectedIndex[d]);
                        })
                    }
                    if (brushNum == 0) {
                        d3.selectAll(".foreground").filter("." + blockId).style("display", "inline");
                        d3.selectAll(".highlight").style("opacity", 0);
                    }

                    unitManager.logger('Brush-PCP-Index', unitManager.getLoggerObj({
                        block_iden: blockId,
                        block_ver: $blockVer,
                        block_name: $blockName,
                        selected_index: JSON.stringify(changedSelection),
                        brushed_column: JSON.stringify(brushedCol)
                    }));

                }

                // Handles a brush event, toggling the display of foreground lines.
                function brush(a) {
                    y[a].brushed = true;
                    var s = d3.event.selection || y[a].range();
                    y[a].selection = s;

                    updatebrush();
                }

                function updatebrush() {
                    var actives = dimensions.filter(function (p, i) {
                            return y[p].brushed;
                        }),
                        extents = actives.map(function (p) {

                            return y[p].selection.map(y[p].invert, y[p]);
                        });

                    /* interaction with scatter plot */
                    for (var j = 0; j < actives.length; j++) {
                        PCPindexList = [];
                        data.forEach(function (d, i) {
                            if (data[i][actives[j]] <= extents[j][0] && data[i][actives[j]] >= extents[j][1]) {

                                if (j == 0) {
                                    prevList.push(i);
                                    PCPindexList.push(i);
                                }
                                else {
                                    if (prevList.includes(i))
                                        PCPindexList.push(i);
                                }
                            }
                        });
                        prevList = PCPindexList;
                    }

                    brushNum = actives.length;

                    var foregrounds = d3.selectAll(".foreground").filter("." + blockId).style("display", "none");
                    PCPindexList.forEach(function (d, i) {
                        d3.selectAll(".ind_" + d).filter("." + blockId).style("display", "inline");
                    })

                    brushedCol = [];
                    actives.forEach(function (d, i) {
                        brushedCol.push(colName[d]);
                    })

                }

                function parseCSV(dataSet) {

                    var allRows = dataSet.split(/\r?\n|\r/);
                    if (colOrder.length === 0)
                        colOrder = [1, 2, 3, 4, 5, 6, 7];

                    for (var singleRow = 0; singleRow < allRows.length; singleRow++) {
                        if (singleRow === 0) {
                            var rowCells = allRows[singleRow].split(',');

                            for (var rowCell = 0; rowCell < rowCells.length; rowCell++)
                                colName.push(rowCells[rowCell]);
                        }
                        else {
                            var rowCells = allRows[singleRow].split(',');
                            if (selectedIndex.length == 0) {
                                data.push([rowCells[0], rowCells[colOrder[0]], rowCells[colOrder[1]], rowCells[colOrder[2]], rowCells[colOrder[3]], rowCells[colOrder[4]], rowCells[colOrder[5]], rowCells[colOrder[6]]]);
                            } else {
                                if (selectedIndex.includes(singleRow)) {
                                    data.push([rowCells[0], rowCells[colOrder[0]], rowCells[colOrder[1]], rowCells[colOrder[2]], rowCells[colOrder[3]], rowCells[colOrder[4]], rowCells[colOrder[5]], rowCells[colOrder[6]]]);
                                }
                            }
                        }
                    }
                }

                /* Funtion for interaction */
                this.pcpHighlight = function (idxList) {
                    d3.selectAll(".foreground").style("display", "none");

                    idxList.forEach(function (d, i) {
                        d3.selectAll(".ind_" + idxList[i]).style("display", "inline");
                    })
                }

                this.pcpDeHighlight = function () {
                    d3.selectAll(".foreground").style("display", "inline");
                }

            },
            createSCM: function (dataSet, blockId, $blockVer, $blockName, name, selectedIndex) {
                var data = [];
                var colName = ["name", "economy (mpg)", "cylinders", "displacement (cc)", "power (hp)", "weight (lb)", "0-60 mph (s)", "year"];
                // parseCSV(dataSet);

                var width = 960,
                    size = 200,
                    padding = 20,
                    height = 960;

                var padding = 10;
                var margin = {top: 30, right: 10, bottom: 10, left: 10};

                var $block = $('#' + blockId);
                var SCMindexList = [];
                var brushedCol = [];
                //      this.SPMchangedSelection = [];

                var color = d3.scaleOrdinal(d3.schemeCategory10);


                d3.csv("static/csv/car.csv", function (error, dt) {

                    dt.forEach(function (d, i) {
                        if (selectedIndex.length == 0)
                            data.push([d["name"], +d["economy (mpg)"], +d["cylinders"], +d["displacement (cc)"], +d["power (hp)"], +d["weight (lb)"], +d["0-60 mph (s)"], +d["year"]]);
                        else {
                            if (selectedIndex.includes(i))
                                data.push([d["name"], +d["economy (mpg)"], +d["cylinders"], +d["displacement (cc)"], +d["power (hp)"], +d["weight (lb)"], +d["0-60 mph (s)"], +d["year"]]);
                        }
                    });
                    if (error) throw error;


                    var domainByTrait = {},
                        traits = d3.keys(colName).filter(function (d) {
                            return colName[d] !== "name";
                        }),
                        n = traits.length;

                    traits.forEach(function (trait) {
                        domainByTrait[trait] = d3.extent(data, function (d) {
                            return d[trait];
                        });
                    });

                    var size = width / n;

                    var x = d3.scaleLinear()
                        .range([padding / 2, size - padding / 2]);

                    var y = d3.scaleLinear()
                        .range([size - padding / 2, padding / 2]);

                    var xAxis = d3.axisBottom()
                        .scale(x)
                        .ticks(6);

                    var yAxis = d3.axisLeft()
                        .scale(y)
                        .ticks(6);

                    xAxis.tickSize(size * n);
                    yAxis.tickSize(-size * n);

                    var brush = d3.brush()
                        .on("start", brushstart)
                        .on("brush", brushmove)
                        .on("end", brushend)
                        .extent([[0, 0], [size, size]]);

                    d3.select("#" + blockId).select("div.block-display").html("");
                    var originViewBox = "-50 -50 " + ((width + 100) + " " + (height + 100));
                    var svg = d3.select("#" + blockId).select("div.block-display")
                        .append("svg")
                        .attr("width", "100%")
                        .attr("viewBox", originViewBox)
                        .attr("transform", "translate(" + (margin.left) + "," + margin.top + ")");
                    $block.attr('originViewBox', originViewBox);

                    svg.selectAll(".x.axis")
                        .data(traits)
                        .enter().append("g")
                        .attr("class", "x axisM")
                        .attr("transform", function (d, i) {
                            return "translate(" + (n - i - 1) * size + ",0)";
                        })
                        .each(function (d) {
                            x.domain(domainByTrait[d]);
                            d3.select(this).call(xAxis);
                        });

                    svg.selectAll(".y.axis")
                        .data(traits)
                        .enter().append("g")
                        .attr("class", "y axisM")
                        .attr("transform", function (d, i) {
                            return "translate(0," + i * size + ")";
                        })
                        .each(function (d) {
                            y.domain(domainByTrait[d]);
                            d3.select(this).call(yAxis);
                        });

                    var cell = svg.selectAll(".cell")
                        .data(cross(traits, traits))
                        .enter().append("g")
                        //.attr("width", size)
                        // .attr("height", size)
                        .attr("class", function (d, i) {
                            return "cell ind_" + i;
                        })
                        .attr("transform", function (d) {
                            return "translate(" + (n - d.i - 1) * size + "," + d.j * size + ")";
                        })
                        .each(plot);


                    // Titles for the diagonal.
                    cell.filter(function (d) {
                        return d.i === d.j;
                    }).append("text")
                        .attr("x", padding)
                        .attr("y", padding)
                        .attr("dy", ".71em")
                        .text(function (d) {
                            return colName[d.x];
                        });


                    cell.call(brush);

                    function plot(p) {
                        var cell = d3.select(this);

                        x.domain(domainByTrait[p.x]);
                        y.domain(domainByTrait[p.y]);

                        cell.append("rect")
                            .attr("class", "frame")
                            .attr("x", padding / 2)
                            .attr("y", padding / 2)
                            .attr("width", size - padding)
                            .attr("height", size - padding);


                        cell.selectAll("circle")
                            .data(data)
                            .enter().append("circle")
                            .attr("cx", function (d) {
                                return x(d[p.x]);
                            })
                            .attr("cy", function (d) {
                                return y(d[p.y]);
                            })
                            .attr("r", 2)
                            .style("fill", function (d) {
                                return color(d[0]);
                            });
                    }

                    var brushCell;

                    // Clear the previously-active brush, if any.
                    function brushstart(p) {
                        if (brushCell !== this) {
                            d3.select(brushCell).call(brush.move, null);
                            brushCell = this;
                            x.domain(domainByTrait[p.x]);
                            y.domain(domainByTrait[p.y]);

                            brushedCol = [];
                            brushedCol.push(colName[p.x]);
                            brushedCol.push(colName[p.y]);

                        }
                    }

                    // Highlight the selected circles.
                    function brushmove(p) {
                        var e = d3.brushSelection(this);
                        svg.selectAll("circle").classed("hidden", function (d, i) {
                            return !e
                                ? false
                                : (
                                    e[0][0] > x(+d[p.x]) || x(+d[p.x]) > e[1][0]
                                    || e[0][1] > y(+d[p.y]) || y(+d[p.y]) > e[1][1]
                                );
                        });

                        SCMindexList = [];
                        if (e) {
                            data.forEach(function (d, i) {
                                if (e[0][0] < x(+d[p.x]) && x(+d[p.x]) < e[1][0]
                                    && e[0][1] < y(+d[p.y]) && y(+d[p.y]) < e[1][1])
                                    SCMindexList.push(i);
                            })
                        }
                    }

                    // If the brush is empty, select all circles.
                    function brushend() {
                        var e = d3.brushSelection(this);


                        if (e === null) {
                            svg.selectAll(".hidden").classed("hidden", false);
                            SCMindexList = [];
                        }

                        changedSelection = [];
                        if (selectedIndex.length == 0) {
                            SCMindexList.forEach(function (d, i) {
                                changedSelection.push(d);
                            });
                        }
                        else {
                            SCMindexList.forEach(function (d, i) {
                                changedSelection.push(selectedIndex[d]);
                            });

                        }

                        unitManager.logger('Brush-SCM-Index', unitManager.getLoggerObj({
                            block_iden: blockId,
                            block_ver: $blockVer,
                            block_name: $blockName,
                            selected_index: JSON.stringify(changedSelection),
                            brushed_column: JSON.stringify(brushedCol)
                        }));
                    }
                });

                function cross(a, b) {
                    var c = [], n = a.length, m = b.length, i, j;
                    for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
                    return c;
                }

                function parseCSV(dataSet) {
                    var allRows = dataSet.split(/\r?\n|\r/);

                    for (var singleRow = 0; singleRow < allRows.length; singleRow++) {
                        if (singleRow === 0) {
                            var rowCells = allRows[singleRow].split(',');

                            for (var rowCell = 0; rowCell < rowCells.length; rowCell++)
                                colName.push(rowCells[rowCell]);
                        }
                        else {
                            var rowCells = allRows[singleRow].split(',');
                            if (selectedIndex.length == 0) {
                                data.push([rowCells[0], rowCells[1], rowCells[2], rowCells[3], rowCells[4], rowCells[5], rowCells[6], rowCells[7]]);
                            } else {
                                if (selectedIndex.includes(singleRow)) {
                                    data.push([rowCells[0], rowCells[1], rowCells[2], rowCells[3], rowCells[4], rowCells[5], rowCells[6], rowCells[7]]);

                                }
                            }
                        }
                    }
                }

                /* Funtion for interaction */
                this.scmHighlight = function (idxList) {
                    d3.selectAll("circle").classed("hidden", true);

                    idxList.forEach(function (d, i) {
                        d3.selectAll(".ind_" + idxList[i]).classed("hidden", false)
                    })
                }

                this.scmDeHighlight = function () {
                    d3.selectAll("circle").classed("hidden", false);
                }

            }
        });
})(visualizer);