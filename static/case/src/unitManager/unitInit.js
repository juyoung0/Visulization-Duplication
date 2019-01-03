/**
 * Created by dryji on 2017-02-20.
 */
var unitManager = {
    SELECTED: undefined,
    EDIT_MODE: false,
    basicUrl: "geromics/",
    blockMap: {},
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
        $.ajax({url: 'visTypes.html',
            success: unitManager.createVisTypesOptions,
            error: unitManager.failAjax});


        // <-- logger events
        $('#block_data').on('fileloaded', function (event) {
            console.log("change-file");
            unitManager.changeData(unitManager.SELECTED);
        });

        $('#block_name').on('blur', function (e) {
            if (!unitManager.EDIT_MODE) return;
            console.log("change-unit-name");
            if (unitManager.SELECTED.data().req.block_name && unitManager.SELECTED.data().req.block_name != $("#block_name").val())
                unitManager.changeName(unitManager.SELECTED);
        }).on('change',function (e) {
            unitManager.EDIT_MODE = true;
        });


        $('.btn-create-annotation').on('click', function (e) {
            unitManager.createUnitAnnotation(unitManager.SELECTED)
        });

        // event for block editor
        $('.btn-block-new').on('click', function (e) {
            console.log(e);
            e.preventDefault();
            e.stopPropagation();
            unitManager.createUnit();
            unitState = "new";
        });

        $('.btn-block-branch').on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            unitManager.branchUnit();
            unitState = "branch";
        });
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

        $('.btn-grid').on('click',function (e) {
            unitManager.gridUnits();
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
                color_type: JSON.stringify(unitManager.colorArr)
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
            error: userManager.failAjax
        }).done(function (data, status) {
            console.log(data);
        });
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
        unitManager.logger('Change-Data', unitManager.getLoggerObj({
            data: $('textarea.file-preview-text').val(),
            data_name: $('div.file-footer-caption').text()
        }));
    }
};