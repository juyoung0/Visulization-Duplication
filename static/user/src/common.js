/**
 * Created by dryji on 2017-02-22.
 */

var init_history_panel = true;

function writeDownloadLink(svg, title) {
    try {
        var isFileSaverSupported = !!new Blob();
    } catch (e) {
        alert("blob not supported");
    }

    var html = d3.select(svg)
        .attr("title", title)
        .attr("version", 1.1)
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .node().parentNode.innerHTML;

    var blob = new Blob([html], {type: "image/svg+xml"});
    saveAs(blob, title + ".svg");
}

function saveAs(blob, filename) {
    var svgUrl = URL.createObjectURL(blob);
    var downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

function sliderToggle(e) {

    var prevActive = $('li.btn-slider.active');
    var active = _.without($(this).attr('class').split(" "), "active", "btn-slider").pop();
    var sl = $('.btn-toggle-slider1');
    var slider = $('.navmenu');
    var sl_menu = $('.slider-menu');

    slider.off('hidden.bs.offcanvas');

    // hide all slider menu
    sl_menu.css('display', "none");

    if (prevActive[0] == $(this)[0]) {
        $(slider[1]).offcanvas('hide');
        prevActive.removeClass('active');
        return;
    }

    // if there is toggled menu open slider
    if (prevActive.length == 0) sl.click();

    prevActive.removeClass('active');
    $(this).addClass('active');
    $('#' + active).css('display', 'block');

    $block = unitManager.SELECTED;

    var reqObj = {
        username: userManager.USERNAME,
        project_name: userManager.PROJECT,
        session_name: userManager.SESSION,
        session_ver: userManager.SESSION_VER
    };

    // call functions for each menu;
    switch (active) {
        case 'slider-history':
            // init panel construct
            if (init_history_panel) {
                loadHistory();
                init_history_panel = false;
            } else {
                // init session history tree.
                if ($('#history_tree').children().length == 0) {
                    historyManager.getSessionHistory();
                }
            }
            //userManager.logger('Click-Sankey-Tab', reqObj, 'Tab');
            break;
        case 'slider-heatmap':
          // userManager.logger('Click-Menu-Tab', reqObj, 'Tab');
            break;
        case 'slider-folder':
            //userManager.logger('Click-Table-Tab', reqObj, 'Tab');
            visualizer.createStatTable(changedSelection);
            //visualizer.appendLogger();
            break;
        case 'slider-network':
            visualizer.createNetworkTable({output: []});
            break;
    }

}

function failAjax(xhr, status, error) {
    if (xhr['success'] == false) {
        alert(xhr.detail);
    } else {
        alert('xhr error');
    }
    console.log(xhr, error);
}

function loadHistory() {
    require(["dojo/parser", "dijit/layout/BorderContainer", "dijit/layout/ContentPane", "dojo/domReady!"], function (parser, BorderContainer, ContentPane) {
        var bc = new BorderContainer({
            style: "height:100%;width:100%;padding:0;margin:0;border:1;overflow:hidden",
            design: "sidebar",
            gutters: false,
            liveSplitters: true
        });

        // create a ContentPane as the left pane in the BorderContainer
        var cp1 = new ContentPane({
            region: "top",
            style: "height: 30%;width:100%;overflow:hidden",
            splitter: true,
            class: "history-table-container",
            id: "dojo-table-container",
            content: '<table class="table table-bordered" width="100%" id="#action_history_table"></table>'
        });
        var cp2 = new ContentPane({
            region: "center",
            style: "height: 70%;width:100%;overflow:hidden",
            splitter: true,
            class: "history-tree-container",
            content: '<svg id="history_tree" width="100%" height="100%"></svg>'
        });
        bc.addChild(cp1);
        bc.addChild(cp2);
        document.getElementById("slider-history").appendChild(bc.domNode);
        bc.startup();

        // call session history tree.
        historyManager.getSessionHistory();

        // init action tree table
        visualizer.createActionHistoryTable({output: []});

    });
    require(["dojo/ready", "dojo/aspect", "dijit/registry"], function (ready, aspect, registry) {
        ready(function () {
            aspect.after(registry.byId("dojo-table-container"), "resize", function () {
                var newHeight = this.h - 15;
                var myTable = $('#action_history_table')
                var oSettings = myTable.dataTable().fnSettings();
                oSettings.oScroll.sY = newHeight + "px";
                $('#action_history_table_wrapper').find('.dataTables_scrollBody').height(newHeight);
            });
        });
    });
}