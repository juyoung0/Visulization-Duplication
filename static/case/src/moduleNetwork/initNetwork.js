/**
 * Created by dryji on 2017-03-19.
 */
var moduleNetwork = {
    SPECIECS: [],
    init: function () {
        // get species data
        this.getSpecies();
    },
    logger: function (action, reqObj) {
        var SCOPE = 'unit';
        var reqObj = _.merge({scope: SCOPE, action: action}, reqObj);
        $.ajax({
            url: "insertLog.html",
            method: 'post',
            data: reqObj,
            error: userManager.failAjax
        }).done(function (data, status) {
            console.log(data);
        });
    },failAjax: function (xhr, status, error) {
        alert('xhr error' + xhr);
        console.log('failAjax',xhr, error);
    },
    getSpecies:function () {
        //{"species_list": [{"species": "human"}, {"species": "rat"}, {"species": "mouse"}]}
        $.get('species.html').done(function (data) {
            moduleNetwork.SPECIECS = _.map(data.species_list, function (item) {
                return item.species;
            })
            var $ul = $('.network-species-options');
            var $ula = $('.gesa-species-options');
            _.forEach(moduleNetwork.SPECIECS,function (item) {
                var $li = $('<li class="option-species"><a class="species" href="#"></a></li>');
                var $lia = $('<li class="option-species"><a class="gesa-species" href="#"></a></li>');
                $li.find('a').text(item);
                $lia.find('a').text(item);
                $ul.append($li);
                $ula.append($lia);
            });
        });
    }
};
