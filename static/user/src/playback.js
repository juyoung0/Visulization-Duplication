/**
 * Created by juyoung on 2017-06-26.
 */

var unitNum = 0;
var unit_list = [];
var action_nums = [];
var sp_x = "";
var sp_y = "";
var pause = false;
var stop = false;
var stop_loc = 0;
var play_num = 0;
var table_row = 0;
var TableIsOpen = false;
var SankeyIsOpen = false;
var MenuIsOpen = true;
var AnnoIsOpen = false;
var anno_block = 0;
var initalize_list = false;
var min_unit = 0;
var logs;
var branch_list = [];

isPlayback = true;

window.get_logs = function() {

    if(!(pause || stop)) {
        if (AnnoIsOpen) {
            close_annotation(anno_block);
            setTimeout(function () {
            }, 3000);
        }

        if (!initalize_list) {
            $.getJSON("static/userLogs/juyoung3.json", function (data) {
                logs = data.output;
                unitNum = logs.length;
                console.log(logs);

                for (var j = 0; j < unitNum; j++) {

                    unit_list[logs[j].block_iden] = {};
                    unit_list[logs[j].block_iden].vis_type = logs[j].vis_types;
                    unit_list[logs[j].block_iden].action_list = logs[j].action_list;
                    unit_list[logs[j].block_iden].anno_path = logs[j].annotation_path;
                    unit_list[logs[j].block_iden].anno_num = 0;
                    unit_list[logs[j].block_iden].block_ver = logs[j].block_ver;
                    unit_list[logs[j].block_iden].block_name = logs[j].block_name;
                    action_nums[logs[j].block_iden] = 0;

                    if(logs[j].block_name != null){
                        if(logs[j].block_name.length > 3)
                            branch_list[logs[j].block_iden] = 1;
                        else
                            branch_list[logs[j].block_iden] = 0;
                    }else{
                        branch_list[logs[j].block_iden] = 0;
                    }

                    if (logs[j].vis_types == "Scatter Plot") {
                        for (var i = 0; i < logs[j].action_list.length; i++) {
                            if (logs[j].action_list[i].action == "Brush-SP-Axis") {
                                unit_list[logs[j].block_iden].sp_x = logs[j].action_list[i].parameter.x_axis;
                                unit_list[logs[j].block_iden].sp_y = logs[j].action_list[i].parameter.y_axis;
                                i += logs[j].action_list.length;
                            }
                        }
                    }

                    if (logs[j].vis_types == "Parallel Coordinate Plot") {
                        unit_list[logs[j].block_iden].prev_order = "[1,2,3,4,5,6,7,8]"
                    }
                }

                initalize_list = true
            });
        }
        if (initalize_list) {
            var id = 0;
            var min_action = 1000000;
            for (var i = 0; i < unitNum; i++) {
                id = logs[i].block_iden;
                if (unit_list[id].action_list.length > action_nums[id] + 1) {
                    var action = unit_list[id].action_list[action_nums[id]];

                    if (min_action > action.action_id) {
                        min_action = action.action_id;
                        min_unit = id;

                    }
                }
            }
            console.log(min_unit);
            console.log(action_nums);

            if(branch_list[min_unit] == 1){
                $('#block_name').val( unit_list[min_unit].block_name);
                while(unit_list[min_unit].action_list[action_nums[min_unit]].action != "Branch-Unit") {
                    play(unit_list[min_unit].action_list[action_nums[min_unit]], min_unit, unit_list[min_unit]);
                    action_nums[min_unit]++;
                    branch_list[min_unit] = 0;
                }
                action_nums[min_unit]++;
            }else {
                play(unit_list[min_unit].action_list[action_nums[min_unit]], min_unit, unit_list[min_unit]);
                action_nums[min_unit]++;
            }


        }
        setTimeout(get_logs, 3000);
    }

}

function play(log, block_iden, vis) {

    var vis_type = vis.vis_type;
    var block_ver = vis.block_ver;
    var anno_path = vis.anno_path;
    var action = log.action;
    console.log("----------");
    console.log(action);
    visualizer.unitDehighlight();
    select_unit(log, block_iden);

    switch(action) {
        case "Create-Unit":
            unitManager.empty = true;
            create_unit(log, block_iden, vis_type);
            console.log("created now");
          //  locate_unit(log, block_iden);
            break;
        case "Delete-Unit":
            delete_unit(log, block_iden);
            break;
        case "Select-Unit":
            select_unit(log, block_iden);
            break;
        case "Save-Unit":
            save_unit(log, vis_type, block_iden, block_ver);
            break;
        case "Branch-Unit":
            select_unit(log, block_iden);
         //   branch_unit(log, block_iden);
            break;
        case "Locate-Unit":
            locate_unit(log, block_iden);
            break;
        case "Create-Unit-Annotation":
            create_unit_annotation(log, block_iden, anno_path);
            break;
        case "Delete-Unit-Annotation":
            break;
        case "Change-PCP-Column":
            select_unit(log, block_iden);
            change_PCP_column(log, block_iden);
            break;
        case "Brush-SP-Axis":
            select_unit(log, block_iden);
            brush_SP_axis(log, block_iden);
            break;
        case "Brush-PCP-Axis":
            select_unit(log, block_iden);
            brush_PCP_axis(log, block_iden);
            break;
        case "Brush-SCM-Axis":
            select_unit(log, block_iden);
            brush_SCM_axis(log, block_iden);
            break;
        case "Search-Table":
            search_table(log, block_iden);
            break;
        case "Search-Table-Row":
            search_table_row(log);
            break;
        case "Restore-Unit":
            restore_unit(log, vis_type);
            break;
        case "Unit-Workflow":
            unit_workflow(log);
            break;
        case "Click-Sankey-Tab":
            click_sankey_tab(log);
            break;
        case "Click-Table-Tab":
            click_table_tab(log);
            break;
        case "Click-Menu-Tab":
            click_menu_tab(log);
            break;
        case "Pin-Unit":
            pin_unit(log, block_iden);
            break;
        case "Unpin-Unit":
            unpin_unit(log, block_iden);
            break;
    }


}

window.playback_start = function() {
    stop = false;
    pause = false;
    get_logs();
}

window.playback_pause = function() {
    pause = true;
}

window.playback_stop = function() {
    stop = true;
    play_num = 0;
    initialize_list = false;
}

function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

function create_unit(log, block_iden, vis_type, block_name){
    $('#block_name').val(log.parameter.block_name);
    if (vis_type == "Scatter Plot") {
        $('#SPxAxis').val(unit_list[block_iden].sp_x);
        $('#SPyAxis').val(unit_list[block_iden].sp_y);
    }
    $('#vis_types').val(vis_type);
    $('#block_note').val("");
    $('#cluster_list').val("");
    $('#cluster_param').val("");

    unitManager.createUnit();
    unit_id = unitManager.SELECTED.data().req.block_iden;
    unit_list[block_iden].id = unit_id;
}

function delete_unit(log, block_iden){
    unit_id = block_iden;
    unitManager.deleteUnit(unit_id);
}

function select_unit(log, block_iden){
    if (unit_list[block_iden].id == null) {
        return;
    }
    else {
        $block = $('#'+unit_list[block_iden].id);
        $('.block').removeClass('selected-block');
        $block.addClass('selected-block');
        unitManager.selectUnit($block);
    }
}

function save_unit(log, vis_type, block_iden, block_ver){

    if (vis_type == "Scatter Plot") {
        $('#SPxAxis').val(unit_list[block_iden].sp_x);
        $('#SPyAxis').val(unit_list[block_iden].sp_y);
    }
    $('#vis_types').val(vis_type);
    $('#block_note').val("");
    $('#cluster_list').val("");
    $('#cluster_param').val("");
    $('#block_name').val($('#block_name').val());

    $block = unitManager.SELECTED;

    if(block_ver == 0)
        unitManager.updateUnit($block, false, false);
    else
        unitManager.updateUnit($block, true, false);
}

function branch_unit(log, block_iden){
    //$block = unitManager.SELECTED;
    $block = $('#'+unit_list[block_iden].id);
    unitManager.branchUnit($block);
}

function locate_unit(log, block_iden){

    if (unit_list[block_iden].id == null) {
        return;
    }
    $block  = $('#'+unit_list[block_iden].id);

    if($block != null) {
        unitManager.selectUnit($block);

        $block.css('position', 'absolute');
        if (log.action == "Locate-Unit") {
            p = log.parameter.position;
            $block.animate({
                'left': p.position_left,
                'top': p.position_top,
                'width': p.position_width,
                'height': p.position_height
            }, 1000);
        }
        else {
            p = {position_left: 0, position_top: 0, position_width: 800};
            $block.animate({'left': p.position_left, 'top': p.position_top, 'width': p.position_width}, 1000);
        }
    }

}

function create_unit_annotation(log, block_iden, anno_path){
    $block = unitManager.SELECTED;
   // unitManager.getAnnotations(anno_path, $block);

    $('textarea.input-data-note').val("test");
    unitManager.createUnitAnnotation($block);

    var annos = $block.find('.annotation-item');
  //  annos[annos.length-1].click();
/*
    $(anno).popover('toggle');
    $('[data-toggle="popover"]').popover({html: true});

    wait(1000);
    $('[data-toggle="popover"]').popover('hide');
    */

}

function open_annotation(block_iden){
    console.log("open annotation");
    $block  = $('#'+unit_list[block_iden].id);
    var anno_num = unit_list[block_iden].anno_num;
    $block.find('.annotation').find('a').find('#anno-'+anno_num).click();
    unit_list[block_iden].anno_num++;
    AnnoIsOpen = true;
    anno_block = block_iden;
}

function close_annotation(block_iden){
    console.log("close annotation");
    $block = unitManager.SELECTED;
    var anno_num = unit_list[block_iden].anno_num - 1;
    $block.find('.annotation').find('a').find('#anno-'+anno_num).click();
    AnnoIsOpen = false;
}

function delete_unit_annotation(log){
    unitManager.deleteUnitAnnotation(log.parameter.annotation_num);
}

function change_PCP_column(log, block_iden){


    var position = JSON.parse(log.parameter.column_order);
    var svg = d3.select("#" + unit_list[block_iden].id).select('svg');
    var dimensions = svg.selectAll(".dimension");
    var foreground = svg.selectAll(".foreground");
    var background = svg.selectAll(".background");
    var prev_position = unit_list[logs[j].block_iden].prev_order;
    var first = 0;
    var second = 0;
    for (var i=0; i<position.length; i++){
        if(position[i] != prev_position[i]){
            if(first == 0)
                first = i+1;
            else
                second = i+1;
        }
    }

    dimensions.call(drag(position));

    /*
    var width = 950;
    var x = d3.scalePoint().range([0, width]),  y = {};
    var line = d3.line();

    var dragBehavior = d3.drag().on("drag", dragCallback);

    dimensions.call(dragBehavior);
    dragCallback();


    background.attr("visibility", "hidden");
   foreground.attr("d", path);

    dimensions.sort(function(a, b) { return position[a] - position[b]; });
    x.domain(dimensions);
    dimensions.attr("transform", function(d) { return "translate(" + position[d] + ")"; });

    dimensions.transition().duration(500).attr("transform", function(d) { return "translate(" + x(d) + ")";});
    foreground.transition().duration(500).attr("d", path);
    background
        .attr("d", path)
        .transition()
        .delay(500)
        .duration(0)
        .attr("visibility", null);
*/

    $block = $('#'+unit_list[block_iden].id);
    $block.data(log.parameter);
    unit_list[logs[j].block_iden].prev_order = position;
}




function brush_SP_axis(log, block_iden){
    var svg = d3.select("#" + unit_list[block_iden].id).select('svg');
    svg.selectAll('.sp_brush').remove();
    var brushRange = JSON.parse(log.parameter.brushed_range);
    svg.append("rect")
        .attr("class", "sp_brush")
        .attr("x", brushRange[0][0])
        .attr("y", brushRange[0][1])
        .attr("width",  brushRange[1][0] - brushRange[0][0])
        .attr("height", brushRange[1][1] - brushRange[0][1])
        .attr("fill", "none")
        .attr("stroke", "blue");

    var indexList = JSON.parse(log.parameter.selected_index);

    if (indexList.length == 0)
        svg.selectAll(".dots").classed("hidden", false);
    else {
        svg.selectAll(".dots").classed("hidden", true);
        indexList.forEach(function (d, i) {
            svg.selectAll(".dot_" + indexList[i]).classed("hidden", false);
        })
    }

   // visualizer.spInteraction(indexList);

//    var cell = d3.select(".cell."+unit_list[block_iden].id);
    /*
    var cell = d3.select(".cell."+unit_list[block_iden].id);
    var brush = cell._groups[0][0].__brush;
    var brushRange = JSON.parse(log.parameter.brushed_range);
    if(brushRange[0] == [0,0] && brushRange[1] == [0,0]){}
    else {
       // brush.extent = brushRange;
        //brush.selection.x = brushRange[0][0];
       // brush.selection.y = brushRange[0][1];
       // brush.selection.width = brushRange[1][0] - brushRange[0][0];
       // brush.selection.height = brushRange[1][1] - brushRange[0][1];
        //   d3.select(cell).call(brush.move, brushRange);
     //   cell.transition()
            //.call(brush.extent (brushRange))
       //     .call(brush.event);

        var brush = $('#brush_'+unit_list[log.parameter.block_iden]);
        brush.extent(brushRange);
        d3.selectAll("." + unit_list[log.parameter.block_iden]).call(brush.move, brushRange);

    }
    */

    changedSelection = indexList;
}

function brush_PCP_axis(log, block_iden){
    var brushAxis = JSON.parse(log.parameter.brushed_axis);
    var brushRange = JSON.parse(log.parameter.brushed_range);

    var svg = d3.selectAll("#" + unit_list[block_iden].id); //.select('svg');
  //  var brushes = svg.selectAll(".brush");
    svg.selectAll('.pcp_brush').remove();
    var brush;

    for(var i=0; i<brushAxis.range; i++){
        if (brushAxis[i] == 1) {
            brush = svg.select('.axis_' + (i + 1));
            brush.append('rect')
                .attr("class", "pcp_brush")
                .attr("x", -10)
                .attr("y", brushRange[i][0])
                .attr("width", 20)
                .attr("height", brushRange[i][1] - brushRange[i][0])
                .attr("fill", "none")
                .attr("stroke", "blue");
        }
    }

    var indexList = JSON.parse(log.parameter.selected_index);


    if (indexList.length == 0)
            svg.selectAll(".foreground").style("display", "inline");
    else {
        svg.selectAll(".foreground").style("display", "none");
        indexList.forEach(function (d, i) {
            svg.selectAll(".ind_" + d).style("display", "inline");
        });
    }

    changedSelection = indexList;
   // visualizer.pcpInteraction(indexList);
}

function brush_SCM_axis(log, block_iden){
    var brushAxis = JSON.parse(log.parameter.brushed_axis);
    var brushRange = JSON.parse(log.parameter.brushed_range);

    var svg = d3.select("#" + unit_list[block_iden].id).select('svg');
    svg.selectAll('.scm_brush').remove();
    var cell = svg.selectAll(".cell.i_" + brushAxis[0] + ".j_" + brushAxis[1]);

    cell.append('rect')
        .attr("class", "scm_brush")
        .attr("x", brushRange[0][0])
        .attr("y", brushRange[0][1])
        .attr("width",  brushRange[1][0] - brushRange[0][0])
        .attr("height", brushRange[1][1] - brushRange[0][1])
        .attr("fill", "none")
        .attr("stroke", "blue");

    var indexList = JSON.parse(log.parameter.selected_index);

    if (indexList.length == 0)
            svg.selectAll(".circles").classed("hidden", false);
    else {
        svg.selectAll(".circles").classed("hidden", true);
        indexList.forEach(function (d, i) {
            svg.selectAll(".circle_" + indexList[i]).classed("hidden", false);
            svg.selectAll(".circle_" + indexList[i]).attr("r", 2);
        })
    }

    changedSelection = indexList;
  //  visualizer.scmInteraction(indexList);
}

function search_table(log, block_iden){
    table_row = 0;

    if (!TableIsOpen) {
        $("#document_icon").click();
        TableIsOpen = true;
    }else{

        $block = $('#'+unit_list[block_iden].id);
        $block.find('.show-table').click();
    }

    //SankeyIsOpen = false;
}

function search_table_row(log){
    var table = $('.selection-table').DataTable();
    visualizer.unitDehighlight();

    table_row = log.parameter.selected_index;
    table.rows().nodes().removeClass( 'hover' );
    table.rows( table_row ).nodes().addClass( 'hover' );

   // $( table.cells().nodes() ).removeClass( 'highlight' );
   // $( table.column( table_row ).nodes() ).addClass( 'highlight' );
    if(log.parameter.selected_index == null) {
        visualizer.unitHighlight([table_row]);
    }
    else{
        index = log.parameter.selected_index;
        visualizer.unitHighlight([index[1]]);
    }

    table_row ++;
}

function restore_unit(log, vis_type){
    if (vis_type == "Scatter Plot") {
        $('#SPxAxis').val(sp_x);
        $('#SPyAxis').val(sp_y);
    }
    $('#vis_types').val(vis_type);
    $('#block_note').val("");
    $('#cluster_list').val("");
    $('#cluster_param').val("");
    $('#block_name').val($('#block_name').val());
    console.log($('#block_name').val());
    $block = unitManager.SELECTED;
    unitManager.updateUnit($block, false, true);
}

function unit_workflow(log){

    if(!SankeyIsOpen) {
        $("#history_icon").click();
        SankeyIsOpen = true;
    }

    if ($('#history_tree').children().length == 0)
        historyManager.getSessionHistory();

    // show this session
//    visualizer.showSession(data);
    visualizer.transformToMiniMap();
 //   visualizer.D_SANKEY = {id:data.name,ver:data.ver};
//    historyManager.getUnitHistory(data.name, data.ver);
    TableIsOpen = false;
    MenuIsOpen = false;
}



function click_sankey_tab(log){
    $("#history_icon").click();

    if(SankeyIsOpen)
        SankeyIsOpen = false;
    else
        SankeyIsOpen = true;
}

function click_table_tab(log){
    $("#document_icon").click();

    if(TableIsOpen)
       TableIsOpen = false;
    else
        TableIsOpen = true;
}

function click_menu_tab(log){
    $("#menu_icon").click();

    if(MenuIsOpen)
       MenuIsOpen = false;
    else
        MenuIsOpen = true;
}

function pin_unit(log, block_iden){
    $block = $('#'+unit_list[block_iden].id);
    $block.find('.fix-block').click();
}

function unpin_unit(log, block_iden){
    $block = $('#'+unit_list[block_iden].id);
    $block.find('.fix-block').click();
}

function drag(pos){
    console.log('dragging');
    return d3.drag()
         .origin(function() {
            var g = this;
            return {x: d3.transform(g.getAttribute("transform")).translate[0],
                    y: d3.transform(g.getAttribute("transform")).translate[1]};
        })
        .on("drag", function(d) {

            g = this;
            translate = d3.transform(g.getAttribute("transform")).translate;

            x = d3.event.dx + translate[0],
            y = d3.event.dy + translate[1];


            d3.select(g).attr("transform", "translate(" + x + "," + y + ")");
            d3.event.sourceEvent.stopPropagation();
        });
}