/**
 * Created by dryji on 2017-02-20.
 */
// TODO 테스트용 임의 코드
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $('#toggle_bar_table').on('change', function (e) {
        $('div.bar-table').toggle();
        $('div.bar-graph').toggle();
    });


    // init process
    userManager.init();
    unitManager.init();
    historyManager.init();
    moduleNetwork.init();

    $(window).scroll(function () {
        //$('.sidebar').animate({top: $(window).scrollTop() + "px"}, {queue: false, duration: 50});
        //$('div.history').animate({top: $(window).scrollTop() + "px"}, {queue: false, duration: 50});
    });
    $('#login-modal').modal({
        backdrop: 'static',
        keyboard: false,
        show: true
    });
    $('.dropdown-menu').on('click', function (e) {
        e.stopPropagation();
    });
    $('.sidebar .form-control').click(function (e) {
        e.stopPropagation()
    });
    $('.btn-slider').on('click',sliderToggle);
    // slider
    $('.btn-toggle-slider').on('click', function (e) {
        var $t = $('#action_history_table');
       // if ($t.hasClass('dataTable')) $t.dataTable().fnAdjustColumnSizing();
    });

});
function refreshTooltip() {
    var tooltip = 'test';
    $('.annotation > li').tooltip({
        content: function (i, x) {
            console.log(i, x);
            return $('<span class="badge">test</span>');
        }
    });
}

function htmlbodyHeightUpdate() {
    var height3 = $(window).height();
    var height1 = $('.nav').height() + 50;
    height2 = $('div.main').height();
    if (height2 > height3) {
        $('html').height(Math.max(height1, height3, height2) + 10);
        $('body').height(Math.max(height1, height3, height2) + 10);
    } else {
        $('html').height(Math.max(height1, height3, height2));
        $('body').height(Math.max(height1, height3, height2));
    }

}

var test;
