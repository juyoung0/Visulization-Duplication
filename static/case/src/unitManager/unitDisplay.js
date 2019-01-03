/**
 * Created by dryji on 2017-02-20.
 * addUnit will display new unit in the screen,
 * locate unit will setup unit position using position data.
 * update unit is used to update and preview *
 */
(function (parent) {
    unitState = "new";
    _.extend(parent, {
        addUnit: function (dataObj) {
            var blockId;
            if (dataObj == undefined) {
                dataObj = {req: null, res: null, position: null};
                blockId = this.getBlockId();
                // 블록 파라메터 생성
                var reqObj = {
                    // django add color
                    block_iden: blockId,
                    block_name: "U" + ($('.block').length + 1),
                    block_ver: 0,
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    project_name: userManager.PROJECT,
                    position: {top: 0, left: 0}
                };
                dataObj.req = reqObj;
                dataObj.position = {top: 0, left: 0};
            }
            else {
                blockId = dataObj.req.block_iden;
            }

            var blockSvgId = blockId + "-svg";
            var $block = $('<div class="thumbnail block display text-right">' +
                '<a href="#" class="block-title badge" style="float:left" data-toggle="tooltip" title="">' + dataObj.req.block_name + ' </a>' +
                '<div class="block-menu">' +
                '<a href="#" class="download-block"><i class="glyphicon glyphicon-download-alt"></i> </a>' +
                '<a href="#" class="fix-block"><i class="glyphicon glyphicon-pushpin"></i> </a>' +
                '<a href="#" class="hide-text"><i class="glyphicon glyphicon-text-background"></i> </a>' +
                '<a href="#" class="toggle-block hide"><i class="glyphicon glyphicon-resize-horizontal"></i> </a>' +
                '<a href="#" class="del-block"> <i class="glyphicon glyphicon-remove"></i></a>' +
                '</div>' +
                '<div><select data-live-search="true" class="selectpicker gene-selector" data-width="100%" multiple data-actions-box="true"></select></div>' +
                '<div class="tabbable tab-right" style="width:0px;height: 0px;">' +
                '<ul class="pagination pagination-sm annotation" style="vertical-align:top;display: inline;position: relative"><li><a href="#" style="padding-left: 1px !important;padding-right: 1.5px !important;padding-bottom: 0px !important;" class="add-unit-annotation"><i class="material-icons">note_add</i></a></li></ul>' +
                '</div>' +
                '<div class="" style="display: block">' +
                '<div class="caption">' + '<div class="block-display"></div></div>' +
                '</div></div>');

            $('#content-list').append($block);
            $block.attr('id', blockId);
            $block.data(dataObj);
            $block.find('a.del-block').on('click', function (e) {
                unitManager.deleteUnit(blockId)
            });
            $block.on('click', function (e) {
                $('.block').removeClass('selected-block');
                $block.addClass('selected-block');
                unitManager.selectUnit($block);
            });

            $block.find('a.hide-text').on('click', function () {
                var s = d3.select($block.find('svg').get(0));
                if ($block.hasClass('hide-text')) {
                    s.selectAll('g:not(.legend)').selectAll('text').style('display', 'inline');
                } else {
                    s.selectAll('g:not(.legend)').selectAll('text').style('display', 'none');
                }
                $block.toggleClass('hide-text');
            });

            // appending download event
            $block.find('.download-block').on('click', function (e) {
                ////console.log('download-block', $block.find('svg').get(0));
                writeDownloadLink($block.find('svg').get(0), $block.data().req.block_name);
            });

            // appending annotation
            if (dataObj.res != null)
                unitManager.getAnnotations(dataObj.res.annotation_path, $block);


            $block.find('a.fix-block').on('click', function (e) {
                var $caption = $block.find('div.caption');
                ////console.log($caption);
                if ($caption.hasClass('fixed-block')) {
                    $caption.removeClass('fixed-block');
                    $caption.removeAttr('style');
                }
                else {
                    $caption.addClass('fixed-block');
                    $caption.css('height', window.innerHeight - 150 + 'px');
                }
            });
            $block.find('.add-unit-annotation').on('click', function (e) {
                $block.trigger('click');
                $('#annotation-modal').find('input').val("");
                $('#annotation-modal').find('textarea').val("");
                $('#annotation-modal').modal('show');
            });
            $('#annotation-modal').on('shown.bs.modal', function (e) {
                var regExp = /\(([^)]+)\)/;
                $('input.input-last-edited-note').val(new Date().toString().replace(regExp, ""));
                $('.project-badge').text(userManager.PROJECT);
                $('.session-badge').text(userManager.SESSION + ' - VER.' + userManager.SESSION_VER);
                $('.unit-name').text(unitManager.SELECTED.data().req.block_name);
                $('.input-author-note').val(userManager.USERNAME);
                $('.data-name-badge').text(unitManager.SELECTED.data().req.data_name);
                $('.input-cluster-note').val(unitManager.SELECTED.data().req.cluster_type + " - " + unitManager.SELECTED.data().req.cluster_param);
            });
            // Menu set
            var $blockDisplay = $block.find('div.block-display');
            var $blockEdit = $block.find('div.block-edit');
            var $blockTitle = $block.find('.block-title');
            var $blockToggle = $block.find('.toggle-block');
            var $blockName = $('#block_name').val();
            var $blockVer = $block.data().req.block_ver;

            $block.find('a.fix-block').on('click', function (e) {
                var blockHeight = $block.height();
                ////console.log(blockHeight);
            });
            $block.find('a.edit-block').on('click', function (e) {
                $blockDisplay.toggle();
                $blockEdit.toggle();
            });

            $blockToggle.on('click', function (e) {
                    var mySvg = $block.find('svg');
                    createMiniViewBox($block);
                    if ($block.hasClass('only-heatmap')) {
                        mySvg.attr('viewBox', $block.attr('originViewBox'));
                        $block.toggleClass('only-heatmap');
                    }
                    else {
                        mySvg.attr('viewBox', $block.attr('miniViewBox'));
                        $block.toggleClass('only-heatmap');
                    }
                }
            );

            function createMiniViewBox($block) {
                var originViewBox = $block.attr('originViewBox');
                if (originViewBox == null) return;
                var replaceViewBox = originViewBox.split(" ");
                var heat_size = (replaceViewBox[2] - 500);
                //var rect_size =  heat_size/ $block.data().res.label.length;
                replaceViewBox[0] = heat_size;
                replaceViewBox[1] = 5;
                replaceViewBox[2] = heat_size / 2;
                replaceViewBox = replaceViewBox.join(" ");
                $block.attr('miniViewBox', replaceViewBox);
            }


            // 화면 갱신
            $block.hide().show('normal');
            $("input.file").fileinput({'showRemove': false, 'showUpload': false});
            this.blockMap[blockId] = $block;
            unitManager.DRAGGED = false;
            $block.draggable({
                //handle: "div.block",
                snap: true,
                start: function (event, ui) {
                    unitManager.selectUnit($block);
                    if(event.shiftKey) {
                        return false;
                    }
                },
                stop: function (e, ui) {
                    if (unitManager.DRAGGED) {
                        ////console.log(unitManager.DRAGGED);
                        unitManager.moveUnit($(e.target));
                        unitManager.DRAGGED = false;
                    }
                },
                drag: function (event, ui) {
                    if(event.shiftKey) {
                        return false;
                    }
                    unitManager.DRAGGED = true;
                    var $container = $("#content-list");
                    if (ui.position.left < 0) {
                        ui.position.left = 0;
                    }
                    if (ui.position.top < 0) {
                        ui.position.top = 0;
                    }
                    /*
                     var maxDown = $container.height() - $(this).height();
                     if( ui.position.top > maxDown) {
                     ui.position.top = maxDown;
                     }
                     */
                },
                //containment: "#content-list"
            }).resizable({
                //containment: "#conten-list",
                handles: 'w,e',
                minWidth: 60,
                resize: function (event, ui) {
                    createMiniViewBox($block);
                    var viewBox;
                    if ($block.hasClass("only-heatmap")) {
                        viewBox = $block.attr("miniViewBox");
                    }
                    else {
                        viewBox = $block.attr("originViewBox");
                    }
                    if (ui.size.width < 130) {
                        $block.find('.label').css({'display': 'none'});
                        $block.find('.block-menu').css({'display': 'none'});
                        $block.find('svg').attr('viewBox', $block.attr("miniViewBox"));
                    }
                    else {
                        $block.find('.label').css({'display': 'block'});
                        $block.find('.block-menu').css({'display': 'block'});
                        $block.find('svg').attr('viewBox', viewBox);
                    }

                    //var height = $block.find('div.caption');
                    //var h = (height[0].offsetHeight);
                    //$block.outerHeight(h);
                }
            });
            //var originViewBox = '0 0 700 5110';
            //$block.attr('originViewBox', originViewBox);
            $block.css({top: 0, left: 0});
            //$('#content-list').append($block);
            // 신규 블럭 셀렉트
            //$block.trigger('click');
            $block.data(dataObj);
            //unitManager.SELECTED = $block;


            // 블록 디스플레이
            var $gene_sel = $block.find('.gene-selector');
            if (dataObj.res) {
                if (dataObj.res.vis_types == "Heatmap") {
                    visualizer.createHeatmap(dataObj.res.cluster_data, dataObj.res.label, dataObj.res.name_data, blockId, "main");
                    _.forEach(dataObj.res.name_data, function (item) {
                        var $o = $('<option></option>').val(item).text(item);
                        $gene_sel.append($o);
                    });
                    $('.selectpicker').selectpicker('refresh');
                }
                if (dataObj.res.vis_types == null){
                    moduleNetwork.loadGraph(dataObj.res.node_path, dataObj.res.edge_path, $block);
                    $block.data().gesa = {genes:dataObj.res["gene_list"].split('\n'),species:dataObj.res.species};
                    $gene_sel.parent().addClass('hide');
                }
                if (dataObj.res.vis_types == "Parallel Coordinate Plot") {
                    visualizer.createPCP(dataObj.res.data, blockId, $blockVer, $blockName, "main", JSON.parse(dataObj.res.column_order), JSON.parse(dataObj.res.selected_index));
                }
                if (dataObj.res.vis_types == "Scatterplot Matrix") {
                    visualizer.createSCM(dataObj.res.data, blockId, $blockVer, $blockName, "main", JSON.parse(dataObj.res.selected_index));
                }
            }

            // 블록 이동
            if (dataObj.position) {
                unitManager.locateUnit($block, dataObj.position)
            }
            //////console.log('addunit',$block);
            //////console.log('logger','Create-Unit',$block.data());
            $('.selectpicker').selectpicker('refresh');
            return $block;
        },
        locateUnit: function ($block, p) {
            var position = p;
            if (p.top < 0) p.top = 0;
            $block.css('position', 'absolute');
            $block.css('left', p.left);
            $block.css('top', p.top);
            $block.css('width', p.width);
            //$block.css('height', p.height);

            var observer = new MutationObserver(function (mutations) {
                mutations.forEach(function (mutationRecord) {
                    //////console.log(this,mutationRecord);
                    if (mutationRecord.target.style.width == "" || mutationRecord.target.style.width == undefined) {
                        $block.css('width', p.width);
                        //$block.css('height', p.height);
                    }
                });
            });

            var target = document.getElementById($block.attr('id'));
            observer.observe(target, {attributes: true, attributeFilter: ['style']});
        },
        updateUnit: function ($block, isSave, restore) {
            ////console.log($block);
            ////console.log(isSave);
            ////console.log(restore);
            if ($block == null)
                $block = $('div.selected-block');
            ////console.log($block);
            // restore deleted unit;
            /*
             if ($block.length ==0){
             var reqObj = {req:{},position:{top: 0, left: 0}};
             reqObj.req = restore;
             reqObj.position = {top: 0, left: 0};
             reqObj.req.block_ver = restore.save_ver;
             $block = unitManager.addUnit(reqObj);
             }
             */
            if (restore) {
                $.ajax({
                    url: "restoration.html",
                    method: 'post',
                    data: restore,
                    error: userManager.failAjax,
                    success: successRestoreUnit
                });
                return;
            }


            var blockId = $block.attr('id');
            // Menu set
            var $blockTitle = $block.find('.block-title');
            var comment = $block.find('textarea.comment').val();
            $blockTitle.attr('title', comment);

            var $blockName = $('#block_name').val();
            var $clusterType = $('#cluster_list').val();
            var $clusterParam = $('#cluster_param').val();
            /* chunggilee implementation */
            var $colorType = JSON.stringify(unitManager.colorArr);
            var textData = $('textarea.file-preview-text:first').text();
            if (textData == "") textData = $($('div.kv-file-content >object')[0].contentDocument.body).find('pre').text();
            var dataName = $('div.file-footer-caption').text();
            var note = $('#block_note').val();
            var $blockVer = $block.data().req.block_ver;
            var p = unitManager.getBlockPosition($block);
            var vis_type = $('#vis_types').val();
            if (vis_type == null) vis_type = "Heatmap";
            if (unitState == "new") {
                var columnOrder = ["1", "2", "3", "4", "5", "6", "7"];
                var seletedIndex = [];
            } else if (unitState == "branch") {
                var columnOrder = changedOrder;
                var seletedIndex = changedSelection;
            }

            if (vis_type == "Heatmap") {
                var reqObj = {
                    block_iden: blockId,
                    block_ver: $blockVer,
                    block_name: $blockName,
                    cluster_type: $clusterType,
                    cluster_param: $clusterParam,
                    color_type: $colorType,
                    data: textData,
                    data_name: dataName,
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    project_name: userManager.PROJECT,
                    position: JSON.stringify(p),
                    vis_types: "Heatmap"
                };
            } else if (vis_type == "Parallel Coordinate Plot") {
                var reqObj = {
                    block_iden: blockId,
                    block_ver: $blockVer,
                    block_name: $blockName,
                    data: textData,
                    data_name: dataName,
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    project_name: userManager.PROJECT,
                    position: JSON.stringify(p),
                    vis_types: "Parallel Coordinate Plot",
                    selected_index: JSON.stringify(seletedIndex),
                    column_order: JSON.stringify(columnOrder)
                };
            } else if (vis_type == "Scatterplot Matrix") {
                var reqObj = {
                    block_iden: blockId,
                    block_ver: $blockVer,
                    block_name: $blockName,
                    data: textData,
                    data_name: dataName,
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    project_name: userManager.PROJECT,
                    position: JSON.stringify(p),
                    vis_types: "Scatterplot Matrix",
                    selected_index: JSON.stringify(changedSelection)
                };
            }

            if (isSave != undefined) {
                reqObj['is_save'] = isSave;
            }
            if (!restore) {
                $.ajax({
                    url: "clusters.html",
                    method: 'post',
                    data: reqObj,
                    error: userManager.failAjax,
                    success: successUpdateUnit
                });
            }
            function successRestoreUnit(data, status) {
                if (!data.success) {
                    alert(data.detail);
                    return;
                }


                _.forEach(_.reverse(data.output), function (item, idx) {
                    //////console.log(item);
                    var unit_path = "";
                    if (item.heatmap_path != null) {
                        unit_path = item.heatmap_path;
                    } else if (item.pcp_path != null) {
                        unit_path = item.pcp_path;
                    } else if (item.scm_path != null) {
                        unit_path = item.scm_path;
                    } else if (item.node_path != null){
                        unit_path = item.graph_path;
                    }
                    $.ajax({url: unit_path, method: 'post'}).done(function (data) {
                        ////console.log(data);
                        if (!data.request) return;
                        // TODO 수정 경로 서버
                        var d = unitManager.transData(data);
                        d.res.annotation_path = item.annotation_path;
                        $('#' + d.req.block_iden).remove();
                        var $res_block = unitManager.addUnit(d);
                        $res_block.trigger('click');
                        unitManager.logger('Restore-Unit', unitManager.getLoggerObj({block_name: $res_block.data().req.block_name}));
                    })
                });
            }


            function successUpdateUnit(data, status) {
                //data = JSON.parse(data);

                //$block.attr('data', JSON.stringify({req: reqObj, res: data}));
                if (!data.errors) {
                    data = data.output;
                    reqObj.block_ver = data.block_ver;
                    $block.data({req: reqObj, res: data, position: JSON.parse(reqObj.position)});
                    $blockTitle.text(reqObj.block_name);

                    if (vis_type == "Heatmap") {
                        unitManager.createGeneList({res: data},$block);
                        visualizer.createHeatmap(data.cluster_data, data.label, data.name_data, blockId, "main");
                    } else if (vis_type == "Parallel Coordinate Plot") {
                        visualizer.createPCP(data.data, blockId, $blockVer, $blockName, "main", JSON.parse(data.column_order), JSON.parse(data.selected_index));
                    } else if (vis_type == "Scatterplot Matrix") {
                        visualizer.createSCM(data.data, blockId, $blockVer, $blockName, "main", JSON.parse(data.selected_index));
                    }
                    isSave ? unitManager.logger('Save-Unit', reqObj) : unitManager.logger('Apply-Unit', reqObj);
                    isSave ? $block.removeClass('preview-unit') : $block.addClass('preview-unit');
                    $block.trigger('click');
                } else {
                    var errors = data.errors;
                    var errors_str = "";
                    for ($i = 0; $i < errors.length; $i++) {
                        errors_str += data.errors[$i] + "\n";
                    }
                    alert(errors_str);
                }
            }
        }, moveUnit: function ($block) {
            unitManager.logger('Locate-Unit', unitManager.getLoggerObj({position: JSON.stringify(unitManager.getBlockPosition($block))}));
        }, gridUnits: function () {
            var $container = $('#content-list');
            var w = $container.width();
            var left = 0;
            var top = 0;
            var h = 0;
            var blocks = $('.block').sort(function (a, b) {
                return $(a).height() > $(b).height();
            });
            _.forEach(blocks, function (block) {
                var $block = $(block);
                $block.css('position', 'absolute');
                $block.css('top', top);
                $block.css('left', left);
                h = h < $block.height() ? $block.height() : h;
                left = left + $block.width() + 40;
                if (left > w) {
                    top = top + h;
                    left = 0;
                }
            })
        }, createGeneList: function (dataObj, $block) {
            // 블록 디스플레이
            var $gene_sel = $block.find('select.gene-selector');
            ////console.log('createGeneList', $gene_sel);
            _.forEach(dataObj.res.name_data, function (item) {
                var $o = $('<option></option>').val(item).text(item);
                $gene_sel.append($o);
            });
            $('.selectpicker').selectpicker('refresh');
        }
    });
})(unitManager);
