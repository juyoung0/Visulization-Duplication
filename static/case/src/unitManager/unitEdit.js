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
        branchUnit: function ($block, reqObj) {
            if ($block != null && $block.length == 0) {
                alert("Can't find the unit to branch.");
                return;
            }
            //console.log("branch");
            if ($block == null) $block = unitManager.SELECTED;
            //console.log($block.data().req);
            //var blockId = unitManager.getBlockId();
            /*
             if(selectedIndex.length == "[]")
             selectedIndex = changedSelection;
             //console.log(selectedIndex);
             */

            var $blockName;
            var $blockVer;
            if (reqObj == null){
                reqObj = {};
                reqObj.cluster_type = $block.data().req.cluster_type;
                reqObj.cluster_param = $block.data().req.cluster_param;
                reqObj.color_type = $block.data().req.color_type;
                reqObj.data = $block.data().req.data;
                reqObj.parent_block_iden = $block.data().req.block_iden;
                reqObj.parent_block_ver = $block.data().req.block_ver;
                reqObj.data_name = $block.data().req.data_name;
                reqObj.vis_types = $block.data().req.vis_types;
                reqObj.block_name = $block.data().req.block_name + "-B" + _.filter($('.block'),function (item) {
                        if ($(item).data().req.block_name.indexOf($block.data().req.block_name + "-B") != -1) return true;
                    }).length + 1;
                if ($block.data().req.vis_types == "Heatmap") {
                    reqObj.cluster_type = $block.data().req.cluster_type;
                    reqObj.cluster_param = $block.data().req.cluster_param;
                    reqObj.color_type = $block.data().req.color_type;
                } else if ($block.data().req.vis_types == "Parallel Coordinate Plot") {
                    var selectedIndex = JSON.parse($block.data().req.selected_index);
                    reqObj.selected_index = JSON.stringify(changedSelection); //$block.data().req.selected_index;//
                    reqObj.column_order = JSON.stringify(changedOrder);//$block.data().req.column_order;//
                } else if ($block.data().req.vis_types == "Scatterplot Matrix") {
                    var selectedIndex = JSON.parse($block.data().req.selected_index);
                    reqObj.selected_index = JSON.stringify(changedSelection);//$block.data().req.selected_index;//JSON.stringify(selectedIndex);
                }
                $blockName= $('#block_name').val();
                $blockVer= $block.data().req.block_ver;
            }else{
                reqObj.parent_block_iden = reqObj.block_iden;
                reqObj.parent_block_ver = reqObj.block_ver;
                reqObj.block_name = reqObj.block_name + "-B" + _.filter($('.block'),function (item) {
                        if ($(item).data().req.block_name.indexOf(reqObj.block_name + "-B") != -1) return true;
                    }).length + 1;
            }
            reqObj.block_ver = 0;
            reqObj.username = userManager.USERNAME;
            reqObj.session_name = userManager.SESSION;
            reqObj.session_ver = userManager.SESSION_VER;
            reqObj.project_name = userManager.PROJECT;
            // create new block
            var $newBlock = unitManager.addUnit();
            reqObj.block_iden = $newBlock.data().req.block_iden;
            reqObj.position = JSON.stringify(unitManager.getBlockPosition($newBlock));


            $.ajax({
                url: "clusters.html",
                method: 'post',
                data: reqObj,
                error: userManager.failAjax,
                complete: function (d, s) {
                    if (visualizer.D_SANKEY != null) {
                        //console.log('redraw unit tree',$block, visualizer.D_SANKEY);
                        historyManager.getUnitHistory(visualizer.D_SANKEY.id, visualizer.D_SANKEY.ver);
                    }
                }
            }).done(function (data, status) {
                if (!data.success) return userManager.failAjax(data, status);

                //$block.attr('data', JSON.stringify({req: reqObj, res: data}));
                if (!data.errors) {
                    data = data.output;
                    reqObj.block_ver = data.block_ver;
                    $newBlock.data({req: reqObj, res: data, position: JSON.parse(reqObj.position)});
                    var $blockTitle = $newBlock.find('.block-title');
                    $blockTitle.text(reqObj.block_name);

                    if (data.vis_types == "Heatmap" || data.vis_types == null) {
                        unitManager.createGeneList({res: data}, $newBlock);
                        visualizer.createHeatmap(data.cluster_data, data.label, data.name_data, reqObj.block_iden, "main");
                    }
                    else if (data.vis_types == "Parallel Coordinate Plot")
                        visualizer.createPCP(data.data, blockId, $blockVer, $blockName, "main", JSON.parse(data.column_order), JSON.parse(data.selected_index));
                    else if (data.vis_types == "Scatterplot Matrix")
                        visualizer.createSCM(data.data, blockId, $blockVer, $blockName, "main", JSON.parse(data.selected_index));

                    unitManager.logger('Branch-Unit', reqObj);
                    unitManager.selectUnit($newBlock);
                    //unitManager.selectUnit($newBlock);

                    //refresh session
                    //visualizer.refreshSession();
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
                //console.log('delete block', blockId, data);
                reqObj.block_name = $block.data().req.block_name;
                unitManager.logger('Delete-Unit', reqObj);
                $block.remove();
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
            $("#cluster_list").on("change", {options: options}, unitManager.changeClusterType).on('focus', function (e) {
                unitManager.EDIT_MODE = true;
            });
        },
        changeClusterType: function (e) {
            var data = e.data.options;
            //console.log(this.value, 'changeClusterType', data);
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
            $param.on('focus', function (e) {
                unitManager.EDIT_MODE = true;
            });
            if ($param != null) {
                $param.on('blur', function (e) {
                    if (unitManager.SELECTED.data().req.cluster_param != $param.val()) {
                        if (!unitManager.EDIT_MODE) return;
                        unitManager.logger('Change-Cluster-Parameter', unitManager.getLoggerObj({cluster_param: $param.val()}));
                    }
                });
            }
            if (!unitManager.EDIT_MODE) return;
            unitManager.logger('Change-Cluster-Type', unitManager.getLoggerObj({cluster_type: this.value}));
        },
        /**
         * selected unit would be saved in unitManager.SELECTED
         * @param $block
         */
        selectUnit: function ($block) {
            if ($block.length == 0) {
                alert("Can't find the selected unit in the current session.");
            }
            // switch to DIsplay mode
            unitManager.EDIT_MODE = false;
            ////console.log('select unit ', $block);
            unitManager.SELECTED = $block;
            $('div.block').css('z-index', 1);
            $block.css('z-index', 30);
            var block_param = $block.data();
            $('#block_name').val(block_param.req.block_name);
            $('.block').removeClass('selected-block');
            $block.addClass('selected-block');
            // load gesa if $block has data
            if($block.data().gesa != null){
                var gesa=$block.data().gesa;
                moduleNetwork.getGesa(gesa.genes,gesa.species);
            }
            /*
             //console.log(block_param.req);
             changedSelection = JSON.parse(block_param.req.selected_index);
             changedOrder = JSON.parse(block_param.req.column_order);
             //console.log(changedSelection);
             //console.log(changedOrder);*/
            //unitManager.logger('Select-Unit', unitManager.getLoggerObj({block_name: block_param.req.block_name}));

            /// switching menu based on vis_type
            if (block_param.req.gene_list != null) {
                $('.vis-types').hide();
                $('.vis-types.graph').show();
                if (block_param.res) {
                    $('div.file-input').removeClass('file-input-new');
                    unitManager.addBlockFile($block);
                    $('input.file').fileinput('refreshZoom');
                    $('.file-upload-indicator').remove();
                }
                return;
            }else {
                $('.vis-types').hide();
                $('.vis-types.heatmap').show();
                $('#cluster_color').val(block_param.req.color_type);
                /* chunggilee implementation */
                if (block_param.req.color_type != null) {
                    document.getElementById('btn-color1').style.background = JSON.parse(block_param.req.color_type)[0];
                    document.getElementById('btn-color2').style.background = JSON.parse(block_param.req.color_type)[1];
                    document.getElementById('btn-color3').style.background = JSON.parse(block_param.req.color_type)[2];
                    this.colorArr = JSON.parse(block_param.req.color_type);
                }
                if (block_param.res) {
                    $('#cluster_list').val(block_param.req.cluster_type).change();
                    $('#cluster_param').val(block_param.req.cluster_param);
                    $('div.file-input').removeClass('file-input-new');
                    unitManager.addBlockFile($block);
                    $('input.file').fileinput('refreshZoom');
                    $('.file-upload-indicator').remove();
                } else {
                    $('#cluster_list').val("");
                    $('#cluster_param').val("");
                    $('div.fileinput-remove').trigger('click');
                }
            }

        },
        /**
         * transData would transform dataformat from the server to the UI
         * @param data
         * @returns {{req: *, res, position}}
         */
        transData: function (data) {
            ////console.log('transData', data);
            var d = {
                req: data.request[0],
                res: data.response[0],
                position: data.position
            };
            if (d.req.gene_list !=null){
                d.req.data = d.req.gene_list;
                d.req.data_name = d.req.species;
            }
            if (d.req.block_name == null){
                d.req.block_name = "";
            }

            ////console.log('transData', d);
            return d;
        },
        getBlockId: function () {
            // 고유 ID 부여
            var d = new Date();
            var t = d.getTime();
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
            ////console.log('test block file');
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
            ////console.log($b,$file);
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
            $vis_types.append($('<option disabled selected>Select Visualization Method</option>'));
            _.map(options, function (item, idx) {
                var $option = $('<option></option>');
                $option.text(item.visTypes);
                $option.val(item.visTypes);
                $vis_types.append($option);
            });
            $vis_types.on("change", {options: options}, unitManager.changeVisTypesOptions);
        },
        changeVisTypesOptions: function (e) {
            var data = e.data.options;
            //console.log(this.value);
            var param = _.find(data, {visTypes: this.value}).visTypes;
            var $visTypes = $('div.vis-types');
            //$visTypes.empty();
            //$clusterParamter.append($('<br>'));
            var $param = null;
            //unitManager.logger('Change-Cluster-Type', unitManager.getLoggerObj({cluster_type: this.value}));
        }
    })
})(unitManager);
