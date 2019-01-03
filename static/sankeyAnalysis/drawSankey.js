/**
 * * Created by juyoung on 2017-06-22.
 */
var A=["A8","A9","A11","A12","A13","A14","A15","A18","A19","A20","A21","A22","B26","B28","B29"];
var B=["B4","B12","B13","B14","B15","B18","B19","B20","B30","B32","B33","B34","B39","B43","B44","B16","B17","B21","B22","B23","B24","B27","B31","B35","B38","B40","B41","B42","B45","B46","B47","B48","B49"];
var C=["B4","B12","B13","B14","B15","B18","B19","B20","B30","B32","B33","B34","B39","B43","B44"];
var D=["B16","B17","B21","B22","B23","B24","B27","B31","B35","B38","B40","B41","B42","B45","B46","B47","B48","B49"];
var E=["B21","B23","B24","B45","B46","B22"];
var F=["B16","B17","B27","B31","B35","B38","B40","B41","B42","B47","B48","B49"];

function CreatCard(name) {
    var stringToAdd = ""
    var div = $('.flex-row').append('div').addClass('col-xs-6 col-sm-4 col-lg-3');
    $('col-xs-6 col-sm-4 col-lg-3').append('div').addClass('sankey-history');
    //$('div.append('div').addClass('caption');
    div.append('<p>Test</p>');
}

function SelectGroup(num) {
    $(".flex-row").empty();
    for (var i = 0; i<A.length; i++){
        CreatCard(A[i]);
    }
}