(function (parent) {
    _.extend(parent,
        {
            createSessionTree: function (sankeyData, height, width) {
                if (init_history_panel) return;
                //console.log('session');
                //console.log(sankeyData);
                d3.select('.nodeTooltip').remove();


                // setup containers
                visualizer.P_SANKEY = null;
                visualizer.U_SANKEY = null;
                visualizer.ZOOM_SANKEY = null;

                var $container = $('#history_tree');
                $container.remove();
                $container = $('<svg id="history_tree" width="100%" height="100%"></svg>');
                $('.history-tree-container').append($container);

                //var w = $container.width();
                //var h = $container.height();


                var h = 343;
                var width = h, height = h / 2, padding = 2.5;
                var nodeWidth = 10;
                var sourceX, sourceY;
                var zoom_fun = d3.zoom().scaleExtent([1, 8]).on('zoom', zoomed);

                var legend_tab = d3.select('#history_tree')
                    .append('g')
                    .attr('class', 'legend_menu')
                    .attr('transform', 'translate(55,0)');
                var svg = d3.select($container.get(0));
                svg.call(zoom_fun);
                var originTransform = 'translate(' + ($container.width() - h / 2) / 2 + ',' + 200 + ')' // legend height 200
                var project = svg.append('g')
                //.attr('transform', originTransform)
                    .attr('id', 'project-tree');
                visualizer.P_SANKEY = project;
                //console.log('test', $container, svg, project)
                //console.log('translateBy - proj', ($container.width() - h / 2) / 2);
                zoom_fun.translateBy(svg, ($container.width() - h / 2) / 2, 200);
                function zoomed() {
                    if (!$('#project-tree').hasClass('mini')) {
                        visualizer.P_SANKEY.attr('transform', d3.event.transform);
                    }
                    if (visualizer.U_SANKEY) {
                        visualizer.U_SANKEY.attr('transform', d3.event.transform);
                    }
                }

                visualizer.ZOOM_SANKEY = zoom_fun;

                // end setup


                var book = false;

                //var wid = $('div.history-tree-container')[0].getBoundingClientRect().width;
                var wid = 549;

                var fromFlag = false, toFlag = false;
                var ht = 343;

                var root = d3.hierarchy(sankeyData, function (d) {
                    return d.children;
                });

                root = d3.hierarchy(sankeyData, function (d) {
                    return d.parent;
                });

                var actionTest = function (root) {
                    var from = d3.select('rect.history-from').data();
                    var to = d3.select('rect.history-to').data();
                    userManager.ROOT = root;
                    if (from.length != 0 && to.length != 0) {
                        //console.log('actionTest');
                        historyManager.getActionHistory(searchNode(from[0], to[0], []));
                    }
                };

                var searchNode = function (from, to, list) {
                    var node = {
                        session_name: to.name,
                        session_ver: to.ver
                    };
                    list.unshift(node);

                    if (from == to)
                        return list;

                    if (to.parent.id == from.id) {
                        list.unshift({
                            session_name: from.name,
                            session_ver: from.ver
                        });
                        //console.log(list);
                        return list;
                    }
                    return searchNode(from, to.parent, list);
                };

                var menu = [
                    {
                        title: 'Start Here',
                        action: function (d) {
                            if (!fromFlag) {
                                d3.selectAll('.nodeblock').classed('history-from', false);
                                d3.select(d).classed('history-from', true);
                                d3.select(d).style('fill', 'orange');
                                fromFlag = true;
                            }
                            else {
                                d3.select('.nodeblock.history-from').attr('class', 'nodeblock').style('fill', 'steelblue');
                                d3.selectAll('.node').classed('history-from', false);
                                d3.select(d).classed('history-from', true);
                                d3.select(d).style('fill', 'orange');
                            }

                            if (fromFlag == true && toFlag == true)
                                actionTest(root);
                        }
                    },
                    {
                        title: 'End Here',
                        action: function (d) {
                            if (!toFlag) {
                                d3.selectAll('.nodeblock').classed('history-to', false);
                                d3.select(d).classed('history-to', true);
                                d3.select(d).style('fill', 'yellow');
                                toFlag = true;
                            }
                            else {
                                d3.select('.nodeblock.history-to').attr('class', 'nodeblock').style('fill', 'steelblue');
                                d3.selectAll('.node').classed('history-to', false);
                                d3.select(d).classed('history-to', true);
                                d3.select(d).style('fill', 'yellow');
                            }

                            if (fromFlag == true && toFlag == true)
                                actionTest(root);
                        }
                    },
                    {
                        title: 'Unit Workflow',
                        action: function (d) {
                            var data = d3.select(d).data()[0];
                            // show this session
                            visualizer.showSession(data);
                            /*
                             d3.select('#history_tree').remove();
                             d3.select('.history-tree-container')
                             .append('svg')
                             .attr('id', 'history_tree')
                             .attr('width', '100%')
                             .attr('height', '100%')
                             .attr('opacity', 0);

                             update();
                             */
                            visualizer.transformToMiniMap();
                            //$('#unit-legend').empty();
                            visualizer.D_SANKEY = {id: data.name, ver: data.ver};
                            historyManager.getUnitHistory(data.name, data.ver);

                            unitManager.logger('Unit-Workflow', {
                                username: userManager.USERNAME,
                                project_name: userManager.PROJECT,
                                session_name: userManager.SESSION,
                                session_ver: data.ver
                            });
                        }
                    }, {
                        title: 'Branch Session',
                        action: function (d) {
                            var data = d3.select(d).data()[0];
                            var sessionObj = {
                                username: userManager.USERNAME,
                                project_name: userManager.PROJECT,
                                session_name: null,
                                parent_session_name: data.name,
                                parent_session_ver: data.ver
                            };
                            historyManager.SESSION = sessionObj;
                            //enter sankey-mode
                            $('#session-modal').addClass('mode-sankey');
                            //userManager.branchSession(userManager.SESSION + "-" + userManager.SESSION + "-branch");
                            userManager.btnBranchSession();
                        }
                    },
                    {
                        title: 'Book mark',
                        action: function (d) {
                            var data = d3.select(d).data()[0];
                            console.log('data')
                            console.log(data)

                            if(!data.bookmark){
                                $.ajax({
                                    url: "bookmark.html",
                                    method: "post",
                                    data: {
                                        username: userManager.USERNAME,
                                        project_name: userManager.PROJECT,
                                        session_name: data.name,
                                        session_ver: data.ver
                                    },
                                    error: userManager.failAjax,
                                    success: console.log('ok')
                                });
                            }
                            else {
                                $.ajax({
                                    url: "delBookmark.html",
                                    method: "post",
                                    data: {
                                        username: userManager.USERNAME,
                                        project_name: userManager.PROJECT,
                                        session_name: data.name,
                                        session_ver: data.ver
                                    },
                                    error: userManager.failAjax,
                                    success: console.log('ok2')
                                });
                            }

                            historyManager.getSessionHistory();
                        }
                    },
                    {
                        title: 'Refresh Project',
                        action: function (d) {
                            historyManager.getSessionHistory();
                        }
                    }
                ];


                //------------------------------------------------------------------------------
                //$('#history_tree').empty();

                //-------------legend menu-------------

                var legend_menu = [
                    {'tab': 'MANAGEMENT', 'color': '#377eb8', 'rcolor': 'black'},
                    {'tab': 'ANALYSIS', 'color': '#4daf4a', 'rcolor': 'black'},
                    {'tab': 'ANNOTATION', 'color': '#984ea3', 'rcolor': 'black'},
                    {'tab': 'HISTORY', 'color': '#ff7f00', 'rcolor': 'black'}
                ];
                var mgt = [
                    {'tab': 'Create-Project', 'color': '#e41a1c'},
                    {'tab': 'Delete-Project', 'color': '#377eb8'},
                    {'tab': 'Create-Session', 'color': '#4daf4a'},
                    {'tab': 'Delete-Session', 'color': '#984ea3'},
                    {'tab': 'Apply-Unit', 'color': '#ff7f00'},
                    {'tab': 'Save-Session', 'color': '#ffff33'},
                    {'tab': 'Create-Unit', 'color': '#a65628'},
                    {'tab': 'Delete-Unit', 'color': '#f781bf'},
                    {'tab': 'Save-Unit', 'color': '#a6cee3'}
                ];
                var als = [
                    {'tab': 'Branch-Session', 'color': '#66c2a5'},
                    {'tab': 'Change-Data', 'color': '#fc8d62'},
                    {'tab': 'Change-Cluster-Type', 'color': '#8da0cb'},
                    {'tab': 'Change-Color', 'color': '#e78ac3'},
                    {'tab': 'Change-Unit-Name', 'color': '#a6d854'},
                    {'tab': 'Branch-Unit', 'color': '#ffd92f'},
                    {'tab': 'Restore-Unit', 'color': '#1f78b4'},
                    {'tab': 'Create-Unit-Graph', 'color': '#e31a1c'},
                    {'tab': 'Change-Cluster-Parameter', 'color': '#a6761d'}
                ];
                var anno = [
                    {'tab': 'Update-Unit-Annotation', 'color': '#984ea3'},
                    {'tab': 'Create-Unit-Annotation', 'color': '#fc8d62'},
                    {'tab': 'Delete-Unit-Annotation', 'color': '#8da0cb'},
                    {'tab': 'Change-Session-Annotation', 'color': '#66c2a5'}
                ];
                var his = [
                    {'tab': 'Show-Session', 'color': '#8dd3c7'},
                    {'tab': 'Undo-Unit', 'color': '#ffffb3'},
                    {'tab': 'Redo-Unit', 'color': '#bebada'},
                    {'tab': 'Move-Unit', 'color': '#fb8072'},
                    {'tab': 'Copy-Unit', 'color': '#80b1d3'}
                ];

                var legendData2 = {};
                var catData = {};
                mgt.forEach(function (elm) {
                    legendData2[elm['tab']] = '#377eb8';
                    catData[elm['tab']] = 'mgt';
                });
                als.forEach(function (elm) {
                    legendData2[elm['tab']] = '#4daf4a';
                    catData[elm['tab']] = 'als';
                });
                anno.forEach(function (elm) {
                    legendData2[elm['tab']] = '#984ea3';
                    catData[elm['tab']] = 'anno';
                });
                his.forEach(function (elm) {
                    legendData2[elm['tab']] = '#ff7f00';
                    catData[elm['tab']] = 'his';
                });

                var back_wid = wid * 3 / 4;
                var tab_wid = (wid * 3 / 4 - 50) / 4;

                var legend_background = legend_tab.append('rect')
                    .attr('class', 'legend_background')
                    .style('width', back_wid)
                    .style('height', '50px')
                    .style('opacity', .1)
                    .style('fill', 'gray')
                    .attr('transform', 'translate(' + wid / 8 + ',' + '30)')
                    .attr('rx', 15)
                    .attr('ry', 15);

                var tab_menu = legend_tab
                    .append('g')
                    .selectAll('.tab_menu')
                    .data(legend_menu)
                    .enter()
                    .append('rect')
                    .attr('class', function (d, i) {
                        return 'tab_menu' + i;
                    })
                    .style('width', tab_wid)
                    .style('height', 20)
                    .style('fill', function (d) {
                        return d.color;
                    })
                    .attr('transform', function (d, i) {
                        return 'translate(' + (wid / 8 + 10 + i * (tab_wid + 10)) + ',45)';
                    })
                    .attr('rx', 5)
                    .attr('ry', 5);

                tab_menu.transition();

                var tab_text = legend_tab
                    .append('g')
                    .selectAll('.tab_menu_text')
                    .data(legend_menu)
                    .enter()
                    .append('text')
                    .attr('class', function (d, i) {
                        return 'tab_text' + i;
                    })
                    .text(function (d) {
                        return d.tab;
                    })
                    .attr('font-family', 'sans-serif')
                    .attr('font-size', '10px')
                    .attr('stroke', function (d) {
                        return d.rcolor;
                    })
                    .attr('transform', function (d, i) {
                        return 'translate(' + (wid / 8 + 10 + tab_wid / 2 + i * (tab_wid + 10)) + ',60)';
                    })
                    .style('text-anchor', 'middle');

                tab_text.transition();

                tab_menu.on('mouseover', function (d, i) {
                    d3.select('.tab_menu' + i).style('fill', d.rcolor);
                    d3.select('.tab_text' + i).style('stroke', d.color);
                })
                    .on('mouseout', function (d, i) {
                        d3.select('.tab_menu' + i).style('fill', d.color);
                        d3.select('.tab_text' + i).style('stroke', d.rcolor);
                    });

                tab_text.on('mouseover', function (d, i) {
                    d3.select('.tab_menu' + i).style('fill', d.rcolor);
                    d3.select('.tab_text' + i).style('stroke', d.color);
                })
                    .on('mouseout', function (d, i) {
                        d3.select('.tab_menu' + i).style('fill', d.color);
                        d3.select('.tab_text' + i).style('stroke', d.rcolor);
                    });

                function link_refresh() {
                    d3.selectAll('.smgt').style('opacity', 1).style('stroke', '#377eb8');
                    d3.selectAll('.sals').style('opacity', 1).style('stroke', '#4daf4a');
                    d3.selectAll('.sanno').style('opacity', 1).style('stroke', '#984ea3');
                    d3.selectAll('.shis').style('opacity', 1).style('stroke', '#ff7f00');
                    d3.selectAll('#linkS').style('opacity', .1);
                    tab_refresh();
                }

                function mgt_refresh() {
                    mgt.forEach(function (management) {
                        d3.selectAll('.' + management.tab)
                            .style('stroke', management.color)
                            .style('opacity', 1);
                    });
                    d3.select('.tab_menu1').style('opacity', .2);
                    d3.select('.tab_menu2').style('opacity', .2);
                    d3.select('.tab_menu3').style('opacity', .2);
                    d3.select('.tab_text1').style('opacity', .2);
                    d3.select('.tab_text2').style('opacity', .2);
                    d3.select('.tab_text3').style('opacity', .2);
                }

                function als_refresh() {
                    als.forEach(function (analysis) {
                        d3.selectAll('.' + analysis.tab)
                            .style('stroke', analysis.color)
                            .style('opacity', 1);
                    });
                    d3.select('.tab_menu0').style('opacity', .2);
                    d3.select('.tab_menu2').style('opacity', .2);
                    d3.select('.tab_menu3').style('opacity', .2);
                    d3.select('.tab_text0').style('opacity', .2);
                    d3.select('.tab_text2').style('opacity', .2);
                    d3.select('.tab_text3').style('opacity', .2);
                }

                function anno_refresh() {
                    anno.forEach(function (annotation) {
                        d3.selectAll('.' + annotation.tab)
                            .style('stroke', annotation.color)
                            .style('opacity', 1);
                    });
                    d3.select('.tab_menu0').style('opacity', .2);
                    d3.select('.tab_menu1').style('opacity', .2);
                    d3.select('.tab_menu3').style('opacity', .2);
                    d3.select('.tab_text0').style('opacity', .2);
                    d3.select('.tab_text1').style('opacity', .2);
                    d3.select('.tab_text3').style('opacity', .2);
                }

                function his_refresh() {
                    his.forEach(function (history) {
                        d3.selectAll('.' + history.tab)
                            .style('stroke', history.color)
                            .style('opacity', 1);
                    });
                    d3.select('.tab_menu0').style('opacity', .2);
                    d3.select('.tab_menu1').style('opacity', .2);
                    d3.select('.tab_menu2').style('opacity', .2);
                    d3.select('.tab_text0').style('opacity', .2);
                    d3.select('.tab_text1').style('opacity', .2);
                    d3.select('.tab_text2').style('opacity', .2);
                }

                function tab_refresh() {
                    d3.select('.tab_menu0').style('opacity', 1);
                    d3.select('.tab_menu1').style('opacity', 1);
                    d3.select('.tab_menu2').style('opacity', 1);
                    d3.select('.tab_menu3').style('opacity', 1);
                    d3.select('.tab_text0').style('opacity', 1);
                    d3.select('.tab_text1').style('opacity', 1);
                    d3.select('.tab_text2').style('opacity', 1);
                    d3.select('.tab_text3').style('opacity', 1);
                }


                var click = false;
                var tab0 = 0;
                var legend_rect0;

                function tabZero(d) {
                    if (tab0 % 2 == 0) {
                        d3.selectAll('#linkS').style('opacity', .1);
                        mgt_refresh();

                        legend_background.style('height', '140px');
                        legend_rect0 = legend_tab.append('g').attr('class', 'mgt').selectAll('management')
                            .data(mgt)
                            .enter().append('rect')
                            .attr('class', 'management')
                            .style('width', 10)
                            .style('height', 10)
                            .style('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 4;
                                var k = Math.floor(i / 4);
                                return 'translate(' + (wid / 8 + 20 + j * (tab_wid + 10)) + ',' + (k * 20 + 90) + ')';
                            })
                            .style('fill', function (d) {
                                return d.color;
                            })
                            .on('mouseover', function (d) {
                                if (!click) {
                                    d3.select(this).style('fill-opacity', .1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    d3.selectAll('.' + d.tab).style('opacity', 1)
                                        .style('stroke', d.color);
                                }
                            })
                            .on('mouseout', function (d) {
                                if (!click) {
                                    d3.selectAll('.management').style('fill-opacity', 1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    mgt_refresh();
                                }
                            })
                            .on('click', function (d) {
                                if (click == false) click = true;
                                else click = false;
                            });

                        d3.select('.mgt').selectAll('mgt_list')
                            .data(mgt)
                            .enter().append('text')
                            .text(function (d) {
                                return d.tab;
                            })
                            .attr('font-family', 'sans-serif')
                            .attr('font-size', '10px')
                            .attr('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 4;
                                var k = Math.floor(i / 4);
                                return 'translate(' + (wid / 8 + 35 + j * (tab_wid + 10)) + ',' + (k * 20 + 98) + ')';
                            })
                    }
                    else {
                        legend_background.style('height', '50px');
                        d3.select('.mgt').remove();
                        legend_rect0.attr('class', function (d) {
                            d3.selectAll('.smgt').style('opacity', 1)
                                .style('stroke', legendData2[d.tab]);
                        });
                        click = false;
                        tab_refresh();
                    }
                    tab0++;
                    if (tab1 % 2 == 1 || tab2 % 2 == 1 || tab3 % 2 == 1) {
                        if (tab1 % 2 == 1) {
                            d3.select('.als').remove();
                            tab1++;
                            link_refresh();
                            mgt_refresh();
                        }
                        if (tab2 % 2 == 1) {
                            d3.select('.anno').remove();
                            tab2++;
                            link_refresh();
                            mgt_refresh();
                        }
                        if (tab3 % 2 == 1) {
                            d3.select('.his').remove();
                            tab3++;
                            link_refresh();
                            mgt_refresh();
                        }

                        click = false;
                    }

                    if (tab0 % 2 == 0 && tab1 % 2 == 0 && tab2 % 2 == 0 && tab3 % 2 == 0)
                        d3.selectAll('#linkS').style('opacity', 1);
                }

                d3.select('.tab_menu0').on('click', function (d) {
                    tabZero(d);
                });
                d3.select('.tab_text0').on('click', function (d) {
                    tabZero(d);
                });

                var tab1 = 0;
                var legend_rect1;

                function tabOne(d) {
                    if (tab1 % 2 == 0) {
                        d3.selectAll('#linkS').style('opacity', .1);
                        als_refresh();

                        legend_background.style('height', '140px');
                        legend_rect1 = legend_tab.append('g').attr('class', 'als').selectAll('analysis')
                            .data(als)
                            .enter().append('rect')
                            .attr('class', 'analysis')
                            .style('width', 10)
                            .style('height', 10)
                            .style('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 3;
                                var k = Math.floor(i / 3);
                                return 'translate(' + (wid / 8 + 20 + j * (tab_wid * 4 / 3 + 10)) + ',' + (k * 20 + 90) + ')';
                            })
                            .style('fill', function (d) {
                                return d.color;
                            })
                            .on('mouseover', function (d) {
                                if (!click) {
                                    d3.select(this).style('fill-opacity', .1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    d3.selectAll('.' + d.tab).style('opacity', 1)
                                        .style('stroke', d.color);
                                }
                            })
                            .on('mouseout', function (d) {
                                if (!click) {
                                    d3.selectAll('.analysis').style('fill-opacity', 1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    als.forEach(function (analysis) {
                                        d3.selectAll('.' + analysis.tab)
                                            .style('stroke', analysis.color)
                                            .style('opacity', 1);
                                    });
                                }
                            })
                            .on('click', function (d) {
                                if (click == false) click = true;
                                else click = false;
                            });
                        d3.select('.als').selectAll('als_list')
                            .data(als)
                            .enter().append('text')
                            .text(function (d) {
                                return d.tab;
                            })
                            .attr('font-family', 'sans-serif')
                            .attr('font-size', '10px')
                            .attr('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 3;
                                var k = Math.floor(i / 3);
                                return 'translate(' + (wid / 8 + 35 + j * (tab_wid * 4 / 3 + 10)) + ',' + (k * 20 + 98) + ')';
                            })
                    }
                    else {
                        legend_background.style('height', '50px');
                        d3.select('.als').remove();
                        legend_rect1.attr('class', function (d) {
                            d3.selectAll('.sals').style('opacity', 1)
                                .style('stroke', legendData2[d.tab]);
                        });
                        click = false;
                        tab_refresh();
                    }
                    tab1++;
                    if (tab0 % 2 == 1 || tab2 % 2 == 1 || tab3 % 2 == 1) {
                        if (tab0 % 2 == 1) {
                            d3.select('.mgt').remove();
                            tab0++;
                            link_refresh();
                            als_refresh();
                        }
                        if (tab2 % 2 == 1) {
                            d3.select('.anno').remove();
                            tab2++;
                            link_refresh();
                            als_refresh();
                        }
                        if (tab3 % 2 == 1) {
                            d3.select('.his').remove();
                            tab3++;
                            link_refresh();
                            als_refresh();
                        }
                        click = false;
                    }

                    if (tab0 % 2 == 0 && tab1 % 2 == 0 && tab2 % 2 == 0 && tab3 % 2 == 0)
                        d3.selectAll('#linkS').style('opacity', 1);
                }

                d3.select('.tab_menu1').on('click', function (d) {
                    tabOne(d);
                });
                d3.select('.tab_text1').on('click', function (d) {
                    tabOne(d);
                });

                var tab2 = 0;
                var legend_rect2;

                function tabTwo(d) {
                    if (tab2 % 2 == 0) {
                        d3.selectAll('#linkS').style('opacity', .1);
                        anno_refresh();

                        legend_background.style('height', '110px');
                        legend_rect2 = legend_tab.append('g').attr('class', 'anno').selectAll('annotation')
                            .data(anno)
                            .enter().append('rect')
                            .attr('class', 'annotation')
                            .style('width', 10)
                            .style('height', 10)
                            .style('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 3;
                                var k = Math.floor(i / 3);
                                return 'translate(' + (wid / 8 + 20 + j * (tab_wid * 4 / 3 + 10)) + ',' + (k * 20 + 90) + ')';
                            })
                            .style('fill', function (d) {
                                return d.color;
                            })
                            .on('mouseover', function (d) {
                                if (!click) {
                                    d3.select(this).style('fill-opacity', .1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    d3.selectAll('.' + d.tab).style('opacity', 1)
                                        .style('stroke', d.color);
                                }
                            })
                            .on('mouseout', function (d) {
                                if (!click) {
                                    d3.selectAll('.annotation').style('fill-opacity', 1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    anno_refresh();
                                }
                            })
                            .on('click', function (d) {
                                if (click == false)
                                    click = true;
                                else
                                    click = false;
                            });
                        d3.select('.anno').selectAll('anno_list')
                            .data(anno)
                            .enter().append('text')
                            .text(function (d) {
                                return d.tab;
                            })
                            .attr('font-family', 'sans-serif')
                            .attr('font-size', '10px')
                            .attr('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 3;
                                var k = Math.floor(i / 3);
                                return 'translate(' + (wid / 8 + 35 + j * (tab_wid * 4 / 3 + 10)) + ',' + (k * 20 + 98) + ')';
                            })
                    }
                    else {
                        legend_background.style('height', '50px');
                        d3.select('.anno').remove();
                        legend_rect2.attr('class', function (d) {
                            d3.selectAll('.sanno').style('opacity', 1)
                                .style('stroke', legendData2[d.tab]);
                        });
                        click = false;
                        tab_refresh();
                    }
                    tab2++;
                    if (tab0 % 2 == 1 || tab1 % 2 == 1 || tab3 % 2 == 1) {
                        if (tab0 % 2 == 1) {
                            d3.select('.mgt').remove();
                            tab0++;
                            link_refresh();
                            anno_refresh();
                        }
                        if (tab1 % 2 == 1) {
                            d3.select('.als').remove();
                            tab1++;
                            link_refresh();
                            anno_refresh();
                        }
                        if (tab3 % 2 == 1) {
                            d3.select('.his').remove();
                            tab3++;
                            link_refresh();
                            anno_refresh();
                        }
                        click = false;
                    }

                    if (tab0 % 2 == 0 && tab1 % 2 == 0 && tab2 % 2 == 0)
                        d3.selectAll('#linkS').style('opacity', 1);
                }

                d3.select('.tab_menu2').on('click', function (d) {
                    tabTwo(d);
                });
                d3.select('.tab_text2').on('click', function (d) {
                    tabTwo(d);
                });

                var tab3 = 0;
                var legend_rect3;

                function tabThree(d) {
                    if (tab3 % 2 == 0) {
                        d3.selectAll('#linkS').style('opacity', .1);
                        his_refresh();

                        legend_background.style('height', '110px');
                        legend_rect3 = legend_tab.append('g').attr('class', 'his').selectAll('history')
                            .data(his)
                            .enter().append('rect')
                            .attr('class', 'history')
                            .style('width', 10)
                            .style('height', 10)
                            .style('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 4;
                                var k = Math.floor(i / 4);
                                return 'translate(' + (wid / 8 + 20 + j * (tab_wid + 10)) + ',' + (k * 20 + 90) + ')';
                            })
                            .style('fill', function (d) {
                                return d.color;
                            })
                            .on('mouseover', function (d) {
                                if (!click) {
                                    d3.select(this).style('fill-opacity', .1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    d3.selectAll('.' + d.tab).style('opacity', 1)
                                        .style('stroke', d.color);
                                }
                            })
                            .on('mouseout', function (d) {
                                if (!click) {
                                    d3.selectAll('.history').style('fill-opacity', 1);
                                    d3.selectAll('#linkS').style('opacity', .1);
                                    his_refresh();
                                }
                            })
                            .on('click', function (d) {
                                if (click == false)
                                    click = true;
                                else
                                    click = false;
                            });
                        d3.select('.his').selectAll('his_list')
                            .data(his)
                            .enter().append('text')
                            .text(function (d) {
                                return d.tab;
                            })
                            .attr('font-family', 'sans-serif')
                            .attr('font-size', '10px')
                            .attr('stroke', 'black')
                            .attr('transform', function (d, i) {
                                var j = i % 4;
                                var k = Math.floor(i / 4);
                                return 'translate(' + (wid / 8 + 35 + j * (tab_wid + 10)) + ',' + (k * 20 + 98) + ')';
                            })
                    }
                    else {
                        legend_background.style('height', '50px');
                        d3.select('.his').remove();
                        legend_rect3.attr('class', function (d) {
                            d3.selectAll('.shis').style('opacity', 1)
                                .style('stroke', legendData2[d.tab]);
                        });
                        click = false;
                        tab_refresh();
                    }
                    tab3++;
                    if (tab0 % 2 == 1 || tab1 % 2 == 1 || tab2 % 2 == 1) {
                        if (tab0 % 2 == 1) {
                            d3.select('.mgt').remove();
                            tab0++;
                            link_refresh();
                            his_refresh();
                        }
                        if (tab1 % 2 == 1) {
                            d3.select('.als').remove();
                            tab1++;
                            link_refresh();
                            his_refresh();
                        }
                        if (tab2 % 2 == 1) {
                            d3.select('.anno').remove();
                            tab2++;
                            link_refresh();
                            his_refresh();
                        }
                        click = false;
                    }

                    if (tab0 % 2 == 0 && tab1 % 2 == 0 && tab2 % 2 == 0 && tab3 % 2 == 0)
                        d3.selectAll('#linkS').style('opacity', 1);
                }

                d3.select('.tab_menu3').on('click', function (d) {
                    tabThree(d);
                });
                d3.select('.tab_text3').on('click', function (d) {
                    tabThree(d);
                });


                //---------------


                var sankey = d3.sankey()
                    .nodeWidth(nodeWidth)
                    .nodePadding(padding)
                    .sankeyHeight(height)
                    .size([width, height]);

                sankey.data(sankeyData)
                    .sessionLayout();

                update();

                function update() {

                    var unit = svg.append('g')
                        .attr('id', 'unit-sankey');

                    var legend = svg.append('g')
                        .attr('id', 'unit-legend');


                    function actionNum(d) {
                        var most, m = 0, a = 0, an = 0, h = 0;

                        if (d.action_list != null) {
                            d.action_list.forEach(function (action) {
                                if (catData[action.action] == 'mgt')
                                    m++;
                                else if (catData[action.action] == 'als')
                                    a++;
                                else if (catData[action.action] == 'anno')
                                    an++;
                                else
                                    h++;
                            });

                            if (m >= a) most = m;
                            else most = a;
                            if (most >= an) {
                            }
                            else most = an;
                            if (most >= h) {
                            }
                            else most = h;

                            if (most == m) most = 'MANAGEMENT';
                            else if (most == a) most = 'ANALYSIS';
                            else if (most == an) most = 'ANNOTATION';
                            else most = 'HISTORY';

                            return most;
                        }
                        else
                            return null;
                    }

                    // link
                    var linkBackground = project.append('g').selectAll('linkB')
                        .data(sankey.linkBackground)
                        .enter()
                        .append('path')
                        .attr('d', sankey.link())
                        .style('fill', '#eee');

                    //link
                    var link = project.append('g').selectAll('.linkS')
                        .data(sankey.links)
                        .enter()
                        .append('g')
                        .append('path')
                        .attr('id', 'linkS')
                        .attr('class', function (d) {
                            return 's' + catData[d.action] + ' ' + d.action;
                        })
                        .style('stroke', function (d) {
                            return legendData2[d.action];
                        })
                        .attr('d', sankey.link());

                    var node = project.append('g').selectAll('.node')
                        .data(sankey.nodes)
                        .enter()
                        .append('g')
                        .attr('class', 'node')
                        .append('rect')
                        .attr('class', 'nodeblock')
                        .attr('id', function (d, i) {
                            return 'sr' + i;
                        })
                        .attr('height', nodeWidth)
                        .attr('width', function (d) {
                            return d.height;
                        })
                        .attr('transform', function (d, i) {
                            if (i == 0) {
                                sourceX = d.x;
                                sourceY = d.y;
                            }
                            return 'translate(' + d.x + ',' + d.y + ')';
                        })
                        .style('fill', function (d, i) {
                            if (actionNum(d) == null)
                                return 'steelblue';
                            else {
                                var tmp = actionNum(d);
                                if (tmp == 'MANAGEMENT')
                                    return legend_menu[0].color;
                                else if (tmp == 'ANALYSIS')
                                    return legend_menu[1].color;
                                else if (tmp == 'ANNOTATION')
                                    return legend_menu[2].color;
                                else
                                    return legend_menu[3].color;
                            }
                        })
                        .style('stroke', 'black')
                        .style('fill-opacity', .9)
                        .on('contextmenu', d3.contextMenu(menu));

                    // show this session event by skyjin
                    node.on('mousedown', function (d, i) {
                        if (d3.event.button == 0) {
                            visualizer.showSession(d);

                            // call unit action history
                            historyManager.getActionHistory([{session_name: d.name, session_ver: d.ver}]);
                        }

                        d3.selectAll('.nodeblock').attr('stroke-width', 1);
                        d3.select('#sr' + i).attr('stroke-width', 2);
                    });

                    // node mouse over, drag
                    node.on('mouseover', function (d) {
                        // tooltip
                        var tooltip = d3.select('#slider-history')
                            .append('div')
                            .attr('class', 'nodeTooltip')
                            .style('opacity', 0);
                        //console.log(d);
                        tooltip.style('width', '230px')
                            .style('height', '80px')
                            .style('left', d3.event.x + 30 + 'px')
                            .style('top', d3.event.y + 'px')
                            .html('NAME : ' + d.name + '<br>' +
                                'LAST DATE : ' + d.last_date + "<br>" +
                                'VER : ' + d.ver + "<br>" +
                                'ACTION NUM : ' + d.action_num)
                            .transition()
                            .style('opacity', 1);

                        // hierarchy
                        d3.select(this)
                            .style('fill-opacity', .5);

                        var s = d.source;
                        while (s >= -1) {
                            d3.select('#sr' + s)
                                .style('fill-opacity', .5);

                            if (s != -1)
                                s = sankey.nodes()[s].source;
                            else
                                s = -2;
                        }
                    })
                        .on('mouseout', function (d, i) {
                            d3.select('.nodeTooltip').remove();

                            d3.select(this)
                                .style('fill-opacity', .9);
                            var s = d.source;
                            while (s >= -1) {
                                d3.select('#sr' + s)
                                    .style('fill-opacity', .9);

                                if (s != -1)
                                    s = sankey.nodes()[s].source;
                                else
                                    s = -2;
                            }
                        });

                    var bookmark = d3.selectAll('.node')
                        .append('g')
                        .attr('class', 'bookmark')
                        .append('path')
                        .attr('d', d3.symbol().type(d3.symbolStar).size(function (d) {
                            if(d.bookmark){
                                return 40;
                            }
                            else {
                                return 0;
                            }
                        }))
                        .attr('transform', function (d, i) {
                            return 'translate(' + d.x + ',' + (d.y+10) + ')';
                        })
                        .attr('fill', 'red')
                        .attr('stroke', 'black');

                    // symbol
                    var symbol = d3.selectAll('.node')
                        .append('g')
                        .attr('class', 'star')
                        .append('path')
                        .attr('d', d3.symbol().type(d3.symbolStar).size(function (d) {
                            if (d.anno_num > 20)
                                return 400;
                            else
                                return 20 * d.anno_num;
                        }))
                        .attr('transform', function (d, i) {
                            return 'translate(' + d.x + ',' + d.y + ')';
                        })
                        .attr('fill', 'yellow')
                        .attr('stroke', 'black');



                    // source circle
                    d3.select('#sr0').remove();
                    project
                        .append('circle')
                        .attr('r', 10)
                        .attr('transform', function () {
                            return 'translate(' + sourceX + ',' + sourceY + ')';
                        })
                        .style('fill', 'white')
                        .style('stroke', 'black');
                    project
                        .append('circle')
                        .attr('r', 10)
                        .attr('transform', function () {
                            return 'translate(' + sourceX + ',' + sourceY + ')';
                        })
                        .style('fill', 'steelblue')
                        .style('stroke', 'black')
                        .attr('id', 'sr0')
                        .attr('class', 'nodeblock')
                        .on('contextmenu', d3.contextMenu(menu));

                }
            },
            createUnitTree: function (sankeyData, height, width) {
                if (init_history_panel) return;
                visualizer.U_SANKEY = null;
                //console.log('unit');
                //console.log(sankeyData);
                d3.select('.nodeTooltip').remove();

                var fromFlag = false, toFlag = false;

                var root = d3.hierarchy(sankeyData, function (d) {
                    return d.children;
                });

                root = d3.hierarchy(sankeyData, function (d) {
                    return d.parent;
                });

                var actionTest = function (root) {
                    var from = d3.select('rect.history-from').data();
                    var to = d3.select('rect.history-to').data();
                    userManager.ROOT = root;

                    if (from.length != 0 && to.length != 0) {
                        //   if (from.length != 0 && to.length != 0 && (from[0].id == to[0].id)) {
                        historyManager.getUnitActionhistory(searchNode(from[0], to[0], []));
                    }
                    else {
                        //console.log('select again');
                    }
                };

                var searchNode = function (from, to, list) {
                    var node = {
                        block_iden: to.id,
                        block_ver: to.ver
                    };
                    list.unshift(node);

                    if (from == to) {
                        //console.log('list');
                        //console.log(list);
                        return list;
                    }


                    if (to.parent.id == from.id && to.parent.ver == from.ver) {
                        list.unshift({
                            block_iden: from.id,
                            block_ver: from.ver
                        });
                        //console.log('list');
                        //console.log(list);
                        return list;
                    }
                    return searchNode(from, to.parent, list);
                };

                var menu2 = [
                    {
                        title: 'test',
                        action: function (d) {
                            //console.log('menu2 ok')
                        }
                    }
                ];

                var menu = [
                    {
                        title: 'Start Here',
                        action: function (d) {
                            if (!fromFlag) {
                                d3.selectAll('.nodeblock').classed('history-from', false);
                                d3.select(d).classed('history-from', true);
                                d3.select(d).style('fill', 'orange');
                                fromFlag = true;
                            }
                            else {
                                d3.select('.nodeblock.history-from').attr('class', 'nodeblock').style('fill', 'steelblue');
                                d3.selectAll('.unode').classed('history-from', false);
                                d3.select(d).classed('history-from', true);
                                d3.select(d).style('fill', 'orange');
                            }

                            if (fromFlag == true && toFlag == true)
                                actionTest(root);
                        }
                    },
                    {
                        title: 'End Here',
                        action: function (d) {
                            if (!toFlag) {
                                d3.selectAll('.nodeblock').classed('history-to', false);
                                d3.select(d).classed('history-to', true);
                                d3.select(d).style('fill', 'yellow');
                                toFlag = true;
                            }
                            else {
                                d3.select('.nodeblock.history-to').attr('class', 'nodeblock').style('fill', 'steelblue');
                                d3.selectAll('.unode').classed('history-to', false);
                                d3.select(d).classed('history-to', true);
                                d3.select(d).style('fill', 'yellow');
                            }

                            if (fromFlag == true && toFlag == true)
                                actionTest(root);
                        }
                    },
                    /*
                     {
                     title: 'Restoration',
                     action: function (d) {
                     var data = d3.select(d).data()[0];
                     //console.log(data);
                     unitManager.updateUnit($('#' + data.id), false, {
                     username: userManager.USERNAME,
                     project_name: userManager.PROJECT,
                     session_name: userManager.SESSION,
                     session_ver: userManager.SESSION_VER,
                     block_iden: data.id,
                     block_ver: data.save_ver
                     });
                     }
                     },
                     */
                    {
                        title: 'Branch Unit',
                        action: function (d) {
                            var data = d3.select(d).data()[0];
                            visualizer.D_SANKEY = {id: userManager.SESSION, ver: userManager.SESSION_VER};
                            // restore unit data first and branch it.
                            console.log(d,data);
                            $.ajax({
                                url: 'restoration.html',
                                method: 'post',
                                data: {
                                    username: userManager.USERNAME,
                                    project_name: userManager.PROJECT,
                                    session_name: userManager.SESSION,
                                    session_ver: userManager.SESSION_VER,
                                    block_iden: data.id,
                                    save_ver: data.save_ver
                                },
                                error: userManager.failAjax
                            }).done(function (data,status) {
                                if (!data.success) return userManager.failAjax(data,status);
                                $.ajax({
                                    url: data.output[0].heatmap_path,
                                    error: userManager.failAjax
                                }).done(function (data,status) {
                                    var reqObj = data.request[0];
                                    unitManager.branchUnit(null,reqObj);
                                });
                            });
                        }
                    },
                    {
                        title: 'Refresh Session',
                        action: function (d) {
                            visualizer.refreshSession(d);
                        }
                    },
                    {
                        title: 'Session Workflow',
                        action: function (d) {
                            historyManager.getSessionHistory();

                            userManager.logger('Session-Workflow', {
                                username: userManager.USERNAME,
                                project_name: userManager.PROJECT
                            });
                        }
                    }
                ];

                var legend_menu = [
                    {'tab': 'MANAGEMENT', 'color': '#377eb8', 'rcolor': 'black'},
                    {'tab': 'ANALYSIS', 'color': '#4daf4a', 'rcolor': 'black'},
                    {'tab': 'ANNOTATION', 'color': '#984ea3', 'rcolor': 'black'},
                    {'tab': 'HISTORY', 'color': '#ff7f00', 'rcolor': 'black'}
                ];
                var mgt = [
                    {'tab': 'Create-Project', 'color': '#e41a1c'},
                    {'tab': 'Delete-Project', 'color': '#377eb8'},
                    {'tab': 'Create-Session', 'color': '#4daf4a'},
                    {'tab': 'Delete-Session', 'color': '#984ea3'},
                    {'tab': 'Apply-Unit', 'color': '#ff7f00'},
                    {'tab': 'Save-Session', 'color': '#ffff33'},
                    {'tab': 'Create-Unit', 'color': '#a65628'},
                    {'tab': 'Delete-Unit', 'color': '#f781bf'},
                    {'tab': 'Save-Unit', 'color': '#a6cee3'}
                ];
                var als = [
                    {'tab': 'Branch-Session', 'color': '#66c2a5'},
                    {'tab': 'Change-Data', 'color': '#fc8d62'},
                    {'tab': 'Change-Cluster-Type', 'color': '#8da0cb'},
                    {'tab': 'Change-Color', 'color': '#e78ac3'},
                    {'tab': 'Change-Unit-Name', 'color': '#a6d854'},
                    {'tab': 'Branch-Unit', 'color': '#ffd92f'},
                    {'tab': 'Restore-Unit', 'color': '#1f78b4'},
                    {'tab': 'Change-Cluster-Parameter', 'color': '#a6761d'},
                    {'tab': 'Create-Unit-Graph', 'color': '#e31a1c'}
                ];
                var anno = [
                    {'tab': 'Update-Unit-Annotation', 'color': '#984ea3'},
                    {'tab': 'Create-Unit-Annotation', 'color': '#fc8d62'},
                    {'tab': 'Delete-Unit-Annotation', 'color': '#8da0cb'},
                    {'tab': 'Change-Session-Annotation', 'color': '#66c2a5'}
                ];
                var his = [
                    {'tab': 'Show-Session', 'color': '#8dd3c7'},
                    {'tab': 'Undo-Unit', 'color': '#ffffb3'},
                    {'tab': 'Redo-Unit', 'color': '#bebada'},
                    {'tab': 'Move-Unit', 'color': '#fb8072'},
                    {'tab': 'Copy-Unit', 'color': '#80b1d3'}
                ];

                var legendData2 = {};
                var catData = {};
                mgt.forEach(function (elm) {
                    legendData2[elm['tab']] = '#377eb8';
                    catData[elm['tab']] = 'mgt';
                });
                als.forEach(function (elm) {
                    legendData2[elm['tab']] = '#4daf4a';
                    catData[elm['tab']] = 'als';
                });
                anno.forEach(function (elm) {
                    legendData2[elm['tab']] = '#984ea3';
                    catData[elm['tab']] = 'anno';
                });
                his.forEach(function (elm) {
                    legendData2[elm['tab']] = '#ff7f00';
                    catData[elm['tab']] = 'his';
                });


                //-----------------------------------------------------------------------
                var $svg = $('#history_tree');
                //var w = $svg.width();
                var h = 343;
                var width = h / 2, height = h / 2, padding = 2.5;
                var nodeWidth = 10;
                var sourceX, sourceY;

                var sankey = d3.sankey()
                    .nodeWidth(nodeWidth)
                    .nodePadding(padding)
                    .sankeyHeight(height)
                    .size([width, height]);

                sankey.data(sankeyData)
                    .layout();

                update();
                function update() {
                    $('#unit-sankey').empty();
                    var svg = d3.select('#unit-sankey')
                    //.attr('transform', 'translate(90,90)')
                    var canvas = svg.append('g')
                        .attr('class', 'nodelink');

                    function thiszoomed() {
                        svg.attr("transform", d3.event.transform);
                    }

                    visualizer.U_SANKEY = canvas;
                    var h = 343;
                    //var zoom_fun = d3.zoom().scaleExtent([1, 8]).on('zoom', thiszoomed);
                    var thissvg = d3.select('#history_tree');
                    //thissvg
                    //thissvg.call(zoom_fun);
                    //d3.select('#history_tree')._groups[0][0].__zoom = {k:1,x:0,y:0}
                    //console.log(($('#history_tree').width() - h / 2) / 4);
                    //console.log(visualizer.ZOOM_SANKEY);
                    visualizer.ZOOM_SANKEY.scaleTo(thissvg, 1);
                    var z = d3.zoomTransform(d3.select('#history_tree').node());
                    visualizer.ZOOM_SANKEY.translateBy(thissvg, 230 - z.x, -z.y);
                    canvas.attr('transform', 'translate(230,0)scale(1)');

                    //link background
                    var linkBackground = canvas.append('g').selectAll('linkB')
                        .data(sankey.linkBackground)
                        .enter()
                        .append('path')
                        .attr('d', sankey.link())
                        .style('fill', '#eee');

                    //link
                    var link = canvas.append('g').selectAll('.linkS')
                        .data(sankey.links)
                        .enter()
                        .append('g')
                        .append('path')
                        .attr('id', 'linkS')
                        .attr('class', function (d) {
                            return 's' + catData[d.action] + ' ' + d.action;
                        })
                        .style('stroke', function (d) {
                            return legendData2[d.action];
                        })
                        .attr('d', sankey.link());

                    function actionNum(d) {
                        var most, m = 0, a = 0, an = 0, h = 0;

                        if (d.action_list != null) {
                            d.action_list.forEach(function (action) {
                                if (catData[action.action] == 'mgt')
                                    m++;
                                else if (catData[action.action] == 'als')
                                    a++;
                                else if (catData[action.action] == 'anno')
                                    an++;
                                else
                                    h++;
                            });

                            if (m >= a) most = m;
                            else most = a;
                            if (most >= an) {
                            }
                            else most = an;
                            if (most >= h) {
                            }
                            else most = h;

                            if (most == m) most = 'MANAGEMENT';
                            else if (most == a) most = 'ANALYSIS';
                            else if (most == an) most = 'ANNOTATION';
                            else most = 'HISTORY';

                            return most;
                        }
                        else
                            return null;
                    }

                    var deleted_units = _.filter(unitManager.DELETED_UNITS, function (item) {
                        if (item.session_name == userManager.SESSION && item.session_ver == userManager.SESSION_VER) {
                            return item;
                        }
                    });

                    // node
                    var node = canvas.append('g').selectAll('.unode')
                        .data(sankey.nodes)
                        .enter()
                        .append('g')
                        .attr('class', 'unode')
                        .append('rect')
                        .attr('class', 'nodeblock')
                        .attr('id', function (d, i) {
                            return 'r' + i;
                        })
                        .attr('height', nodeWidth)
                        .attr('width', function (d) {
                            return d.height;
                        })
                        .attr('transform', function (d, i) {
                            if (i == 0) {
                                sourceX = d.x;
                                sourceY = d.y
                            }
                            return 'translate(' + d.x + ',' + d.y + ')';
                        })
                        .style('fill', function (d, i) {
                            //console.log('test',d,deleted_units);
                            if (_.find(deleted_units, {block_iden: d.id, block_ver: d.save_ver})) {
                                //console.log({block_iden:d.id, block_ver:d.save_ver});
                                return 'black';
                            }

                            if (actionNum(d) == null)
                                return 'steelblue';
                            else {
                                var tmp = actionNum(d);
                                if (tmp == 'MANAGEMENT')
                                    return legend_menu[0].color;
                                else if (tmp == 'ANALYSIS')
                                    return legend_menu[1].color;
                                else if (tmp == 'ANNOTATION')
                                    return legend_menu[2].color;
                                else
                                    return legend_menu[3].color;
                            }
                        })
                        .style('stroke', 'black')
                        .style('fill-opacity', .9)
                        .on('contextmenu', d3.contextMenu(menu));

                    var bookmark = d3.selectAll('.unode')
                        .append('g')
                        .attr('class', 'bookmark')
                        .append('path')
                        .attr('d', d3.symbol().type(d3.symbolStar).size(function (d) {
                            if(d.bookmark){
                                return 40;
                            }
                            else {
                                return 0;
                            }
                        }))
                        .attr('transform', function (d, i) {
                            return 'translate(' + d.x + ',' + (d.y+10) + ')';
                        })
                        .attr('fill', 'red')
                        .attr('stroke', 'black');

                    // symbol
                    var symbol = d3.selectAll('.unode')
                        .append('g')
                        .attr('class', 'star')
                        .append('path')
                        .attr('d', d3.symbol().type(d3.symbolStar).size(function (d) {
                            if (d.anno_num > 20)
                                return 400;
                            else
                                return 20 * d.anno_num;
                        }))
                        .attr('transform', function (d, i) {
                            return 'translate(' + d.x + ',' + d.y + ')';
                        })
                        .attr('fill', 'yellow')
                        .attr('stroke', 'black');

                    // is broken
                    d3.selectAll('.unode')
                        .style("stroke-dasharray", function(d){
                           if(d.is_broken){
                                return 4;
                           }
                        });


                    function copyUnit(s, t) {
                        $.ajax({
                            url: "unitCopy.html",
                            method: "post",
                            data: {
                                username: userManager.USERNAME,
                                project_name: userManager.PROJECT,
                                session_name: userManager.SESSION, session_ver: userManager.SESSION_VER,
                                block_iden: s.id, block_ver: s.ver,
                                target_session_name: userManager.SESSION, target_session_ver: userManager.SESSION_VER,
                                target_block_iden: t.id, target_block_ver: t.ver
                            },
                            error: userManager.failAjax,
                            success: successUnitCopy
                        });
                    }

                    function setupCopyActionModal(data, testdrag) {
                        $('.history-copy-table-container').empty();
                        ////console.log('setupCopyActionModal',data);
                        $('a.btn-choose-copy-action').off('click').on('click', function (e) {
                            var aid = _.map($('#history_copy_table').find('input[name="check-action"]:checked'), function (item) {
                                return {action_id: item.value};
                            });
                            //console.log(aid);
                            //console.log('checked',aid);
                            $.ajax({
                                url: "actionMove.html",
                                method: "post",
                                data: {
                                    username: userManager.USERNAME,
                                    project_name: userManager.PROJECT,
                                    session_name: userManager.SESSION,
                                    session_ver: userManager.SESSION_VER,
                                    block_iden: testdrag.id,
                                    block_ver: testdrag.ver,
                                    action_list: JSON.stringify(aid)
                                },
                                error: userManager.failAjax,
                                success: successUnitMove
                            });
                        });
                        var table = $('<table id="history_copy_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody></tbody></thead></table>');

                        var thead = table.find('thead');
                        var tr = $('<tr>');
                        var header = ["#", "DATE", "ACTION", 'DETAIL'];
                        _.forEach(header, function (item, idx) {
                            var th = $('<th>').text(item);
                            tr.append(th);
                        });
                        thead.append(tr);
                        var parsedData = _.map(data.action_list, function (item, idx) {
                            switch (item.action) {
                                default:
                                    //console.log(item.parameter);
                                    item.param_label = _.map(_.omit(item.parameter, ['block_iden', 'block_ver', 'ver', 'save_ver']), function (val, key) {
                                        return val;
                                    }).join(", ");
                                    break;
                                case ("Change-Data"):
                                    item.param_label = item.parameter.data_name;
                                    break;
                                case ("Locate-Unit"):
                                    item.param_label = _.map(item.parameter, function (val, key) {
                                        return key + ": " + val;
                                    }).join(", ");
                                    break;
                            }
                            return item;
                        });
                        var tbody = table.find('tbody');
                        _.forEach(parsedData, function (item, idx) {
                            var tr = $('<tr>');
                            var check_td = $('<td><input name="check-action" class="checkbox" type="checkbox" value="' + item.action_id + '"></td>');
                            var td2 = $('<td></td>').text(item.date);
                            var td3 = $('<td></td>').text(item.action);
                            var td4 = $('<td></td>').text(item.param_label);
                            tr.append(check_td, td2, td3, td4);
                            tr.data(item);
                            tbody.append(tr);
                        });
                        $('.history-copy-table-container').append(table);
                        var oTable = table.DataTable(
                            {
                                paging: false,
                                scrollY: '30vh',
                                scrollCollapse: true,
                                dom: "ft",
                                autoWidth: true,
                                fixedHeader: true,
                                initComplete: function () {
                                    var api = this.api();

                                    api.columns().indexes().flatten().each(function (i) {
                                        var column = api.column(i);
                                        if (i == 0) {
                                            var check_all = $('<input type="checkbox" id="check_all_action">');
                                            check_all.on('click', function (e) {
                                                //console.log(check_all.prop('checked'));
                                                var x = $('input[name="check-action"]');
                                                if (check_all.prop('checked')) x.prop('checked', true);
                                                else {
                                                    x.prop('checked', false);
                                                }
                                            });
                                            check_all.appendTo($(column.header()).empty());
                                            return;
                                        }
                                    });
                                    $('#history_copy_table >tbody >tr').on('click', function (e) {
                                        var thisTr = $(this);
                                        var checkbox = thisTr.find('input[name="check-action"]');
                                        var checked = checkbox.prop('checked');
                                        checked ? checkbox.prop("checked", false) : checkbox.prop("checked", true);
                                    });

                                    $('#history-copy-modal').on('shown.bs.modal', function () {
                                        $('#history_copy_table').dataTable().api().columns.adjust();
                                    });
                                }
                            });
                        $('#history-copy-modal').modal('show');
                    }

                    function actionMove(d, testdrag) {
                        /*
                         var aid = [];

                         d.action_list.forEach(function (id) {
                         aid.push({'action_id': id.action_id});
                         });
                         $.ajax({
                         url: "actionMove.html",
                         method: "post",
                         data: {
                         username: userManager.USERNAME,
                         project_name: userManager.PROJECT,
                         session_name: userManager.SESSION,
                         session_ver: userManager.SESSION_VER,
                         block_iden: testdrag.id,
                         block_ver: testdrag.ver,
                         action_list: JSON.stringify(aid)
                         },
                         error: userManager.failAjax,
                         success: successUnitCopy
                         });
                         */
                        setupCopyActionModal(d, testdrag);
                    }

                    function successUnitCopy(d, s) {
                        $('#unit-sankey').empty();
                        $('#unit-legend').empty();
                        d3.select('.nodeTooltip').remove();

                        $.ajax({
                            url: "getSessionHistory.html",
                            method: "post",
                            data: {username: userManager.USERNAME, project_name: userManager.PROJECT},
                            error: userManager.failAjax,
                            success: historyManager.getUnitHistory(userManager.SESSION, userManager.SESSION_VER)
                        });
                    }

                    function successUnitMove(d, s) {
                        alert('Success to move actions.');
                        $('#history-copy-modal').modal('hide');
                        $('#unit-sankey').empty();
                        $('#unit-legend').empty();
                        d3.select('.nodeTooltip').remove();

                        $.ajax({
                            url: "getSessionHistory.html",
                            method: "post",
                            data: {username: userManager.USERNAME, project_name: userManager.PROJECT},
                            error: userManager.failAjax,
                            success: historyManager.getUnitHistory(userManager.SESSION, userManager.SESSION_VER)
                        });
                    }

                    //contextmenu
                    d3.select('body').on('click.d3-context-menu2', function () {
                        d3.select('.d3-context-menu2').remove();
                    });

                    function cmMenu(d, t) {
                        if (mousedrag) {
                            var cm = d3.select('html')
                                .append('div')
                                .attr('class', 'd3-context-menu2')
                                .style('left', (d3.event.sourceEvent.clientX - 2) + 'px')
                                .style('top', (d3.event.sourceEvent.clientY - 2) + 'px')
                                .style('display', 'block')
                                .append('ul');

                            cm.append('li')
                                .html('COPY')
                                .on('click', function () {
                                    d3.select('.d3-context-menu2').remove();

                                    copyUnit(d, t);
                                });

                            cm.append('li')
                                .html('MOVE')
                                .on('click', function () {
                                    d3.select('.d3-context-menu2').remove();

                                    actionMove(d, t);
                                });
                        }
                    }

                    // drag node
                    var mouseover = false;
                    var mousedrag = false;
                    var testdrag;

                    node.call(d3.drag()
                        .on('start', function (d, i) {
                            mousedrag = true;
                            testdrag = null;
                            console.log('start',d);

                            d3.select('#drag')
                                .attr('width', d.height)
                                .attr('height', 10)
                                .attr('transform', 'translate(' + d3.event.x + ',' + d3.event.y + ')');

                            //console.log('start-node');
                            //console.log(d);

                            d3.selectAll('.nodeblock').attr('stroke-width', 1);
                            d3.select('#r' + i).attr('stroke-width', 2);

                            // select unit in the view by skyjin
                            if (($('#' + d.name).length != 0) && (d.ver == $('#' + d.name).data().req.block_ver)) {
                                $('#' + d.name).trigger('click');
                            } else {
                                var data = d;
                                unitManager.updateUnit($('#' + data.id), false, {
                                    username: userManager.USERNAME,
                                    project_name: userManager.PROJECT,
                                    session_name: userManager.SESSION,
                                    session_ver: userManager.SESSION_VER,
                                    block_iden: data.id,
                                    save_ver: data.save_ver
                                });
                            }

                            // call unit action history
                            historyManager.getUnitActionhistory([{block_iden: d.id, block_ver: d.ver}]);
                        })
                        .on('drag', function (d) {
                            d3.select('#drag')
                                .attr('transform', 'translate(' + d3.event.x + ',' + d3.event.y + ')');
                        })
                        .on('end', function (d) {
                            d3.select('#drag')
                                .attr('width', 0)
                                .attr('height', 0);

                            if (mouseover && (testdrag != d && testdrag != null)) {
                                //console.log('end-node');
                                //console.log(testdrag);

                                cmMenu(d, testdrag);
                            }

                            mousedrag = false;
                        })
                    );


                    // node mouse over
                    node.on('mouseover', function (d, i) {
                        mouseover = true;
                        if (mousedrag)
                            testdrag = d;

                        //skyjin select unit on hover
                        if (($('#' + d.name).length != 0) && (d.ver == $('#' + d.name).data().req.block_ver)) {
                            $('#' + d.name).trigger('click');
                        }

                        // tooltip
                        var tooltip = d3.select('#slider-history')
                            .append('div')
                            .attr('class', 'nodeTooltip')
                            .style('position', 'absolute')
                            .style('opacity', 0);

                        tooltip.style('width', '230px')
                            .style('height', '80px')
                            .style('left', event.clientX + 30 + 'px')
                            .style('top', event.clientY + 'px')
                            .html(
                                "<div class='d3-tip-rect' style='z-index: 99'>" +
                                "<span> NAME : " + d.name + "</span><br>" +
                                "<span> LAST DATE : <span class='d3-tip-value'>" + d.last_date + "</span></span><br>" +
                                "<span> SAVE VER : " + d.ver + "</span><br>" +
                                "<span> ACTION NUM : " + d.action_num + "</span>" +
                                "</div>"
                            )
                            .transition()
                            .style('opacity', 1);

                        // hierarchy
                        d3.select(this)
                            .style('fill-opacity', .5);

                        var s = d.source;
                        while (s >= -1) {
                            d3.select('#r' + s)
                                .style('fill-opacity', .5);

                            if (s != -1)
                                s = sankey.nodes()[s].source;
                            else
                                s = -2;
                        }
                    })
                        .on('mouseout', function (d, i) {
                            d3.select('.nodeTooltip').remove();

                            d3.select(this)
                                .style('fill-opacity', .9);
                            var s = d.source;
                            while (s >= -1) {
                                d3.select('#r' + s)
                                    .style('fill-opacity', .9);

                                if (s != -1)
                                    s = sankey.nodes()[s].source;
                                else
                                    s = -2;
                            }

                            mouseover = false;
                        });

                    // source circle
                    d3.select('#r0').remove();
                    canvas
                        .append('circle')
                        .attr('r', 10)
                        .attr('transform', function () {
                            return 'translate(' + sourceX + ',' + sourceY + ')';
                        })
                        .style('fill', 'white')
                        .style('stroke', 'black');
                    canvas
                        .append('circle')
                        .attr('r', 10)
                        .attr('transform', function () {
                            return 'translate(' + sourceX + ',' + sourceY + ')';
                        })
                        .style('fill', 'steelblue')
                        .style('stroke', 'black')
                        .attr('id', 'r0')
                        .attr('class', 'nodeblock')
                        .on('contextmenu', d3.contextMenu(menu));

                    // drag rect
                    d3.select('.unode')
                        .append('rect')
                        .attr('id', 'drag');
                }
            },
            showSession: function (d) {
                //var data = d3.select(d).data()[0];
                var data = d;
                //d3.selectAll(".nodeblock").classed("selected-history", false);
                //d3.select(d).classed("selected-history", true);
                var options = _.map($('select.session-list > option'), function (item, idx) {
                    return item.value;
                });
                options.shift(); // delete description
                var options_json = _.map(options, function (item, idx) {
                    return JSON.parse(item)
                });
                var found = _.find(options_json, {session_name: data.name, session_ver: data.ver});
                $('select.session-list').val(JSON.stringify(found)).change();
            },
            refreshSession: function (d) {
                // show this session
                var data = {name: userManager.SESSION, ver: userManager.SESSION_VER};
                visualizer.showSession(data);
                historyManager.getUnitHistory(data.name, data.ver);
            },
            transformToMiniMap: function () {
                d3.select('#project-tree').attr('transform', 'translate(20,20)scale(0.5)').classed('mini', true);

            }
        });
})(visualizer);
