/**
 * Created by ys on 2017-03-15.
 *//*
(function (parent) {
    _.extend(parent,{
        unitCopy : function(test) {

            console.log('check ok');

            $.ajax({
                url: "unitCopy.html",
                method: "post",
                data: {username:"chung", project_name:"pj", session_name:"day1", session_ver:0, block_iden:"U-0896", block_ver:0,target_session_name : "day4", target_session_ver:0, target_block_iden:"U-9696", target_block_ver:0 },
                error: userManager.failAjax,
                success: historyManager.successUnitCopy
            });
        },
        successUnitCopy: function (data, status) {
            if (!data.success) return userManager.failAjax(data, status);

            console.log('ok')

        }
    })
})(historyManager);*/