/**
 * Created by dryji on 2017-02-20.
 */
var historyManager = {
    HISTORY_HEIGHT: 0,
    init: function () {
        var $h = $('.history');
        var $hm = $('.btn-show-history').parent();
        $('.btn-toggle-history').on('click', function (e) {
            var $h = $('.history');
            $h.toggleClass('hide');
            $('.btn-icon-history').toggleClass('active');
            $('#content-list').toggleClass('full-content');
        });
        $('.btn-toggle-history').trigger('click');
        $('.btn-show-unit-menu').on('click', function (e) {
            $h.addClass('hide');
            $hm.removeClass('open');
            $('span.project-name').text(userManager.PROJECT);
            $('span.session-name').text(userManager.SESSION);
            $('span.session-ver').text("VER. " + userManager.SESSION_VER);
            _.forEach($('.block'), function (item, idx) {
                var $b = $(item);
                var p = $b.data().position;
                if (p == null)
                    p = {top: 0};
                $b.css('top', p.top);
            });
            $('.unit-menu').removeClass('hide');
            $('.session-history-menu').addClass('hide');
        })
    },
    clickcancel: function () {
        var event = d3.dispatch('click', 'dblclick');

        function cc(selection) {
            var down,
                tolerance = 5,
                last,
                wait = null;
            // euclidean distance
            function dist(a, b) {
                return Math.sqrt(Math.pow(a[0] - b[0], 2), Math.pow(a[1] - b[1], 2));
            }

            selection.on('mousedown', function () {
                down = d3.mouse(document.body);
                last = +new Date();
            });
            selection.on('mouseup', function () {
                if (dist(down, d3.mouse(document.body)) > tolerance) {

                } else {
                    if (wait) {
                        window.clearTimeout(wait);
                        wait = null;
                        event.dblclick(d3.event);
                    } else {
                        wait = window.setTimeout((function (e) {
                            return function () {
                                event.click(e);
                                wait = null;
                            };
                        })(d3.event), 300);
                    }
                }
            });
        }

        var value = 'foo';
        cc.method = function (_) {
            if (!arguments.length) return value;
            value = _;
            return cc;
        };
        cc.on = function () {
            var value = event.on.apply(cc, arguments);
            return value === event ? cc : value;
        };
        //return d3.rebind(cc, event, 'on');
        return cc;
    },failAjax: function (xhr, status, error) {
        alert('xhr error ' +error);
        console.log(xhr, error);
    }
};