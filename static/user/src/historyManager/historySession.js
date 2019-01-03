/**
 * Created by dryji on 2017-02-22.
 */
(function (parent) {
    _.extend(parent,{
        getSessionHistory: function () {
            if (userManager.PROJECT == null) {
                alert('There is a no selected project.');
                return;
            }
            $.ajax({
                url: "getSessionHistory.html",
                method: "post",
                data: {username: userManager.USERNAME, project_name: userManager.PROJECT},
                error: userManager.failAjax,
                success: historyManager.successGetSessionHistory
            });
        },
        successGetSessionHistory: function (data, status) {
            //if (!data.success) return userManager.failAjax(data, status);
            var setid = function (item) {
                if (item.ver == undefined) {
                    item.id = item.name + "_session";
                }
                else {
                    item.id = item.name + "_" + item.ver;
                }
                if (item.children) {
                    _.forEach(item.children, setid);
                }

            };
            console.log('successGetSessionHistory',data.output);
            setid(data.output);
            visualizer.createSessionTree(data.output);
        }
    })
})(historyManager);