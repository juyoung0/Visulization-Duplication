/**
 * Created by dryji on 2017-02-20.
 * managing the unit state information using unit menu in the left slider
 */
(function (parent) {
    _.extend(parent, {
        createUnit: function () {
            var $block = unitManager.addUnit();
            $('div.fileinput-remove').trigger('click');
            $block.trigger('click');
            unitManager.logger('Create-Unit', $block.data().req);
        },
        branchUnit: function ($block) {
            if ($block != null && $block.length == 0) {
                alert("Can't find the unit to branch.");
                return;
            }


            if ($block == null) $block = unitManager.SELECTED;
            var $newBlock = unitManager.addUnit();
            var blockId = $newBlock.data().req.block_iden;

            $newBlock.data().req.parent_block_iden = $block.data().req.block_iden;
            $newBlock.data().req.parent_block_ver = $block.data().req.block_ver;
            $newBlock.data().req.cluster_type = $block.data().req.cluster_type;
            $newBlock.data().req.cluster_param = $block.data().req.cluster_param;
            $newBlock.data().req.color_type = $block.data().req.color_type;
            $newBlock.data().req.data = $block.data().req.data;
            $newBlock.data().req.data_name = $block.data().req.data_name;
            $newBlock.data().req.block_name = $block.data().req.block_name + "-B#" + $('.block').length + 1;
            $newBlock.data().req.position = JSON.stringify(unitManager.getBlockPosition($newBlock));
            $newBlock.data().req.vis_types = $block.data().req.vis_types;
            if ($block.data().req.vis_types == "Heatmap") {
                $newBlock.data().req.cluster_type = $block.data().req.cluster_type;
                $newBlock.data().req.cluster_param = $block.data().req.cluster_param;
                $newBlock.data().req.color_type = $block.data().req.color_type;
            } else if ($block.data().req.vis_types == "Parallel Coordinate Plot") {
                $newBlock.data().req.selected_index = $block.data().req.selected_index;
                /*
                 $newBlock.data().req.column_order =  $block.data().req.column_order;
                 $newBlock.data().req.brushed_axis =  $block.data().req.brushed_axis;
                 $newBlock.data().req.brushed_range =  $block.data().req.brushed_range;
                 */
                $newBlock.data().req.column_order = JSON.stringify(changedOrder);
                $newBlock.data().req.brushed_axis = JSON.stringify(changedAxes);
                $newBlock.data().req.brushed_range = JSON.stringify(changedRange);

            } else if ($block.data().req.vis_types == "Scatterplot Matrix") {
                $newBlock.data().req.selected_index = $block.data().req.selected_index;
                /*
                 $newBlock.data().req.brushed_axis =  $block.data().req.brushed_axis;
                 $newBlock.data().req.brushed_range =  $block.data().req.brushed_range;
                 */
                $newBlock.data().req.brushed_axis = JSON.stringify(changedAxes);
                $newBlock.data().req.brushed_range = JSON.stringify(changedRange);

            } else if ($block.data().req.vis_types == "Scatter Plot") {
                /*
                 $newBlock.data().req.brushed_axis =  $block.data().req.brushed_axis;
                 $newBlock.data().req.brushed_range =  $block.data().req.brushed_range;
                 */
                $newBlock.data().req.x_axis = $block.data().req.x_axis;
                $newBlock.data().req.y_axis = $block.data().req.y_axis;
                $newBlock.data().req.brushed_axis = JSON.stringify(changedAxes);
                $newBlock.data().req.brushed_range = JSON.stringify(changedRange);

            }

            var reqObj = $newBlock.data().req;
            var $blockName = $('#block_name').val();
            var $blockVer = $block.data().req.block_ver;
            $.ajax({
                url: "clusters.html",
                method: 'post',
                data: reqObj,
                error: userManager.failAjax,
                complete: function (d, s) {
                    if ($block) {
                        historyManager.getUnitHistory(visualizer.D_SANKEY.id, visualizer.D_SANKEY.ver);
                    }
                }
            }).done(function (data, status) {
                if (!data.success) return userManager.failAjax(data, status);
                //data = JSON.parse(data);
                var axisOrder = [];
                axisOrder["Economy (mpg)"] = "2";
                axisOrder["Cylinders"] = "3";
                axisOrder["Displacement (cc)"] = "4";
                axisOrder["Power (hp)"] = "5";
                axisOrder["Weight (lb)"] = "6";
                axisOrder["0-60 mph (s)"] = "7";
                axisOrder["Year"] = "8";


                //$block.attr('data', JSON.stringify({req: reqObj, res: data}));
                if (!data.errors) {
                    data = data.output;
                    reDraw = true;
                    reqObj.block_ver = data.block_ver;
                    $newBlock.data({req: reqObj, res: data, position: JSON.parse(reqObj.position)});
                    var $blockTitle = $newBlock.find('.block-title');
                    $blockTitle.text(reqObj.block_name);

                    if (data.vis_types == "Heatmap" || data.vis_types == null)
                        visualizer.createHeatmap(data.cluster_data, data.label, data.name_data, blockId, "main");
                    else if (data.vis_types == "Parallel Coordinate Plot") {
                        PCPnum = PCPnum + 1;
                        visualizer.createPCP(data.data, blockId, reqObj.block_ver, reqObj.block_name, "main", JSON.parse(data.column_order), JSON.parse(data.brushed_axis), JSON.parse(data.brushed_range));
                    } else if (data.vis_types == "Scatterplot Matrix") {
                        SCMnum = SCMnum + 1;
                        visualizer.createSCM(data.data, blockId, reqObj.block_ver, reqObj.block_name, "main", JSON.parse(data.brushed_axis), JSON.parse(data.brushed_range));
                    } else if (data.vis_types == "Scatter Plot") {
                        SPnum = SPnum + 1;
                        visualizer.createSP(data.data, blockId, reqObj.block_ver, reqObj.block_name, "main", axisOrder[data.x_axis], axisOrder[data.y_axis], JSON.parse(data.brushed_range));
                    }
                    unitManager.empty = false;
                    unitManager.logger('Branch-Unit', reqObj);
                    unitManager.selectUnit($newBlock);
                } else {
                    var errors = data.errors;
                    var errors_str = "";
                    for ($i = 0; $i < errors.length; $i++) {
                        errors_str += data.errors[$i] + "\n";
                    }
                    alert(errors_str);
                }
            });

        },
        deleteUnit: function (blockId) {
            var $block = $('#' + blockId);
            if ($block.data().req.vis_types == "Parallel Coordinate Plot") {
                if (PCPnum > 0)
                    PCPnum = PCPnum - 1;
            }
            if ($block.data().req.vis_types == "Scatterplot Matrix") {
                if (SCMnum > 0)
                    SCMnum = SCMnum - 1;
            }
            if ($block.data().req.vis_types == "Scatter Plot") {
                if (SPnum > 0)
                    SPnum = SPnum - 1;
            }

            var reqObj = {
                username: userManager.USERNAME,
                project_name: userManager.PROJECT,
                session_name: userManager.SESSION,
                session_ver: userManager.SESSION_VER,
                block_iden: blockId,
                block_ver: $block.data().req.block_ver
            };
            $.ajax({
                url: "closeBlock.html",
                data: reqObj,
                method: 'post',
                error: userManager.failAjax
            }).done(function (data, status) {
                if (!data.success) return userManager.failAjax(data, status);
                console.log('delete block', blockId, data);
                reqObj.block_name = $block.data().req.block_name;
                unitManager.logger('Delete-Unit', reqObj);
                $block.remove();

                unitManager.DELETED_UNITS.push(_.cloneDeep(reqObj));
            });

            return this.blockMap;
        },
        createClusterOptions: function (data) {
            var options = data.cluster_list;
            if (options == undefined) options = CLS;
            $('#cluster_list').append($('<option disabled selected>Select Clustering Method</option>'));
            _.map(options, function (item, idx) {
                var $option = $('<option></option>');
                $option.text(item.ClusterType);
                $option.val(item.ClusterType);
                $('#cluster_list').append($option);
            });
            $("#cluster_list").on("change", {options: options}, unitManager.changeClusterType);
        },
        changeClusterType: function (e) {
            var data = e.data.options;

            var param = _.find(data, {ClusterType: this.value}).Parameter;
            var $clusterParamter = $('div.cluster-parameter');
            $clusterParamter.empty();
            //$clusterParamter.append($('<br>'));
            var $param = null;
            switch (param) {
                case 0:
                    $param = $('<input id="cluster_param" class="form-control input-sm" type="text" placeholder="CLUSTER PARAMETER" style="margin-bottom: 2px;">');
                    $clusterParamter.append($param);
                    break;
                case null:
                    break;
                default:
                    $param = $('<select id="cluster_param" class="form-control input-sm" style="margin-bottom: 2px;"></select>');
                    $param.append($('<option disabled selected>Cluster Parameter</option>'));
                    _.map(param, function (item, idx) {
                        var $option = $('<option></option>');
                        $option.val(item);
                        $option.text(item);
                        $param.append($option)
                    });
                    $clusterParamter.append($param);
                    break;
            }
            if ($param != null) {
                $param.on('blur', function (e) {
                    if (unitManager.SELECTED.data().req.cluster_param != $param.val()) {
                        unitManager.logger('Change-Cluster-Parameter', unitManager.getLoggerObj({cluster_param: $param.val()}));
                    }
                });
            }

            unitManager.logger('Change-Cluster-Type', unitManager.getLoggerObj({cluster_type: this.value}));
        },
        /**
         * selected unit would be saved in unitManager.SELECTED
         * @param $block
         */
        selectUnit: function ($block) {
            if ($block.length == 0) {
                alert('Selected unit is a deleted unit.');
                return;
            }
            unitManager.SELECTED = $block;

            $('div.block').css('z-index', 1);
            $block.css('z-index', 30);
            var block_param = $block.data();
            $('#block_name').val(block_param.req.block_name);
            //$('#cluster_color').val(block_param.req.color_type);
            /* chunggilee implementation
             if (block_param.req.color_type != null) {
             document.getElementById('btn-color1').style.background = JSON.parse(block_param.req.color_type)[0];
             document.getElementById('btn-color2').style.background = JSON.parse(block_param.req.color_type)[1];
             document.getElementById('btn-color3').style.background = JSON.parse(block_param.req.color_type)[2];
             this.colorArr = JSON.parse(block_param.req.color_type);
             }
             $('#cluster_list').val(block_param.req.cluster_type);
             $('#cluster_param').val(block_param.req.cluster_param);
             $('#block_note').val(block_param.req.note);
             */
            if (block_param.res) {
                $('div.file-input').removeClass('file-input-new');
                unitManager.addBlockFile($block);
                $('input.file').fileinput('refreshZoom');
            } else {
                $('div.fileinput-remove').trigger('click');
            }

            unitManager.logger('Select-Unit', unitManager.getLoggerObj({block_name: block_param.req.block_name}));
            /*
             var path = unitManager.selectedPath;

             $.ajax({url: path, method: 'post'}).done(function (data) {
             if (!data.request) return;

             var d = unitManager.transData(data);
             console.log(d);
             if (d.req.selected_index)
             changedSelection = JSON.parse(d.req.selected_index);
             if (d.req.column_order)
             changedOrder = JSON.parse(d.req.column_order);
             if (d.req.brushed_axis)
             changedAxes = JSON.parse(d.req.brushed_axis);
             if (d.req.brushed_range)
             changedRange = JSON.parse(d.req.brushed_range);
             })
             */

        },
        /**
         * transData would transform dataformat from the server to the UI
         * @param data
         * @returns {{req: *, res, position}}
         */
        transData: function (data) {
            //console.log('transData', data);
            var d = {
                req: data.request[0],
                res: data.response[0],
                position: data.position
            };
            //console.log('transData', d);
            return d;
        },
        getBlockId: function () {
            // 고유 ID 부여
            var d = new Date();
            var t = d.getTime() + "";
            return "U-" + t;
        },
        getBlockPosition: function ($block) {
            // {top:111,left:111,width:111,height:111}
            var p = _.merge($block.position(), {width: $block.width(), height: $block.height()});
            return p;
        },
        /**
         * provide file preview icon
         * @param $block
         * @returns {*|jQuery|HTMLElement}
         */
        addBlockFile: function ($block) {
            //console.log('test block file');
            var $b = $('div.file-preview-thumbnails');
            $b.empty();
            var $file = $('<div class="file-live-thumbs"> ' +
                '<div class="file-preview-frame" id="preview-1484141244854-0" data-fileindex="0" data-template="text">' +
                '<div class="kv-file-content"> <textarea class="kv-preview-data file-preview-text" title="loadTest1.txt" readonly="" style="width:213px;height:160px;"></textarea> </div>' +
                '<div class="file-thumbnail-footer"> ' +
                '<div class="file-footer-caption" title="savedData.txt">savedData.txt <br><samp>()</samp></div> <div class="file-actions"> <div class="file-footer-buttons"> <button type="button" class="kv-file-zoom btn btn-xs btn-default" title="View Details"><i class="glyphicon glyphicon-zoom-in"></i></button>     </div> <div class="file-upload-indicator" title="Not uploaded yet"><i class="glyphicon glyphicon-hand-down text-warning"></i></div> <div class="clearfix"></div> </div> </div> </div> </div>');
            $file.find('textarea').text($block.data().req.data);
            $b.append($file);
            //$('input.file').fileinput('refresh');
            //console.log($b,$file);
            // setup data information
            $file.find('.file-footer-caption').attr('title', $block.data().req.data_name);
            $file.find('.file-footer-caption').text($block.data().req.data_name);
            return $file;
        },
        /* chunggilee implementation */
        drawCanvas: function (canvas_id) {
            for ($i = 0; $i < 3; $i++) {
                document.getElementsByName("canvas_picker")[$i].style.display = "none";
            }
            document.getElementById(canvas_id).style = "display:block; padding: 0; margin:auto;";
            canvasPicker = document.getElementById(canvas_id).getContext('2d');
            // create an image object and get it’s source
            var img = new Image();
            img.src = 'static/img/text-color.png';

            // copy the image to the canvas
            $(img).on('load', function () {
                canvasPicker.drawImage(img, 0, 0);
            });
        },
        rgbToHex: function (R, G, B) {
            return unitManager.toHex(R) + unitManager.toHex(G) + unitManager.toHex(B)
        },
        toHex: function (n) {
            n = parseInt(n, 10);
            if (isNaN(n)) return "00";
            n = Math.max(0, Math.min(n, 255));
            return "0123456789ABCDEF".charAt((n - n % 16) / 16) + "0123456789ABCDEF".charAt(n % 16);
        },
        colorChange: function (colorValue) {
            if (colorValue == "Green, Black, Red") {
                document.getElementById('btn-color1').style.background = "#00ff00";
                document.getElementById('btn-color2').style.background = "#000000";
                document.getElementById('btn-color3').style.background = "#ff0000";
                this.colorArr = ["#00ff00", "#000000", "#ff0000"];
            } else if (colorValue == "Blue, White, Red") {
                document.getElementById('btn-color1').style.background = "#0000ff";
                document.getElementById('btn-color2').style.background = "#ffffff";
                document.getElementById('btn-color3').style.background = "#ff0000";
                this.colorArr = ["#0000ff", "#ffffff", "#ff0000"];
            } else if (colorValue == "Red, Orange, Yellow") {
                document.getElementById('btn-color1').style.background = "#ffff00";
                document.getElementById('btn-color2').style.background = "#ffa500";
                document.getElementById('btn-color3').style.background = "#ff0000";
                this.colorArr = ["#ffff00", "#ffa500", "#ff0000"];
            }
        },
        createVisTypesOptions: function (data) {
            var options = data.vis_types;
            if (options == undefined) options = CLS;
            var $vis_types = $('#vis_types');
            //$vis_types.append($('<option disabled selected>Select Visualization Method</option>'));
            _.map(options, function (item, idx) {
                var $option = $('<option></option>');
                $option.text(item.visTypes);
                $option.val(item.visTypes);
                $vis_types.append($option);
            });
            $vis_types.on("change", {options: options}, unitManager.changeVisTypesOptions);
            $vis_types.prop("selectedIndex", 0).change();
        },
        changeVisTypesOptions: function (e) {
            if ($(this).val() == "Scatter Plot") {
                $('div.SPaxes').css('display', 'block');
            } else {
                $('div.SPaxes').css('display', 'none');
            }
            /*
             var data = e.data.options;
             console.log(this.value);
             var param = _.find(data, {visTypes: this.value}).visTypes;
             var $visTypes = $('div.vis-types');
             //$visTypes.empty();
             //$clusterParamter.append($('<br>'));
             var $param = null;
             //unitManager.logger('Change-Cluster-Type', unitManager.getLoggerObj({cluster_type: this.value}));
             */
        }
    })
})(unitManager);
