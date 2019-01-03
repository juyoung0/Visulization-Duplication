/**
 * Created by dryji on 2017-02-22.
 */
(function (parent) {
    _.extend(parent, {
        getUnitHistory: function (session_name, session_ver) {
            $.ajax({
                url: "actionHistory.html",
                method: 'post',
                data: {
                    username: userManager.USERNAME,
                    session_name: session_name,
                    session_ver: session_ver,
                    project_name: userManager.PROJECT
                },
                error: userManager.failAjax,
                success: historyManager.successGetUnitHistory
            });
        },
        successGetUnitHistory: function (data, status) {
            if (!data.success) return userManager.failAjax(data, status);
            //$('#project-tree').attr('transform', "translate(0,100)scale(0.2)");
            /*
            d3.select('#project-tree').selectAll('text').classed('hide', true);
            d3.select('#border-rect').classed('hide', false).classed('border-rect', true).on('click', function (d) {

                $('#history_tree').remove();

                d3.select('.history-tree-container')
                    .append('svg')
                    .attr('id', 'history_tree')
                    .attr('width', '100%')
                    .attr('height', '100%');

                historyManager.getSessionHistory();
            });
            d3.select('#history_tree').attr('opacity', 1);
            */
            visualizer.createUnitTree(data.output);
            visualizer.D_SANKEY = null;
        }
    })
})(historyManager);
