/**
 * Created by dryji on 2017-02-20.
 */
// 히스토리 액션 핸들러
(function (parent) {
    _.extend(parent,
        {
            getActionHistory: function (list) {
                return $.ajax({
                    url: "fromToSession.html", data: {
                        username: userManager.USERNAME,
                        project_name: userManager.PROJECT,
                        session_list: JSON.stringify(list)
                    }, method: 'post', error: userManager.failAjax,
                    success: visualizer.createActionHistoryTable
                });
            },
            getUnitActionhistory: function (list) {
                return $.ajax({
                    url: "fromToUnit.html", data: {
                        username: userManager.USERNAME,
                        project_name: userManager.PROJECT,
                        session_name: userManager.SESSION,
                        session_ver: userManager.SESSION_VER,
                        block_list: JSON.stringify(list)
                    }, method: 'post', error: userManager.failAjax,
                    success: visualizer.createActionHistoryTable
                });
            },
            undoAction: function (block_list) {
                return $.ajax({
                    method: "POST",
                    url: "undoAction.html",
                    data: {action_list: JSON.stringify(block_list)},
                    error: historyManager.failAjax
                });
            },
            redoAction: function (block_list) {
                return $.ajax({
                    method: "POST",
                    url: "redoAction.html",
                    data: {action_list: JSON.stringify(block_list)},
                    error: historyManager.failAjax
                });
            },
            checkActionDependent: function (block_list) {
                return $.ajax({
                    method: "POST",
                    url: "depenCheck.html",
                    data: {action_list: JSON.stringify(block_list)},
                    error: historyManager.failAjax
                });
            }
        });
})(historyManager);

