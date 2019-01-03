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

                if (isPlayback)
                    blockName = $('#block_name').val();
                else
                    blockName = $('.block').length+1;

                var reqObj = {
                    // django add color
                    block_iden: blockId,
                    block_name: $('.block').length+1,
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
                '<a href="#" class="show-table"><i class="glyphicon glyphicon-th-list"></i></a>' +
                '<a href="#" class="fix-block"><i class="fixed-pin glyphicon glyphicon-pushpin"></i> </a>' +
                '<a href="#" class="del-block"> <i class="glyphicon glyphicon-remove"></i></a></div>' +
                '<div class="tabbable tab-right" style="width:0px;height: 0px;">' +
                '<ul class="pagination pagination-sm annotation" style="vertical-align:top;display: inline;position: relative"><li><a href="#" style="padding-left: 1px !important;padding-right: 1.5px !important;padding-bottom: 0px !important;" class="add-unit-annotation"><i class="material-icons">note_add</i></a></li></ul>' +
                '</div>' +
                '<div class="" style="display: block">' +
                '<div class="caption col-sm-12">' + '<div class="block-display"></div></div>' +
                '</div></div>');
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

            // appending undo filtering event
            $block.find('.show-table').on('click', function (e) {
                console.log('show-table', $block.find('svg').get(0));
                visualizer.createStatTable(changedSelection);
                //visualizer.appendLogger();
            });

            // appending download event
            $block.find('.download-block').on('click', function (e) {
                console.log('download-block', $block.find('svg').get(0));
                writeDownloadLink($block.find('svg').get(0), $block.data().req.block_name);
            });

            // appending annotation

            if (dataObj.res != null) {
                console.log(dataObj.res);
                unitManager.getAnnotations(dataObj.res.annotation_path, $block);
            }

            var reqObj = {
                user_name: userManager.USERNAME,
                block_name : $block.data().req.block_name,
                block_iden : $block.data().req.block_iden,
                block_ver : $block.data().req.block_ver
            };

            $block.find('a.fix-block').on('click', function (e) {
                var visContainer =  $("#" + blockId).find("svg");
                if (visContainer.attr("class") == "unfixed") {
                    visContainer.attr('class', "fixed");
                    $(this).find('i').addClass("fixed-pin");
                    unitManager.logger('Pin-Unit', unitManager.getLoggerObj(reqObj));
                    console.log("unit is pinned");
                }
                else {
                    visContainer.attr('class', "unfixed");
                    $(this).find('i').removeClass("fixed-pin");
                    unitManager.logger('Unpin-Unit', unitManager.getLoggerObj(reqObj));
                    console.log("unit is un-pinned");
                }
            });
            $block.find('.add-unit-annotation').on('click', function (e) {
                $block.trigger('click');
                $('textarea.input-data-note').val("");
                $('textarea.input-research-note').val("");
                $('#annotation-modal').modal('show');

            });
            $('#annotation-modal').on('shown.bs.modal', function (e) {
                var regex = /\(([^)]+\))/;
                $('input.input-last-edited-note').val(new Date().toString().replace(regex,""));
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
                var replaceViewBox = originViewBox.split(" ");
                var heat_size = (replaceViewBox[2] - 500);
                //var rect_size =  heat_size/ $block.data().res.label.length;
                replaceViewBox[0] = heat_size;
                replaceViewBox[1] = 5;
                replaceViewBox[2] = heat_size /2;
                replaceViewBox = replaceViewBox.join(" ");
                $block.attr('miniViewBox', replaceViewBox);
            }


            // 화면 갱신
            $block.hide().show('normal');
            $('.selectpicker').selectpicker('refresh');
            $("input.file").fileinput({'showRemove': false, 'showUpload': false});
            this.blockMap[blockId] = $block;

            $block.draggable({
                //handle: "div.block",
                snap: true,
                start: function (e,ui) {
                    unitManager.selectUnit($block);
                },
                stop: function (e, ui) {
                    unitManager.moveUnit($(e.target));

                },
                drag: function (event, ui) {
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
                    //createMiniViewBox($block);
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
                },
                stop: function( event, ui ){
                    unitManager.logger('Locate-Unit', unitManager.getLoggerObj({ block_name: $block.data().req.block_name, position: JSON.stringify(unitManager.getBlockPosition($block))}));
                }
            });
            //var originViewBox = '0 0 700 5110';
            //$block.attr('originViewBox', originViewBox);
            $block.css({top: 0, left: 0});
            $('#content-list').append($block);
            // 신규 블럭 셀렉트
            $block.trigger('click');
            $block.data(dataObj);
            unitManager.SELECTED = $block;
            var axisOrder = [];
            axisOrder["Economy (mpg)"] = "2";
            axisOrder["Cylinders"] = "3";
            axisOrder["Displacement (cc)"] ="4";
            axisOrder["Power (hp)"] = "5";
            axisOrder["Weight (lb)"] = "6";
            axisOrder["0-60 mph (s)"] = "7";
            axisOrder["Year"] = "8";

            // 블록 디스플레이
            if(dataObj.res) {
                reDraw = true;

                if (dataObj.res.vis_types == "Heatmap" || dataObj.res.vis_types == null) {
                    visualizer.createHeatmap(dataObj.res.cluster_data, dataObj.res.label, dataObj.res.name_data, blockId, "main");
                }
                if (dataObj.res.vis_types == "Parallel Coordinate Plot") {
                    PCPnum = PCPnum+1;
                    visualizer.createPCP(dataObj.res.data, blockId, $blockVer, $blockName, "main", JSON.parse(dataObj.res.column_order), JSON.parse(dataObj.res.brushed_axis),  JSON.parse(dataObj.res.brushed_range));
                }
                if (dataObj.res.vis_types == "Scatterplot Matrix") {
                    SCMnum = SCMnum+1;
                    visualizer.createSCM(dataObj.res.data, blockId, $blockVer, $blockName, "main", JSON.parse(dataObj.res.brushed_axis),  JSON.parse(dataObj.res.brushed_range));
                }
                if (dataObj.res.vis_types == "Scatter Plot") {
                    SPnum = SPnum+1;
                    visualizer.createSP(dataObj.res.data, blockId, $blockVer, $blockName, "main", axisOrder[dataObj.res.x_axis],  axisOrder[dataObj.res.y_axis], JSON.parse(dataObj.res.brushed_range));
                }
            }else{ /* empty unit */
                unitManager.empty = true;
            }

            // 블록 이동
            if (dataObj.position) {
                unitManager.locateUnit($block, dataObj.position)
            }

            //console.log('logger','Create-Unit',$block.data());
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
                    //console.log(this,mutationRecord);
                    if (mutationRecord.target.style.width == "" || mutationRecord.target.style.width == undefined) {
                        $block.css('width', p.width);
                        //$block.css('height', p.height);
                    }
                });
            });

            var target = document.getElementById($block.attr('id'));
            observer.observe(target, {attributes: true, attributeFilter: ['style']});


            unitManager.logger('Locate-Unit', unitManager.getLoggerObj({block_name: $block.data().req.block_name, position: JSON.stringify(unitManager.getBlockPosition($block))}));
        },
        moveUnit: function ($block) {

            unitManager.logger('Locate-Unit', unitManager.getLoggerObj({block_name: $block.data().req.block_name, position: JSON.stringify(unitManager.getBlockPosition($block))}));
        },
        /**
         *
         * @param $block
         * @param isSave true : saving, false : preview
         */
        updateUnit: function ($block, isSave, restore) {


            if ($block == null)
                $block = $('div.selected-block');

            if(restore){

                $.ajax({
                    url: "restoration.html",
                    method: 'post',
                    data: restore,
                    error: userManager.failAjax,
                    success: successRestoreUnit
                });
                return;
            }

            var $blockTitle, comment, blockId, $blockName, textData, dataName, $blockVer, p, vis_type, columnOrder, selectedIndex, PCPbrushedAxis, SCMbrushedAxis, SPbrushedRange, PCPbrushedRange, xAxis, yAxis;

            if(unitManager.empty == true){
                reDraw = false;
                blockId = $block.attr('id');
                // Menu set
                $blockTitle = $block.find('.block-title');
                comment = $block.find('textarea.comment').val();
                $blockTitle.attr('title', comment);

                $blockName = $('#block_name').val();
                var $clusterType = $('#cluster_list').val();
                var $clusterParam = $('#cluster_param').val();

                /* chunggilee implementation */
                var $colorType = JSON.stringify(unitManager.colorArr);
                textData = "text";
                dataName = "car.csv (17.46 KB)";
                var note = $('#block_note').val();
                $blockVer = $block.data().req.block_ver;
                p = unitManager.getBlockPosition($block);
                vis_type = $('#vis_types').val();

                columnOrder = ["1", "2", "3", "4", "5", "6", "7","8"];
                seletedIndex = [];
                PCPbrushedAxis = [0,0,0,0,0,0,0,0];
                SCMbrushedAxis = [0,0];
                SPbrushedRange = [[0,0],[0,0]];
                PCPbrushedRange = [];
                xAxis = $('#SPxAxis').val();
                yAxis = $('#SPyAxis').val();


            }else{
                reDraw = true;
                var d = unitManager.selectedData;

                blockId = d.block_iden;
                // Menu set

                $blockTitle = $block.find('.block-title');
                comment = $block.find('textarea.comment').val();
                $blockTitle.attr('title', comment);
                $blockName = d.block_name;


                /* chunggilee implementation */
                textData = "text";
                dataName = "car.csv (17.46 KB)";
                $blockVer =  JSON.parse(d.block_ver);
                p = unitManager.getBlockPosition($block);
                vis_type = d.vis_types;

                if(d.column_order)
                    columnOrder = JSON.parse(d.column_order);
                if(d.selected_index)
                    seletedIndex = JSON.parse(d.selected_index);
                if(d.brushed_axis){
                    if(d.vis_types == "Parallel Coordinate Plot")
                        PCPbrushedAxis = JSON.parse(d.brushed_axis);
                    if(d.vis_types == "Scatterplot Matrix")
                        SCMbrushedAxis = JSON.parse(d.brushed_axis);
                }
                if(d.brushed_range){
                    if(d.vis_types == "Parallel Coordinate Plot")
                        PCPbrushedRange =JSON.parse(d.brushed_range);
                    else
                        SPbrushedRange = JSON.parse(d.brushed_range);
                }
                if(d.x_axis)
                    xAxis = d.x_axis;
                if(d.y_axis)
                    yAxis = d.y_axis;

            }

                var axisOrder = [];
                axisOrder["Economy (mpg)"] = "2";
                axisOrder["Cylinders"] = "3";
                axisOrder["Displacement (cc)"] ="4";
                axisOrder["Power (hp)"] = "5";
                axisOrder["Weight (lb)"] = "6";
                axisOrder["0-60 mph (s)"] = "7";
                axisOrder["Year"] = "8";

          /*  }else if(unitState == "branch"){
                var columnOrder = changedOrder;
                var seletedIndex = changedSelection;
            }*/

            if(vis_type =="Heatmap") {
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
                    vis_types:"Heatmap"
                };
            }else if(vis_type=="Parallel Coordinate Plot") {
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
                    vis_types:"Parallel Coordinate Plot",
                    selected_index: JSON.stringify(seletedIndex),
                    column_order: JSON.stringify(columnOrder),
                    brushed_axis: JSON.stringify(PCPbrushedAxis),
                    brushed_range: JSON.stringify(PCPbrushedRange)
                };
            }else if(vis_type=="Scatterplot Matrix") {
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
                    vis_types:"Scatterplot Matrix",
                    selected_index: JSON.stringify(seletedIndex),
                    brushed_axis: JSON.stringify(SCMbrushedAxis),
                    brushed_range: JSON.stringify(SPbrushedRange)
                };
            }else if(vis_type=="Scatter Plot") {
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
                    vis_types:"Scatter Plot",
                    x_axis: JSON.stringify(xAxis),
                    y_axis: JSON.stringify(yAxis),
                    brushed_range: JSON.stringify(SPbrushedRange)
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

               if (!data.success) return userManager.failAjax(data, status);
                _.forEach(_.reverse(data.output), function (item, idx) {
                   // console.log(item);
                    var unit_path = "";
                    if (item.heatmap_path != null) {
                        unit_path = item.heatmap_path;
                    } else if (item.pcp_path != null) {
                        unit_path = item.pcp_path;
                    } else if (item.scm_path != null) {
                        unit_path = item.scm_path;
                    } else if (item.sp_path != null) {
                        unit_path = item.sp_path;
                    }

                    $.ajax({url: unit_path, method: 'post'}).done(function (data) {
                        if (!data.request) return;


                        /*
                        if (!data.success){
                            alert(data.detail);
                            return;
                        }
                        */

                        // TODO 수정 경로 서버
                        var d = unitManager.transData(data);
                        d.res.annotation_path = item.annotation_path;
                        $('#' + d.req.block_iden).remove();
                        var $unit = unitManager.addUnit(d);
                        $unit.trigger('click');
                        unitManager.logger('Restore-Unit', unitManager.getLoggerObj({block_name:data.block_name}));

                    })
                });
            }

            function successUpdateUnit (data, status) {
                //if (!data.success) return userManager.failAjax(data, status);
                unitManager.empty = false;
                //data = JSON.parse(data);

                //$block.attr('data', JSON.stringify({req: reqObj, res: data}));
                if (!data.errors) {
                    data = data.output;

                    reqObj.block_ver = data.block_ver;
                    $block.data({req: reqObj, res: data, position: JSON.parse(reqObj.position)});
                    $blockTitle.text(reqObj.block_name);

                    if(vis_type == "Heatmap") {
                        visualizer.createHeatmap(data.cluster_data, data.label, data.name_data, blockId, "main");
                    }else if(vis_type == "Parallel Coordinate Plot"){
                        PCPnum = PCPnum+1;
                         visualizer.createPCP(data.data, blockId, reqObj.block_ver, reqObj.block_name, "main", JSON.parse(data.column_order), JSON.parse(data.brushed_axis), JSON.parse(data.brushed_range));
                    }else if(vis_type=="Scatterplot Matrix"){
                        SCMnum = SCMnum+1;
                        visualizer.createSCM(data.data, blockId, reqObj.block_ver, reqObj.block_name,  "main", JSON.parse(data.brushed_axis), JSON.parse(data.brushed_range));
                    }else if(vis_type=="Scatter Plot"){
                        SPnum = SPnum+1;
                        visualizer.createSP(data.data, blockId, reqObj.block_ver, reqObj.block_name, "main", axisOrder[data.x_axis], axisOrder[data.y_axis], JSON.parse(data.brushed_range));
                    }
                    isSave ? unitManager.logger('Save-Unit', reqObj) : unitManager.logger('Apply-Unit', reqObj);
                    isSave ? $block.removeClass('preview-unit') : $block.addClass('preview-unit');

                    unitManager.selectedData = reqObj;


                } else {
                    var errors = data.errors;
                    var errors_str = "";
                    for ($i = 0; $i < errors.length; $i++) {
                        errors_str += data.errors[$i] + "\n";
                    }
                    alert(errors_str);
                }
                alert('The unit is saved.');
            }
        }
    });
})(unitManager);
