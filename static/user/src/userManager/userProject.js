/**
 * Created by dryji on 2017-02-20.
 * handle user project.
 */
(function (parent) {
    _.extend(parent,
        {
            getProjects: function (username) {
                return $.ajax({
                    url: "getProjects.html",
                    method: 'post',
                    data: {username: userManager.USERNAME},
                    error: userManager.failAjax,
                    success: userManager.successGetProjects
                });
            },
            successGetProjects: function (data, status) {
                if (!data.success) return userManager.failAjax(data, status);
                //reset del units list on projects;
                unitManager.DELETED_UNITS=[];

                //console.log('successGetSessions', data);
                var $sel = $("select.project-list");
                $sel.empty();
                $sel.append($('<option selected disabled>Select your project.</option>'));
                _.forEach(data.output, function (item, idx) {
                    var $option = $('<option></option>');
                    //console.log(item.lastEdited, item['session_name']);
                    $option.text(item.lastEdited + ", " + item['project_name']);
                    $option.val(JSON.stringify(item));
                    $sel.append($option);
                });
                $sel.unbind();
                $sel.on('change', function (e) {
                    var project = JSON.parse($(this).val());
                    userManager.PROJECT = project.project_name;
                    //userManager.requestProject(project.project_name);
                    userManager.getSessions();
                    historyManager.getSessionHistory();
                });
                //console.log(JSON.stringify(data.output[data.output.length - 1]));
                // 가장 최신 프로젝트 자동 선택
                var $options = $sel.find('option');
                if ($options.length > 1) {
                    $options[1].selected = true;
                    $sel.change();
                }
            },
            createProject: function () {
                var reqObj = {
                    username: userManager.USERNAME,
                    project_name: $('input.input-project-name').val(),
                    project_annotation: $('textarea.input-project-note').val()
                };
                $.ajax({
                    url: "createProject.html", method: 'post',
                    data: reqObj,
                    error: userManager.failAjax
                }).done(function (data, status) {
                    if (!data.success) return userManager.failAjax(data, status);
                    console.log('createProject', data, status);
                    if (data.success) {
                        $('#project-modal').modal('hide');
                        $('#content-list > .block').remove();
                        userManager.getProjects(userManager.USERNAME);
                        userManager.logger('Create-Project',reqObj,'Project');
                    }
                    else {
                        $('span.new-project-error-msg').text(data.detail);
                    }
                })
            },
            deleteProject: function (project) {
                var reqObj = {
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT
                };
                $.ajax({
                    url: "deleteProject.html",
                    method: 'post',
                    data: reqObj,
                    error: userManager.failAjax
                }).done(function (data, status) {
                    if (!data.success) return userManager.failAjax(data, status);
                    userManager.getProjects(userManager.USERNAME);
                    userManager.logger('Delete-Project',reqObj,'Project');
                });

            }
        }
    )
})(userManager);
