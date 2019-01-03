/**
 * Created by dryji on 2017-02-20.
 */
var userManager = {
    USERNAME: '',
    SESSION: '',
    SESSION_VER: '',
    init: function () {
        //var csrftoken = userManager.getCookie('csrftoken');
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!userManager.testCSRF(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $('button.btn-sign-in').on('click', function (e) {
            //$('div.logged-out').toggle();
            //$('div.logged-in').toggle();
            // Chunggi Lee Implementation
            var $username = $('#usrname').val();
            var $password = $('#psw').val();
            var reqObj = {
                username: $username,
                password: $password
            };
            userManager.login(reqObj);
        });

        // slider menu

        //// slider menu ends

        $('.btn-log-out').on('click', function (e) {
            userManager.logout();
        });
        $('.btn-new-session').on('click', function (e) {
            $('span.session-modal-title').text('Create');
            $('input.input-session-name').val('').attr('readonly', false);
            $('textarea.input-session-note').val('');
            $('button.btn-branch-session').hide();
            $('button.btn-edit-done-session').hide();
            $('button.btn-create-session').show();
            $('#session-modal').modal('show');
        });
        $('.btn-edit-session').on('click', function (e) {
            var ss = $('.session-list :selected');
            $('span.session-modal-title').text('Edit Annotation of ');
            $('input.input-session-name').val(ss.text()).attr('readonly', true);
            $('textarea.input-session-note').val(JSON.parse(ss.val()).session_annotation);
            $('button.btn-branch-session').hide();
            $('button.btn-create-session').hide();
            $('button.btn-edit-done-session').show();
            $('#session-modal').modal('show');
        });
        // <-- Project
        $('.btn-new-project').on('click', function (e) {
            $('input.input-project-name').val('');
            $('textarea.input-project-note').val('');
            $('#project-modal').modal('show');
        });

        $('button.btn-create-project').on('click', function (e) {
            userManager.createProject();
        });
        $('.btn-del-project').on('click', function (e) {
            $('span.del-project-id').text(userManager.PROJECT);
            $('#delete-project-modal').modal('show');
        });
        $('button.btn-del-project').on('click', function (e) {
            userManager.deleteProject(userManager.PROJECT);
        });

        $('#project-modal').on('shown.bs.modal', function () {
            $('input.input-project-name').focus();
        });

        // Project -->

        // <--Session
        $('i.btn-save-session').on('click', function (e) {
            $units = $('.preview-unit');
            $l = $('#save-preview-unit-list');
            if ($units.length != 0) {
                $l.empty();
                _.forEach($units, function ($unit) {
                    console.log($unit);
                    $unit = $($unit);
                    var $o = $('<option></option>');
                    $o.text($unit.data().req.block_name);
                    $o.val($unit.data().req.block_iden);
                    $l.append($o);
                });
                $('#save-preview-unit-list').selectpicker('refresh');
                $('#save-session-modal').modal('show');
            }
            else {
                userManager.saveSession([]);
            }
        });
        $('button.btn-save-preview-session').on('click', function (e) {
            userManager.saveSession($('#save-preview-unit-list').val());
            $('#save-session-modal').modal('hide');
        });
        $('i.btn-branch-session').on('click', function (e) {
                userManager.btnBranchSession();
        });
        $('button.btn-create-session').on('click', function (e) {
            console.log('button.btn-create-session', 'test');
            userManager.newSession();
        });
        $('button.btn-branch-session').on('click', function (e) {
            var session_name = $('input.input-session-name').val();
            console.log('btn-branch-session', session_name);
            if ($('#session-modal').hasClass('mode-sankey')){
                userManager.branchSession(session_name,historyManager.SESSION);
            }
            else {
                userManager.branchSession(session_name);
            }
        });
        $('button.btn-edit-done-session').on('click', function (e) {
            userManager.editSession();
        });
        $('#session-modal').on('shown.bs.modal', function () {
            $('input.input-session-name').focus();
        });
        $('.btn-del-session').on('click', function (e) {
            userManager.delSession();
        });
        $('button.btn-del-session').on('click', function (e) {
            userManager.confirmDelSession();
        });
        // Session-->
        $('sidebar-slider').on('click', function (e) {
            console.log('test');
        })
    },
    failAjax: function (xhr, status, error) {
        alert('xhr error');
        console.log(xhr, error);
    },
    logger: function (action, reqObj, SCOPE) {
        if (SCOPE== null) SCOPE = 'user';
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
};