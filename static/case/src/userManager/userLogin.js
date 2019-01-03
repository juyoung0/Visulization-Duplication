/**
 * Created by dryji on 2017-02-20.
 * handle user login, logout and CSRF info.
 */
(function(parent){
    _.extend(parent,
        {
            getCookie: function (name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            },
            testCSRF: function (method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            },
            login: function (reqObj) {
                //alert(JSON.stringify(reqObj));
                return $.ajax({
                    url: "login.html",
                    method: 'POST',
                    data: reqObj,
                    error: userManager.failAjax,
                    success: userManager.successLogin
                });
            },
            successLogin: function (data, status, xhr) {
                //console.log(data);
                if (data.success) {
                    $('#login-modal').modal('hide');
                    // $('a.btn-toggle-slider1').trigger('click');
                    $("#table_main").css("height", $(window).height());

                    // 유저 정보 업데이트
                    userManager.USERNAME = data.output[0].username;
                    if (data.output[0].lastEdited != null) {
                        userManager.SESSION = data.output[0].session_name;
                        userManager.SESSION_VER = data.output[0].session_ver;
                        userManager.PROJECT = data.output[0].project_name;
                    }
                    $('span.username').text(" " + userManager.USERNAME.toUpperCase());
                    userManager.getProjects(data.output[0].username);
                    $('.btn-show-history').trigger('click');
                    //visualizer.createTaperedNetworkGraph();
                    /*
                    d3.json('static/json/network.json', function (data) {
                        function getRandomInt(min, max) {
                            return Math.floor(Math.random() * (max - min + 1)) + min;
                        }
                        var $svg = $('#right_main');
                        var h =$svg.height();
                        var w = $svg.width();
                        _.forEach(data.nodes,function (item) {
                            item.x = getRandomInt(0,w);
                            item.y = getRandomInt(0,h);
                        });
                        visualizer.createPPINetworkGraph(data,'network-edge');
                    });
                    */
                    // $('.btn-show-history').trigger('click');
                }
                else {
                    $('span.log-in').text(data.detail);
                }
            },
            logout: function () {
                $.ajax({
                    url: "logout.html",
                    success: function (data, status, xhr) {
                        window.location.replace("");
                    }
                });
            }
        }
    )
})(userManager);

