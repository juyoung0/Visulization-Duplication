/**
 * Created by dryji on 2017-02-20.
 * handle user session,
 * showSession would load whole units in the session
 * saveSession need to check applied units.
 */
(function (parent) {
    this.PCPnum = 0;
    this.SCMnum = 0;
    this.SPnum = 0;
    _.extend(parent,
        {
            getSessions: function () {
                var reqObj = {username: userManager.USERNAME, project_name: userManager.PROJECT};
                return $.ajax({
                    url: "getSession.html",
                    method: "POST",
                    data: reqObj,
                    success: function (data, status) {
                        if (!data.success) return userManager.failAjax(data, status);
                        userManager.successGetSessions(data, status);
                    },
                    error: userManager.failAjax
                });
            },
            newSession: function () {
                var reqObj = {
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT,
                    session_name: $('input.input-session-name').val(),
                    session_annotation: $('input.input-session-note').val()
                };
                return $.ajax({
                    url: "newSession.html",
                    method: "POST",
                    data: reqObj,
                    success: function (data, status) {
                        if (!data.success) return userManager.failAjax(data, status);
                        userManager.logger('Create-Session', reqObj, 'Session');
                        userManager.successNewSession(data, status)
                    },
                    error: userManager.failAjax
                });
            },
            editSession: function () {
                var reqObj = {
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT,
                    session_name: $('input.input-session-name').val(),
                    session_annotation: $('input.input-session-note').val()
                };
                return $.ajax({
                    url: "newSession.html",
                    method: "POST",
                    data: reqObj,
                    success: function (data, error) {
                        if (!data.success) return userManager.failAjax(data, status);
                        userManager.logger('Change-Session-Annotation', reqObj, 'Session');
                        userManager.successNewSession(data, error);
                    },
                    error: userManager.failAjax
                });
            },
            successNewSession: function () {
                userManager.getSessions().done(function (data) {
                    if (data.success) {
                        console.log(data);
                        $('#session-modal').modal('hide');
                        $('#content-list > .block').remove();
                        userManager.getSessions();
                        historyManager.getSessionHistory();
                    }
                    else {
                        $('span.new-session-error-msg').text(data.detail);
                    }
                });
            },
            confirmDelSession: function () {
                var reqObj = {
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT,
                    session_name: userManager.SESSION,
                    session_ver : userManager.SESSION_VER
                };
                return $.ajax({
                    url: "delSession.html",
                    method: "POST",
                    data: reqObj,
                    success: function (data, status) {
                        if (!data.success) return userManager.failAjax(data, status);
                        userManager.logger('Delete-Session', reqObj, 'Session');
                        userManager.successDelSession(data, status);
                    },
                    error: userManager.failAjax
                });
            },
            delSession: function () {
                $('#delete-session-modal').modal('show');
            },
            successDelSession: function (data) {
                if (!data.success) {
                    return userManager.failAjax(data);
                }
                userManager.getSessions();
                historyManager.getSessionHistory();
            },
            btnBranchSession: function () {
                $('span.session-modal-title').text('Branch');
                $('input.input-session-name').val('').prop('readonly',false);
                $('textarea.input-session-note').val('');
                $('button.btn-branch-session').show();
                $('button.btn-create-session').hide();
                $("button.btn-edit-done-session").hide();
                $('#session-modal').modal('show');
            },
            branchSession: function (session_name, reqObj) {
                console.log('branchSession', session_name);
                if (reqObj ==null) {
                    reqObj = {
                        username: userManager.USERNAME,
                        project_name: userManager.PROJECT,
                        session_name: session_name,
                        parent_session_name: userManager.SESSION,
                        parent_session_ver: userManager.SESSION_VER
                    };
                }else {
                    ///case sankey mode
                    reqObj.session_name = session_name;
                    // turn off sankey mode;
                    $('#session-modal').removeClass('mode-sankey');
                }
                return $.ajax({
                    url: "branchSession.html",
                    method: 'post',
                    success: function (data, status) {
                        if (!data.success) return userManager.failAjax(data, status);
                        userManager.logger('Branch-Session', reqObj, 'Session');
                        userManager.successBranchSession(data, status);
                        historyManager.getSessionHistory();

                    },
                    error: userManager.failAjax,
                    data: reqObj
                });
            },
            successBranchSession: function (data, status) {
                if (!data.success) return userManager.failAjax(data, status);
                userManager.getSessions();
                $('#session-modal').modal('hide');
                alert('The session is branched.');
            },
            successGetSessions: function (data, status, xhr) {
                //console.log('successGetSessions', data);
                var $sel = $("select.session-list");
                $sel.empty();
                $sel.append($('<option selected disabled>Select your session.</option>'));
                _.forEach(data.output, function (item, idx) {
                    var $option = $('<option></option>');
                    //console.log(item.lastEdited, item['session_name']);
                    $option.text(item.lastEdited + ", " + item['session_name'] + " - Ver. " + item['session_ver']);
                    $option.val(JSON.stringify(item));
                    $option.attr('title',item.session_annotation);
                    $sel.append($option);
                });
                $sel.unbind();
                $sel.on('change', function (e) {
                    var session = JSON.parse($(this).val());
                    userManager.SESSION = session.session_name;
                    userManager.SESSION_VER = session.session_ver;
                    userManager.showSession(session.session_name, session.session_ver);
                });
                //console.log(JSON.stringify(data.output[data.output.length - 1]));
                // 가장 최신 세션을 자동 선택
                var $options = $sel.find('option');
                if ($options.length > 1) {
                    $options[1].selected = true;
                    $sel.change();
                }
            },
            showSession: function (session_name, session_ver) {
                console.log('request session', userManager.SESSION);
                var reqObj = {
                    username: userManager.USERNAME,
                    session_name: session_name,
                    session_ver: session_ver,
                    project_name: userManager.PROJECT
                };
                if (!session_name && !session_ver) {
                    session_name = userManager.SESSION;
                    session_ver = userManager.SESSION_VER;
                }
                return $.ajax({
                    url: 'getBlocks.html',
                    method: 'POST',
                    data: reqObj,
                    error: userManager.failAjax,
                    success: function (data, status) {
                        //if (data.success) userManager.logger('Show-Session', reqObj, 'Session');
                        userManager.successShowSession(data, status)
                    }
                });
            },
            successShowSession: function (data, restore) {
                 PCPnum = 0;
                 SCMnum = 0;
                 SPnum = 0;
                if (!data.success) return userManager.failAjax(data);
                $('#content-list > .block').remove();
                console.log("show-session" + userManager.SESSION);
                userManager.logger("Show-Session",{
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER
                });
                _.forEach(_.reverse(data.output), function (item, idx) {
                    //console.log(item);
                    unit_path = "";
                    if (item.heatmap_path != null) {
                        unit_path = item.heatmap_path;
                    }else if (item.pcp_path != null){
                        unit_path = item.pcp_path;
                    }else if (item.scm_path != null){
                        unit_path = item.scm_path;
                    } else if (item.sp_path != null) {
                        unit_path = item.sp_path;
                    }
                    $.ajax({url: unit_path, method: 'post'}).done(function (data) {
                        if (!data.request) return;
                        //if (!data.success) return userManager.failAjax(data, status);
                        // TODO 수정 경로 서버
                        var d = unitManager.transData(data);
                        d.res.annotation_path = item.annotation_path;
                        var $unit = unitManager.addUnit(d);
                        unitManager.locateUnit($unit,$unit.data().position);
                    })
                });
            },
            saveSession: function (units) {
                var sessionObj = {
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    project_name: userManager.PROJECT,
                    block_list: JSON.stringify(units)
                };
                console.log(sessionObj);
                $.post("saveSession.html", sessionObj, function (data, status) {
                    if (!data.success) return userManager.failAjax(data, status);
                    userManager.logger('Save-Session', sessionObj, 'Session');
                    alert(data.detail);
                    userManager.getSessions();
                    historyManager.getSessionHistory();
                });
            }
        }
    );
})(userManager);
