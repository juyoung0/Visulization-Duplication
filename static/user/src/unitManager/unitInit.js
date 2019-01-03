/**
 * Created by dryji on 2017-02-20.
 */
var unitManager = {
    SELECTED: undefined,
    DELETED_UNITS:[],
    basicUrl: "geromics/",
    blockMap: {},
    selectedPath: "",
    empty: false,
    /* chunggilee implementation */
    colorArr: ["#00ff00", "#000000", "#ff0000"],

    init: function () {
        this.blockMap = {};

        // call clusters ui informatioin
        $.ajax({
            url: 'clusterList.html',
            success: unitManager.createClusterOptions,
            error: unitManager.failAjax
        });

        // call vistypes ui information
        $.ajax({
            url: 'visTypes.html',
            success: unitManager.createVisTypesOptions,
            error: unitManager.failAjax
        });


        // <-- logger events
        $('#block_data').on('fileloaded', function (event) {
            console.log("change-file");
            unitManager.changeData(unitManager.SELECTED);
        });

        $('#block_name').on('blur', function (e) {
            console.log("change-unit-name");
            if (unitManager.SELECTED.data().req.block_name != $("#block_name").val())
                unitManager.changeName(unitManager.SELECTED);
        });
        $('.btn-create-annotation').on('click', function (e) {
            unitManager.createUnitAnnotation(unitManager.SELECTED)
        });

        // event for block editor
        $('.btn-block-new').on('click', function (e) {
            console.log(e);
            e.preventDefault();
            e.stopPropagation();
            unitState = "new";
            unitManager.createUnit();
        });

        $('.btn-block-branch').on('click', function (e) {
            unitState = "branch";
            unitManager.branchUnit();
        });

        /* Juyoung Implemented for branche vis type */
        /*
         $(function() {
         $("#branchType").popover({
         html: true,
         content: function () {
         var clone = $($(this).data('popover-content')).clone(true).removeClass('hide');
         return clone;
         }
         });
         });

         $('#branchPCP').on('click', function (e) {
         e.preventDefault();
         e.stopPropagation();
         unitState = "branch";
         branchState = "pcp";
         console.log("branch pcp");
         $('[data-toggle="popover"]').popover('hide');
         unitManager.branchUnit();

         });

         $('#branchSCM').on('click', function (e) {
         e.preventDefault();
         e.stopPropagation();
         unitState = "branch";
         branchState = "scm";
         console.log("branch scm");
         $('[data-toggle="popover"]').popover('hide');
         unitManager.branchUnit();
         });
         */

        $('.btn-block-done').on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            unitManager.updateUnit(null, true);
        });
        $('.btn-block-display').on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            unitManager.updateUnit(null, false);
        });

        /* chunggilee implementation */
        // colorpicker
        var canvasPicker;
        $("canvas[name=canvas_picker]").click(function (event) {
            canvasPicker = document.getElementById(event.target.id).getContext('2d');
            // getting user coordinates
            var x = event.pageX - $('#' + event.target.id).offset().left;
            var y = event.pageY - $('#' + event.target.id).offset().top;
            // getting image data and RGB values
            var img_data = canvasPicker.getImageData(x, y, 1, 1).data;
            var R = img_data[0];
            var G = img_data[1];
            var B = img_data[2];
            var rgb = R + ',' + G + ',' + B;
            // convert RGB to HEX
            var hex = unitManager.rgbToHex(R, G, B);
            // making the color the value of the input
            document.getElementById(event.target.id).style.display = "none";
            var canvas_id = String(event.target.id);
            var num = canvas_id.charAt(canvas_id.length - 1);
            document.getElementById('btn-color' + String(num)).style.background = "#" + hex;
            unitManager.colorArr[num - 1] = "#" + hex;
            unitManager.logger('Change-Color', unitManager.getLoggerObj({
                color: JSON.stringify(unitManager.colorArr)
            }));
        });

    },
    logger: function (action, reqObj) {
        var SCOPE = 'unit';
        var reqObj = _.merge({scope: SCOPE, action: action}, reqObj);
        $.ajax({
            url: "insertLog.html",
            method: 'post',
            data: reqObj,
            error: unitManager.failAjax
        }).done(function (data, status) {
            if (!data.success) return userManager.failAjax(data, status);

            var d = reqObj;
            var folder;
            if (data.output.indexOf("/") > 0) {
                folder = data.output.split("/");
            } else {
                folder = data.output.split("\\");
            }

            if (folder[0] == "static") {
                var path = data.output;

                $.ajax({url: path, method: 'post'}).done(function (data) {
                    if (!data.request) return;
                    d = unitManager.transData(data).req;
                    unitManager.selectedData = d;

                    if (d.selected_index)
                        changedSelection = JSON.parse(d.selected_index);
                    if (d.column_order)
                        changedOrder = JSON.parse(d.column_order);
                    if (d.brushed_axis)
                        changedAxes = JSON.parse(d.brushed_axis);
                    if (d.brushed_range)
                        changedRange = JSON.parse(d.brushed_range);
                })
            }
        })

    },
    getLoggerObj: function (obj) {
        var block = unitManager.SELECTED.data().req;
        var reqObj = {
            username: userManager.USERNAME,
            project_name: userManager.PROJECT,
            session_name: userManager.SESSION,
            session_ver: userManager.SESSION_VER,
            block_iden: block.block_iden,
            block_ver: block.block_ver
        };
        return _.merge(reqObj, obj);
    },
    changeName: function ($block) {
        unitManager.logger('Change-Name', unitManager.getLoggerObj({
            block_name: $('#block_name').val()
        }));
    },
    changeData: function ($block) {
        //  d3.csv("static/csv/car.csv", function(error, dataset) {
        unitManager.logger('Change-Data', unitManager.getLoggerObj({
            data: $('textarea.file-preview-text').val(),
            data_name: $('div.file-footer-caption').text()
            //         data: "",
            //          data_name: "car.csv"
        }));
        //  });
    },
    changeNote: function ($block) {
        $block.data().name = $('#block_name').val();
    }, failAjax: function (xhr, status, error) {
        if (xhr['success'] == false) {
            alert(xhr.detail);
        } else {
      //      alert('xhr error');
        }
        console.log(xhr, error);
    }
}