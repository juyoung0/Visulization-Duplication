/**
 * Created by dryji on 2017-02-20.
 * Project & Session history tree, Action log table
 */
(function (parent) {
    console.log('historyTable.js loaded');
    _.extend(parent,
        {
            transformHistroyTimestamp: function (timestamp) {
                //var unit = ['s','m', 'h','D','W','M','Y'];
                var current = new Date();
                var target = new Date(timestamp);
                var difference = current - target;
                var years = Math.floor(difference / 36e5 / 365),
                    months = Math.floor(difference / 36e5 / 24 / 30),
                    weeks = Math.floor(difference / 36e5 / 24 / 7),
                    days = Math.floor(difference / 36e5 / 24),
                    hours = Math.floor(difference / 36e5),
                    minutes = Math.floor(difference % 36e5 / 60000),
                    seconds = Math.floor(difference % 60000 / 1000);
                if (difference < 60000) return seconds + 's';
                if (difference < 36e5) return minutes + 'm';
                if (difference < 36e5 * 24) return hours + 'h';
                if (difference < 36e5 * 24 * 7) return days + 'D';
                if (difference < 36e5 * 24 * 7 * 30) return weeks + 'W';
                if (difference < 36e5 * 24 * 7 * 365) return months + 'M';
                return years + 'Y';
            },
            createActionHistoryTable: function (data) {
                //if (!data.success) return userManager.failAjax(data, status);
                $('.history-table-container').empty();
                var table = $('<table id="action_history_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody></tbody></thead></table>');
                var parsedData = _.map(data.output, function (item, idx) {
                    switch (item.action) {
                        default:
                            item.param_label = _.map(item.parameter, function (value, key) {
                                return value;
                            }).join(" ");
                            break;
                        case ("Change-Data"):
                            item.param_label = item.parameter.data_name;
                            break;
                        case ("Locate-Unit"):
                            item.param_label = _.map(item.parameter, function (val, key) {
                                return key + ": " + val;
                            }).join(", ");
                            break;
                    }
                    return item;
                });
                var thead = table.find('thead');
                var tr = $('<tr>');
              //  var header = ["#", "DATE", "SCOPE", "ACTION", "DETAIL"];
                var header = ["#", "UNIT", "ACTION", "DETAIL"];
                _.forEach(header, function (item, idx) {
                    var th = $('<th>').text(item);
                    tr.append(th);
                });
                thead.append(tr);
                var tbody = table.find('tbody');
                _.forEach(parsedData, function (item, idx) {
                    var tr = $('<tr>');
                    //var check_td = $('<td><input name="check-action" class="checkbox" type="checkbox" value="' + item.action_id + '"></td>');
                    var check_td = $('<td></td>');
                    var date_td = $('<td></td>').text(visualizer.transformHistroyTimestamp(item.date)).attr('title', item.date);
                   // var scope_td = $('<td></td>').text(item.scope);
                    var scope_td = $('<td></td>');
                    var action_td = $('<td></td>').text(item.action);
                    var column = ["name", "brand", "economy (mpg)", "cylinders", "displacement (cc)", "power (hp)", "weight (lb)", "0-60 mph (s)", "year"];
                    var range_list = [[0,0],[0,0],[46.6,9],[8,3],[455,68],[230,46],[5140,1613],[24.8,8],[1982,1970]];
                    var companyName = ["AMC","Audi","BMW","Buick","Cadillac","Chevrolet","Chevy","Chrysler","Citroen","Datsun","Dodge","Fiat","Ford","Hi","Honda","Mazda","Mercedes-Benz","Mercury","Nissan","Oldsmobile","Opel","Peugeot","Plymouth","Pontiac","Renault","Saab","Subaru","Toyota","Triumph","Volkswagen","Volvo"];
                    var carName = ['AMC Ambassador Brougham', 'AMC Ambassador DPL', 'AMC Ambassador SST', 'AMC Concord DL 6', 'AMC Concord DL', 'AMC Concord DL', 'AMC Concord', 'AMC Concord', 'AMC Gremlin', 'AMC Gremlin', 'AMC Gremlin', 'AMC Gremlin', 'AMC Hornet Sportabout (Wagon)', 'AMC Hornet', 'AMC Hornet', 'AMC Hornet', 'AMC Hornet', 'AMC Matador (Wagon)', 'AMC Matador (Wagon)', 'AMC Matador', 'AMC Matador', 'AMC Matador', 'AMC Matador', 'AMC Matador', 'AMC Pacer D/L', 'AMC Pacer', 'AMC Rebel SST (Wagon)', 'AMC Rebel SST', 'AMC Spirit DL', 'Audi 100 LS', 'Audi 100 LS', 'Audi 100 LS', 'Audi 4000', 'Audi 5000', 'Audi 5000S (Diesel)', 'Audi Fox', 'BMW 2002', 'BMW 320i', 'Buick Century 350', 'Buick Century Limited', 'Buick Century Luxus (Wagon)', 'Buick Century Special', 'Buick Century', 'Buick Century', 'Buick Electra 225 Custom', 'Buick Estate Wagon (Wagon)', 'Buick Estate Wagon (Wagon)', 'Buick Lesabre Custom', 'Buick Opel Isuzu Deluxe', 'Buick Regal Sport Coupe (Turbo)', 'Buick Skyhawk', 'Buick Skylark 320', 'Buick Skylark Limited', 'Buick Skylark', 'Buick Skylark', 'Cadillac Eldorado', 'Cadillac Seville', 'Chevrolet Chevelle Malibu', 'Chevrolet Bel Air', 'Chevrolet Camaro', 'Chevrolet Caprice Classic', 'Chevrolet Caprice Classic', 'Chevrolet Caprice Classic', 'Chevrolet Cavalier 2-Door', 'Chevrolet Cavalier Wagon', 'Chevrolet Cavalier', 'Chevrolet Chevelle Concours (Wagon)', 'Chevrolet Chevelle Concours (Wagon)', 'Chevrolet Chevelle Malibu Classic', 'Chevrolet Chevelle Malibu Classic', 'Chevrolet Chevelle Malibu', 'Chevrolet Chevelle Malibu', 'Chevrolet Chevette', 'Chevrolet Chevette', 'Chevrolet Chevette', 'Chevrolet Chevette', 'Chevrolet Citation', 'Chevrolet Citation', 'Chevrolet Citation', 'Chevrolet Concours', 'Chevrolet Impala', 'Chevrolet Impala', 'Chevrolet Impala', 'Chevrolet Impala', 'Chevrolet Malibu Classic (Wagon)', 'Chevrolet Malibu', 'Chevrolet Malibu', 'Chevrolet Monte Carlo Landau', 'Chevrolet Monte Carlo Landau', 'Chevrolet Monte Carlo S', 'Chevrolet Monte Carlo', 'Chevrolet Monza 2+2', 'Chevrolet Nova Custom', 'Chevrolet Nova', 'Chevrolet Nova', 'Chevrolet Nova', 'Chevrolet Vega (Wagon)', 'Chevrolet Vega 2300', 'Chevrolet Vega', 'Chevrolet Vega', 'Chevrolet Vega', 'Chevrolet Woody', 'Chevy C10', 'Chevy C20', 'Chevy S-10', 'Chrysler Cordoba', 'Chrysler Lebaron Medallion', 'Chrysler Lebaron Salon', 'Chrysler Lebaron Town & Country (Wagon)', 'Chrysler New Yorker Brougham', 'Chrysler Newport Royal', 'Citroen DS-21 Pallas', 'Datsun 1200', 'Datsun 200SX', 'Datsun 200SX', 'Datsun 210', 'Datsun 210', 'Datsun 210', 'Datsun 280ZX', 'Datsun 310 GX', 'Datsun 310', 'Datsun 510 (Wagon)', 'Datsun 510 Hatchback', 'Datsun 510', 'Datsun 610', 'Datsun 710', 'Datsun 710', 'Datsun 810 Maxima', 'Datsun 810', 'Datsun B-210', 'Datsun B210 GX', 'Datsun B210', 'Datsun F-10 Hatchback', 'Datsun PL510', 'Datsun PL510', 'Dodge Aries SE', 'Dodge Aries Wagon (Wagon)', 'Dodge Aspen 6', 'Dodge Aspen SE', 'Dodge Aspen', 'Dodge Aspen', 'Dodge Challenger SE', 'Dodge Charger 2.2', 'Dodge Colt (Wagon)', 'Dodge Colt Hardtop', 'Dodge Colt Hatchback Custom', 'Dodge Colt M/M', 'Dodge Colt', 'Dodge Colt', 'Dodge Colt', 'Dodge Coronet Brougham', 'Dodge Coronet Custom (Wagon)', 'Dodge Coronet Custom', 'Dodge D100', 'Dodge D200', 'Dodge Dart Custom', 'Dodge Diplomat', 'Dodge Magnum XE', 'Dodge Monaco (Wagon)', 'Dodge Monaco Brougham', 'Dodge Omni', 'Dodge Rampage', 'Dodge St. Regis', 'Fiat 124 Sport Coupe', 'Fiat 124 TC', 'Fiat 124B', 'Fiat 128', 'Fiat 128', 'Fiat 131', 'Fiat Strada Custom', 'Fiat X1.9', 'Ford Capri II', 'Ford Country Squire (Wagon)', 'Ford Country Squire (Wagon)', 'Ford Country', 'Ford Escort 2H', 'Ford Escort 4W', 'Ford F108', 'Ford F250', 'Ford Fairmont (Auto)', 'Ford Fairmont (Man)', 'Ford Fairmont 4', 'Ford Fairmont Futura', 'Ford Fairmont', 'Ford Fiesta', 'Ford Futura', 'Ford Galaxie 500', 'Ford Galaxie 500', 'Ford Galaxie 500', 'Ford Gran Torino (Wagon)', 'Ford Gran Torino (Wagon)', 'Ford Gran Torino', 'Ford Gran Torino', 'Ford Gran Torino', 'Ford Granada Ghia', 'Ford Granada GL', 'Ford Granada L', 'Ford Granada', 'Ford LTD Landau', 'Ford LTD', 'Ford LTD', 'Ford Maverick', 'Ford Maverick', 'Ford Maverick', 'Ford Maverick', 'Ford Maverick', 'Ford Mustang Boss 302', 'Ford Mustang Cobra', 'Ford Mustang GL', 'Ford Mustang II 2+2', 'Ford Mustang II', 'Ford Mustang', 'Ford Pinto (Wagon)', 'Ford Pinto Runabout', 'Ford Pinto', 'Ford Pinto', 'Ford Pinto', 'Ford Pinto', 'Ford Pinto', 'Ford Pinto', 'Ford Ranger', 'Ford Thunderbird', 'Ford Torino (Wagon)', 'Ford Torino 500', 'Ford Torino', 'Hi 1200D', 'Honda Accord CVCC', 'Honda Accord LX', 'Honda Accord', 'Honda Accord', 'Honda Civic (Auto)', 'Honda Civic 1300', 'Honda Civic 1500 GL', 'Honda Civic CVCC', 'Honda Civic CVCC', 'Honda Civic', 'Honda Civic', 'Honda Civic', 'Honda Prelude', 'Mazda GLC Deluxe', 'Mazda RX-3', 'Mazda 626', 'Mazda 626', 'Mazda GLC 4', 'Mazda GLC Custom L', 'Mazda GLC Custom', 'Mazda GLC Deluxe', 'Mazda GLC', 'Mazda RX-2 Coupe', 'Mazda RX-4', 'Mazda RX-7 Gs', 'Mercedes-Benz 240D', 'Mercedes-Benz 280S', 'Mercedes-Benz 300D', 'Mercury Capri 2000', 'Mercury Capri V6', 'Mercury Cougar Brougham', 'Mercury Grand Marquis', 'Mercury Lynx L', 'Mercury Marquis Brougham', 'Mercury Marquis', 'Mercury Monarch Ghia', 'Mercury Monarch', 'Mercury Zephyr 6', 'Mercury Zephyr', 'Nissan Stanza XE', 'Oldsmobile Cutlass Ciera (Diesel)', 'Oldsmobile Cutlass LS', 'Oldsmobile Cutlass Salon Brougham', 'Oldsmobile Cutlass Salon Brougham', 'Oldsmobile Cutlass Supreme', 'Oldsmobile Delta 88 Royale', 'Oldsmobile Omega Brougham', 'Oldsmobile Omega', 'Oldsmobile Starfire SX', 'Oldsmobile Vista Cruiser', 'Opel 1900', 'Opel 1900', 'Opel Manta', 'Opel Manta', 'Peugeot 304', 'Peugeot 504 (Wagon)', 'Peugeot 504', 'Peugeot 504', 'Peugeot 504', 'Peugeot 504', 'Peugeot 505S Turbo Diesel', 'Peugeot 604SL', 'Plymouth Arrow GS', 'Plymouth Barracuda 340', 'Plymouth Champ', 'Plymouth Cricket', 'Plymouth Custom Suburb', 'Plymouth Duster', 'Plymouth Duster', 'Plymouth Duster', 'Plymouth Fury Gran Sedan', 'Plymouth Fury III', 'Plymouth Fury III', 'Plymouth Fury III', 'Plymouth Fury', 'Plymouth Grand Fury', 'Plymouth Horizon 4', 'Plymouth Horizon Miser', 'Plymouth Horizon TC3', 'Plymouth Horizon', 'Plymouth Reliant', 'Plymouth Reliant', 'Plymouth Sapporo', 'Plymouth Satellite (Wagon)', 'Plymouth Satellite Custom (Wagon)', 'Plymouth Satellite Custom', 'Plymouth Satellite Sebring', 'Plymouth Satellite', 'Plymouth Valiant Custom', 'Plymouth Valiant', 'Plymouth Valiant', 'Plymouth Volare Custom', 'Plymouth Volare Premier V8', 'Plymouth Volare', 'Pontiac Astro', 'Pontiac Catalina Brougham', 'Pontiac Catalina', 'Pontiac Catalina', 'Pontiac Catalina', 'Pontiac Firebird', 'Pontiac Grand Prix Lj', 'Pontiac Grand Prix', 'Pontiac J2000 Se Hatchback', 'Pontiac Lemans V6', 'Pontiac Phoenix LJ', 'Pontiac Phoenix', 'Pontiac Phoenix', 'Pontiac Safari (Wagon)', 'Pontiac Sunbird Coupe', 'Pontiac Ventura Sj', 'Renault 12 (Wagon)', 'Renault 12TL', 'Renault 18I', 'Renault 5 Gtl', 'Renault Lecar Deluxe', 'Saab 900S', 'Saab 99E', 'Saab 99GLE', 'Saab 99LE', 'Saab 99LE', 'Subaru DL', 'Subaru DL', 'Subaru', 'Subaru', 'Toyota Carina', 'Toyota Celica GT Liftback', 'Toyota Celica GT', 'Toyota Corolla 1200', 'Toyota Corolla 1200', 'Toyota Corolla 1600 (Wagon)', 'Toyota Corolla Liftback', 'Toyota Corolla Tercel', 'Toyota Corolla', 'Toyota Corolla', 'Toyota Corolla', 'Toyota Corolla', 'Toyota Corolla', 'Toyota Corona Hardtop', 'Toyota Corona Liftback', 'Toyota Corona Mark II', 'Toyota Corona', 'Toyota Corona', 'Toyota Corona', 'Toyota Corona', 'Toyota Cressida', 'Toyota Mark II', 'Toyota Mark II', 'Toyota Starlet', 'Toyota Tercel', 'Toyota Corona Mark II (Wagon)', 'Triumph TR7 Coupe', 'Volkswagen Rabbit', 'Volkswagen 1131 Deluxe Sedan', 'Volkswagen 411 (Wagon)', 'Volkswagen Dasher (Diesel)', 'Volkswagen Dasher', 'Volkswagen Dasher', 'Volkswagen Dasher', 'Volkswagen Jetta', 'Volkswagen Model 111', 'Volkswagen Pickup', 'Volkswagen Rabbit C (Diesel)', 'Volkswagen Rabbit Custom Diesel', 'Volkswagen Rabbit Custom', 'Volkswagen Rabbit Custom', 'Volkswagen Rabbit L', 'Volkswagen Rabbit', 'Volkswagen Rabbit', 'Volkswagen Rabbit', 'Volkswagen Rabbit', 'Volkswagen Scirocco', 'Volkswagen Super Beetle 117', 'Volkswagen Super Beetle', 'Volkswagen Type 3', 'Volvo 144EA', 'Volvo 145E (Wagon)', 'Volvo 244DL', 'Volvo 245', 'Volvo 264GL', 'Volvo Diesel'];
                    var companyLoc = [0.0, 15.67, 31.33, 47.0, 62.67, 78.33, 94.0, 109.67, 125.33, 141.0, 156.67, 172.33, 188.0, 203.67, 219.33, 235.0, 250.67, 266.33, 282.0, 297.67, 313.33, 329.0, 344.67, 360.33, 376.0, 391.67, 407.33, 423.0, 438.67, 454.33, 470.0];
                    var columnText = ["name","cylinders","weight(lb)","year"];

                    console.log(item);
                    var details;
                    if(item.action=="Brush-PCP-Axis") {

                        var order = JSON.parse(item.parameter.brushed_axis);
                        var brush = JSON.parse(item.parameter.brushed_range);
                        var name = [];
                        var range = [0,0];
                        var detail = [];
                        scope_td = $('<td></td>').text(item.parameter.block_name );
                        for(var j=0; j<column.length; j++){
                            if(order[j] == 1) {
                                if (j==0){
                                    var company_list = [];

                                    companyName.forEach(function(n, i){
                                        if (companyLoc[i] >= brush[0][0] & companyLoc[i] <= brush[0][1])
                                            company_list.push(n);
                                    });

                                    detail.push("Axis : " + column[j+1] + ", Name : " + company_list + "\n");

                                }
                                else {
                                    range[0] = (range_list[j+1][0] - range_list[j+1][1]) * (470-brush[j][0]) / 470 + range_list[j+1][1];
                                    range[1] = (range_list[j+1][0] - range_list[j+1][1]) * (470-brush[j][1]) / 470 + range_list[j+1][1];
                                    detail.push("Axis : " + column[j+1] + ", Range : " + parseInt(range[1]) + "~" + parseInt(range[0]) + "\n");

                                }
                            }
                        }
                        details = detail;
                    } else if(item.action=="Change-PCP-Column") {
                        scope_td = $('<td></td>').text(item.parameter.block_name );
                        var order = JSON.parse(item.parameter.column_order);
                        var cols = [];
                        order.forEach(function(n,i){
                            cols.push(column[parseInt(n)]);
                        })
                        details = cols;
                    } else if(item.action=="Brush-SCM-Axis"){
                        scope_td = $('<td></td>').text(item.parameter.block_name );
                        var order = JSON.parse(item.parameter.brushed_axis);
                        var brush = JSON.parse(item.parameter.brushed_range);
                        var name = [];
                        var range = [[],[]];
                        for(var i=0; i<2; i++)
                            name.push(column[order[i]+2]);

                        range[0].push((range_list[order[0]+2][0]-range_list[order[0]+2][1]) * brush[0][0] / 136 + range_list[order[0]+2][1]);
                        range[0].push((range_list[order[0]+2][0]-range_list[order[0]+2][1]) * brush[1][0] / 136 + range_list[order[0]+2][1]);
                        range[1].push((range_list[order[1]+2][0]-range_list[order[1]+2][1]) * brush[1][1] / 136 + range_list[order[1]+2][1]);
                        range[1].push((range_list[order[1]+2][0]-range_list[order[1]+2][1]) * brush[0][1] / 136 + range_list[order[1]+2][1]);

                       details = "X : "+ name[0] +", Range : " + parseInt(range[0][0]) + "~"+parseInt(range[0][1])
                        + "\nY : "+name[1] +", Range : " + parseInt(range[1][1]) + "~"+parseInt(range[1][0]);

                    } else if(item.action=="Brush-SP-Axis"){
                        scope_td = $('<td></td>').text(item.parameter.block_name);
                        var brush = JSON.parse(item.parameter.brushed_range);
                        var x_axis = item.parameter.x_axis;
                        var y_axis = item.parameter.y_axis;
                        var range = [[],[]];
                        var x_idx = column.indexOf(x_axis.toLowerCase());
                        var y_idx = column.indexOf(y_axis.toLowerCase());

                        range[0].push((range_list[x_idx][0]-range_list[x_idx][1]) * brush[0][0] / 960 + range_list[x_idx][1]);
                        range[0].push((range_list[x_idx][0]-range_list[x_idx][1]) * brush[1][0] / 960 + range_list[x_idx][1]);
                        range[1].push((range_list[y_idx][0]-range_list[y_idx][1]) * brush[1][1] / 960 + range_list[y_idx][1]);
                        range[1].push((range_list[y_idx][0]-range_list[y_idx][1]) * brush[0][1] / 960 + range_list[y_idx][1]);

                        details = "X : "+x_axis +", Range : " + parseInt(range[0][0]) + "~"+parseInt(range[0][1])
                            + "\nY : "+ y_axis  +", Range : " + parseInt(range[1][1]) + "~"+parseInt(range[1][0]);
                    } else if(item.action=="Search-Table-Row"){
                        var idx = JSON.parse(item.parameter.selected_index)[0];
                        var carname = carName[idx];
                        details = carname;
                    } else if(item.action=="Create-Unit-Annotation"){
                        scope_td = $('<td></td>').text(item.parameter.block_name);
                        details = item.parameter.answer;
                    } else if(item.action=="Create-Unit" || item.action=="Save-Unit" || item.action=="Pin-Unit" || item.action=="Unpin-Unit"){
                        scope_td = $('<td></td>').text(item.parameter.block_name);
                    } else if(item.action=="Click-Menu-Tab" | item.action=="Click-Sankey-Tab" || item.action=="Click-Table-Tab"){
                        scope_td = $('<td></td>').text(item.parameter.block_name);
                        action_td = item.action;
                    } else if (item.action=="Change_Table_Order"){
                        action_td = item.action;
                       // details = columnText[JSON.parse(item.parameter.column)]
                    } else if (item.action == "Change_Table_Page"){
                        action_td = item.action;
                     //   details = item.parameter.page;
                    }

                    var detail_td = $('<td></td>').text(details);
                    //tr.append(check_td, date_td, scope_td, action_td, detail_td);
                    tr.append(check_td, scope_td, action_td, detail_td);
                    tr.data(item);
                    tbody.append(tr);
                });
                $('.history-table-container').append(table);
             //   $('div.toolbar').html('<div class="btn-group"><button class="btn btn-default btn-undo">Undo</button><button class="btn btn-default btn-redo">Redo</button></div>');
                //_.map($('input[name="check-action"]'),function(item){return $(item).val()})
                var oTable = table.DataTable(
                    {
                        paging: false,
                        //fixedHeader: true,
                        columnnDefs: [{
                            name: "#",
                            title: "#",
                            orderable: false,
                            searchable: false,
                            width: "10%"
                        }, //{title: "DATE", name: "DATE", width: "10%"},
                            {title: "UNIT", name: "UNIT"},
                            {title: "ACTION", name: "ACTION"},
                            {title: "DETAIL", name: "DETAIL"}],
                        scrollY: '30vh',
                        scrollCollapse: true,
                        dom: "ft",
                        ordering: false,
                        autoWidth: true,
                        fixedHeader: true,
                        /*
                         drawCallback: function (settings) {
                         addContext(settings);
                         },
                         */
                        initComplete: function () {
                            var api = this.api();

                            api.columns().indexes().flatten().each(function (i) {
                                if (i == 4 || i == 1) return;
                                var column = api.column(i);
                                if (i == 0) {
                                    var check_all = $('<input type="checkbox" id="check_all_action">');
                                    check_all.on('click', function (e) {
                                        console.log(check_all.prop('checked'));
                                        var x = $('input[name="check-action"]');
                                        if (check_all.prop('checked')) x.prop('checked', true);
                                        else {
                                            x.prop('checked', false);
                                        }
                                    });
                                    check_all.appendTo($(column.header()).empty());
                                    return;
                                }
                                var title = $('#action_history_table thead th').eq(i).text();
                                var select = $('<div class="dropdown"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown"><span class="column-name"></span> <span class="caret"></span></button></div>');
                                select.find('.column-name').text(title);
                                var $ul = $('<ul class="dropdown-menu"></ul>');
                                column.data().unique().sort().each(function (d, j) {
                                    var $item = $('<li><a href="#" class="small" tabIndex="-1"><input name="' + title + '" type="checkbox" value="' + d + '"/>&nbsp;' + d + '</a></li>');
                                    $ul.append($item);
                                });
                                select.append($ul);
                                select.appendTo($(column.header()).empty());
                                // setup dropbox
                                select.find('.dropdown-menu a').on('click', function (event) {
                                    var $target = $(event.currentTarget),
                                        $inp = $target.find('input');
                                    var test = $inp.prop('checked');
                                    test ? $inp.prop('checked', false) : $inp.prop('checked', true);
                                    var checked_items = $('input[name="' + title + '"]:checked');
                                    console.log(checked_items);
                                    var val_list = _.map(checked_items, function (item) {
                                        var value = $(item).val();
                                        console.log(value);
                                        return $.fn.dataTable.util.escapeRegex(value);
                                    });
                                    var val = val_list.join('|');
                                    console.log(val);
                                    column
                                        .search(val ? val : '', true, false)
                                        .draw();
                                    $(event.target).blur();
                                    return false;
                                });
                            });
                            $("div.toolbar").html('<div class="btn-group"><a class="btn btn-xs btn-default btn-undo" href="#" title="Undo"><i class="glyphicon glyphicon-backward"></i></a><a class="btn btn-xs btn-default btn-redo" href="#" title="Redo"><i class="glyphicon glyphicon-forward btn-redo"></i></a></div>');
                            $("div.msgbox").html('<div></div>');
                            $(".dropdown-toggle").dropdown();


                            $('#action_history_table >tbody >tr').on('click', function (e) {
                                var thisTr = $(this);
                                console.log(thisTr.data());
                                var checkbox = thisTr.find('input[name="check-action"]');
                                var checked = checkbox.prop('checked');
                                checked ? checkbox.prop("checked", false) : checkbox.prop("checked", true);
                            });

                            // undo button
                            $('a.btn-undo').on('click', function () {
                                $('div.msgbox').empty();
                                $('#action_history_table >tbody >tr').removeClass('danger');
                                var $success = $('<span class="alert alert-success" style="display:block;margin-bottom: 0px;padding-bottom: 7px;padding-top: 7px;margin-top: 1px; text-align: center "><strong>Success!</strong>Selected actions undone.</span>');
                                var $fail = $('<span class="alert alert-danger" style="display:block;margin-bottom: 0px;padding-bottom: 7px;padding-top: 7px;margin-top: 1px; text-align: center"><strong>Failed!</strong> Can not undo selected actions.</span>');

                                var checked = $('input[name="check-action"]:checked');
                                var checked_rows = checked.parent().parent();
                                var action_list = _.map(checked, function (item) {
                                    return {action_id: $(item).parent().parent().data()['action_id']}
                                });

                                /// dependency check
                                historyManager.checkActionDependent(action_list).done(function (data, status) {
                                    if (!data.success) {
                                        return historyManager.failAjax(data, status);
                                    }

                                    var actions = data.output;

                                    // case Unavailable
                                    if (_.find(actions, {output: "Unavailable"})) {
                                        $('div.msgbox').append($fail);
                                        var unavailable = _.filter(actions, function (action) {
                                            if (action.output == "Unavailable") return action;
                                        });
                                        _.forEach(checked_rows, function (row) {
                                            if (_.find(unavailable, {action_id: $(row).data().action_id}))
                                                $(row).addClass('danger');
                                        });
                                        return;
                                    }
                                    // case Need to select
                                    if (_.find(actions, {output: "Need to Select"})) {
                                        visualizer.setupDependentModal(actions);
                                        $('#history-dependent-modal').modal('show');
                                        return;
                                    }
                                    // case Available
                                    historyManager.undoAction(actions).done(function (data, status) {
                                        if (!data.success) {
                                            return historyManager.failAjax(data, status);
                                        }
                                        checked_rows.addClass('action-undo');
                                        $('div.msgbox').append($success);
                                        checked.prop('checked', false);
                                    });
                                });

                            });

                            // redo button
                            $('a.btn-redo').on('click', function () {
                                var checked = $('input[name="check-action"]:checked');
                                var action_list = _.map(checked, function (item) {
                                    return {action_id: $(item).parent().parent().data()['action_id']};
                                });
                                historyManager.redoAction(action_list).done(function (data, status) {
                                    if (!data.success) return historyManager.failAjax(data,status);
                                    checked.removeClass('action-undo');
                                });
                            });
                            $('#action_history_table').on('draw.dt',function () {
                                $('#action_history_table').dataTable().fnAdjustColumnSizing();
                            });

                            /*
                             var $table = $('table.scroll'),
                             $bodyCells = $table.find('tbody tr:first').children(),
                             colWidth;

                             // Adjust the width of thead cells when window resizes
                             $(window).resize(function() {
                             // Get the tbody columns width array
                             colWidth = $bodyCells.map(function() {
                             return $(this).width();
                             }).get();

                             // Set the width of thead columns
                             $table.find('thead tr').children().each(function(i, v) {
                             $(v).width(colWidth[i]);
                             });
                             }).resize(); // Trigger resize handler
                             */

                        }

                    });
                function addContext(settings) {
                    /*
                    console.log('addContext', settings);
                    $.contextMenu({
                        selector: '.dataTable tbody tr',
                        items: {
                            "undo": {
                                name: "undo", icon: "fa-undo", callback: function (key, options) {
                                    console.log(key, options, this);
                                    $(this).addClass('action-undo');
                                }
                            },
                            "redo": {
                                name: "redo", icon: "fa-repeat", callback: function (key, options) {
                                    console.log(key, options, this);
                                    $(this).removeClass('action-undo');
                                }
                            }
                        }
                    });
                    */
                }
            },
            setupDependentModal: function (data) {

                $('.history-dependent-table-container').empty();
                var table = $('<table id="action_history_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody></tbody></thead></table>');
                var parsedData = _.map(data.output, function (item, idx) {

                    switch (item.action) {

                        default:
                            item.param_label = _.map(item.parameter, function (value, key) {
                                return value;
                            }).join(" ");
                            break;
                        case ("Change-Data"):
                            item.param_label = item.parameter.data_name;
                            break;
                        case ("Locate-Unit"):
                            item.param_label = _.map(item.parameter, function (val, key) {
                                return key + ": " + val;
                            }).join(", ");
                            break;
                        case ("Brush-PCP-Axis"):
                            item.param_label = "brsfsf"
                            break;

                        case ("Change-PCP-Column"):
                            item.param_label = "pcpopopopopop"
                            break;

                        case ("Save-Unit"):
                            item.param_label = item.parameter;
                            break;

                    }
                    return item;
                });
                var thead = table.find('thead');
                var tr = $('<tr>');
                //var header = ["#", "DATE", "SCOPE", "ACTION", "DETAIL"];
                var header = ["UNIT", "ACTION", "DETAIL"];
                _.forEach(header, function (item, idx) {
                    var th = $('<th>').text(item);
                    tr.append(th);
                });
                thead.append(tr);
                var tbody = table.find('tbody');
                console.log(parsedData);
                _.forEach(parsedData, function (item, idx) {
                    var tr = $('<tr>');
                    var check_td = $('<td><input name="check-action" class="checkbox" type="checkbox" value="' + item.action_id + '"></td>');
                    var date_td = $('<td></td>').text(visualizer.transformHistroyTimestamp(item.date)).attr('title', item.date);
                    var scope_td = $('<td></td>').text(item.scope);
                    var action_td = $('<td></td>').text(item.action);

                    var detailtxt;
                    var labels = item.param_label.split(" ");
                    if(item.action == "Save-Unit")
                        detailtxt = labels[0];
                    else if(item.action == "Brush-PCP-Axis")
                        detailtxt = labels[4];
                    else if(item.action == "Change-PCP-Column")
                        detailtxt = labels[3];


                    var detail_td = $('<td></td>').text(item.param_label);

                    tr.append(check_td, date_td, scope_td, action_td, detail_td);
                    tr.data(item);
                    tbody.append(tr);
                });


                $('.history-table-container').append(table);
                $('div.toolbar').html('<div class="btn-group"><button class="btn btn-default btn-undo">Undo</button><button class="btn btn-default btn-redo">Redo</button></div>');
                //_.map($('input[name="check-action"]'),function(item){return $(item).val()})
                var oTable = table.DataTable(
                    {
                        paging: false,
                        //fixedHeader: true,
                        columnnDefs: [{
                            name: "#",
                            title: "#",
                            orderable: false,
                            searchable: false,
                            width: "10%"
                        }, {title: "DATE", name: "DATE", width: "10%"},
                            {title: "SCOPE", name: "SCOPE"},
                            {title: "ACTION", name: "ACTION"},
                            {title: "DETAIL", name: "DETAIL"}],
                        scrollY: '80vh',
                        scrollCollapse: true,
                        dom: "f<'toolbar'><'msgbox'>t",
                        ordering: false,
                        autoWidth: true,
                        fixedHeader: true,
                        /*
                         drawCallback: function (settings) {
                         addContext(settings);
                         },
                         */
                        initComplete: function () {
                            var api = this.api();

                            api.columns().indexes().flatten().each(function (i) {
                                if (i == 4 || i == 1) return;
                                var column = api.column(i);
                                if (i == 0) {
                                    var check_all = $('<input type="checkbox" id="check_all_action">');
                                    check_all.on('click', function (e) {
                                        console.log(check_all.prop('checked'));
                                        var x = $('input[name="check-action"]');
                                        if (check_all.prop('checked')) x.prop('checked', true);
                                        else {
                                            x.prop('checked', false);
                                        }
                                    });
                                    check_all.appendTo($(column.header()).empty());
                                    return;
                                }
                                var title = $('#action_history_table thead th').eq(i).text();
                                var select = $('<div class="dropdown"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown"><span class="column-name"></span> <span class="caret"></span></button></div>');
                                select.find('.column-name').text(title);
                                var $ul = $('<ul class="dropdown-menu"></ul>');
                                column.data().unique().sort().each(function (d, j) {
                                    var $item = $('<li><a href="#" class="small" tabIndex="-1"><input name="' + title + '" type="checkbox" value="' + d + '"/>&nbsp;' + d + '</a></li>');
                                    $ul.append($item);
                                });
                                select.append($ul);
                                select.appendTo($(column.header()).empty());
                                // setup dropbox
                                select.find('.dropdown-menu a').on('click', function (event) {
                                    var $target = $(event.currentTarget),
                                        $inp = $target.find('input');
                                    var test = $inp.prop('checked');
                                    test ? $inp.prop('checked', false) : $inp.prop('checked', true);
                                    var checked_items = $('input[name="' + title + '"]:checked');
                                    console.log(checked_items);
                                    var val_list = _.map(checked_items, function (item) {
                                        var value = $(item).val();
                                        console.log(value);
                                        return $.fn.dataTable.util.escapeRegex(value);
                                    });
                                    var val = val_list.join('|');
                                    console.log(val);
                                    column
                                        .search(val ? val : '', true, false)
                                        .draw();
                                    $(event.target).blur();
                                    return false;
                                });
                            });
                            $("div.toolbar").html('<div class="btn-group"><a class="btn btn-xs btn-default btn-undo" href="#" title="Undo"><i class="glyphicon glyphicon-backward"></i></a><a class="btn btn-xs btn-default btn-redo" href="#" title="Redo"><i class="glyphicon glyphicon-forward btn-redo"></i></a></div>');
                            $("div.msgbox").html('<div></div>');
                            $(".dropdown-toggle").dropdown();

                            $('#action_history_table >tbody >tr').on('click', function (e) {
                                var thisTr = $(this);
                                console.log(thisTr.data());
                                var checkbox = thisTr.find('input[name="check-action"]');
                                var checked = checkbox.prop('checked');
                                checked ? checkbox.prop("checked", false) : checkbox.prop("checked", true);
                            });
                            // undo button
                            $('a.btn-undo').on('click', function () {
                                var $success = $('<a href="#" class="btn btn-sm alert-primary btn-block"><strong>Success!</strong> Undo selected actions.</a>');
                                var $fail = $('<a href="#" class="btn btn-sm alert-danger btn-block"><strong>Unavailable!</strong> Can not undo selected actions.</a>');

                                var checked = $('input[name="check-action"]:checked');
                                var checked_rows = checked.parent().parent();
                                var action_list = _.map(checked, function (item) {
                                    return {action_id: $(item).parent().parent().data()['action_id']}
                                });
                                historyManager.checkActionDependent(action_list).done(function (data, status) {
                                    if (!data.success) {
                                        return historyManager.failAjax(data, status);
                                    }
                                    var actionList = data.output;

                                    // case Unavailable
                                    if (_.find(actionList, {output: "Unavailable"})) {
                                        $('div.msgbox').empty().append($fail);
                                        checked_rows.addClass('danger');
                                        $fail.fadeOut(5000, function () {
                                            $(this).remove();
                                        });
                                        checked_rows.removeClass('danger').fadeIn(5000);
                                        return;
                                    }
                                    if (_.find(actionList, {output: "Need to select"})) {

                                    }
                                    // case
                                    historyManager.undoAction(actionList).done(function (data, status) {
                                        if (!data.success) {
                                            return historyManager.failAjax(data, status);
                                        }
                                        checked_rows.addClass('action-undo');
                                        $('div.msgbox').empty().append($success);
                                        $success.fadeOut(5000, function () {
                                            $(this).remove();
                                        });
                                    });

                                    switch (actionList.output) {
                                        case "Available":

                                            break;
                                        case "Unavailable":

                                            break;
                                        case "Need to select":
                                            visualizer.setupDependentModal(output);
                                            $('#history-dependent-modal').modal('show');
                                            break;
                                    }
                                });

                            });

                            // redo button
                            $('a.btn-redo').on('click', function () {
                                var checked = $('input[name="check-action"]:checked');
                                var action_list = _.map(checked, function (item) {
                                    return {action_id: $(item).parent().parent().data()['action_id']};
                                });
                                historyManager.redoAction(action_list).success(function (data, status) {
                                    checked.removeClass('action-undo');
                                });
                            });

                            $('#action_history_table').dataTable().fnAdjustColumnSizing();
                        }
                    });
            }
        });
})(visualizer);


