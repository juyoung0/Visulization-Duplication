/**
 * Created by dryji on 2017-02-20.
 */
var historyManager = {
    HISTORY_HEIGHT: 0,
    UNABLE_UNDO:[],
    SESSION:{},
    init: function () {
        historyManager.getUnableUndoList();
    },
     failAjax: function (xhr, status, error) {
        alert('xhr error ' + error);
        console.log(xhr, error);
    },
    getUnableUndoList: function () {
        //{"unav_undo_list": [{"action": "Create-Unit"}, {"action": "Save-Unit"}, {"action": "Select-Unit"}, {"action": "Locate-Unit"}, {"action": "Apply-Unit"}, {"action": "Create-Unit-Annotation"}, {"action": "Delete-Unit-Annotation"}, {"action": "Update-Unit-Annotation"}]}
        return $.ajax({url: "unavUndo.html", error: historyManager.failAjax}).done(function (data, status) {
            historyManager.UNABLE_UNDO = _.map(data.unav_undo_list,function (item) {
                return item.action;
            });
        });
    }
};