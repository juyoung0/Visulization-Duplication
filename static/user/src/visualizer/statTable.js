/**
 * Created by dryji on 2017-02-20.
 * Bar chart and table for the selected units statistics
 */
(function (parent) {
    var columnTable;
    _.extend(parent,
        {
            createStatTable: function (selectedIndex) {

                $('.stat-table-container').empty();
                var table = $('<table class="selection-table" id="selection-table"></table>');
                $('.stat-table-container').append(table);

                var data = [];

                d3.csv("static/csv/car.csv", function (error, dt) {

                    dt.forEach(function (d, i) {
                        if (selectedIndex.length == 0)
                          //  data.push([d["name"], +d["economy (mpg)"], +d["cylinders"], +d["displacement (cc)"], +d["power (hp)"], +d["weight (lb)"], +d["0-60 mph (s)"], +d["year"] + 1900]);
                            data.push([d["name"], +d["cylinders"],  +d["power (hp)"], +d["weight (lb)"], +d["year"] + 1900]);
                        else {
                            if (selectedIndex.includes(i))
                          //      data.push([d["name"], +d["economy (mpg)"], +d["cylinders"], +d["displacement (cc)"], +d["power (hp)"], +d["weight (lb)"], +d["0-60 mph (s)"], +d["year"] + 1900]);
                            data.push([d["name"], +d["cylinders"],  +d["power (hp)"], +d["weight (lb)"], +d["year"] + 1900]);
                        }
                    });
                    if (error) throw error;

                    var dataTable = $('.selection-table').DataTable({
                        data: data,
                        columns: [
                            {title: 'name'},
                          //  {title: 'economy (mpg)'},
                            {title: 'cylinders'},
                         //   {title: 'displacement (cc)'},
                            {title: 'power (hp)'},
                            {title: 'weight (lb)'},
                        //    {title: '0-60 mph (s)'},
                            {title: 'year'}
                        ],
                        retrieve: false,
                        searching: false
                    });


                    $('.selection-table tbody').on('mouseenter', 'tr', function () {
                        var index = dataTable.row(this).index();
                        if (selectedIndex.length != 0)
                            index = selectedIndex[index];
                        var indexList = [];
                        indexList.push(index);
                        visualizer.unitHighlight(indexList);

                        unitManager.logger('Search-Table-Row', unitManager.getLoggerObj({
                            selected_index: JSON.stringify(indexList)
                        }));

                    }).on('mouseleave', 'tr', function () {
                        visualizer.unitDehighlight();
                    });

                    unitManager.logger('Search-Table', unitManager.getLoggerObj({
                        selected_index: JSON.stringify(selectedIndex)
                    }));

                });

                visualizer.appendLogger();
            },
            appendLogger: function () {
                columnText = [];
                columnText["name"] = 0;
                columnText["cylinders"] = 1;
                columnText["weight(lb)"] = 2;
                columnText["year"] = 3;

                 $('.dataTables_paginate .paginate_button').on('click',  function () {
                    console.log('change page');
                    pagenum = this.innerText;
                    unitManager.logger('Change_Table_Page', {
                        page: pagenum,
                        username: userManager.USERNAME,
                        session_name: userManager.SESSION,
                        session_ver: userManager.SESSION_VER,
                        project_name: userManager.PROJECT
                    });
                });
                $('#selection-table .sorting').on('click',  function () {
                    console.log('change order');

                    unitManager.logger('Change_Table_Order', unitManager.getLoggerObj({
                        column: columnText[this.textContent],
                        username: userManager.USERNAME,
                        session_name: userManager.SESSION,
                        session_ver: userManager.SESSION_VER,
                        project_name: userManager.PROJECT
                    }));
                });
                    /*
                    $('#selection-table .sorting_asc').on('click',  function () {
                        console.log('change order');
                        columnText = this.textContent;
                        unitManager.logger('Change_Table_Order', nitManager.getLoggerObj({
                            column: "Descent " + columnText,
                            username: userManager.USERNAME,
                            session_name: userManager.SESSION,
                            session_ver: userManager.SESSION_VER,
                            project_name: userManager.PROJECT
                        }));
                    });
                    $('#selection-table .solting_desc').on('click',  function () {
                        console.log('change order');
                        columnText = "Ascent " + this.textContent;
                        unitManager.logger('Change_Table_Order', nitManager.getLoggerObj({
                            column: columnText,
                            username: userManager.USERNAME,
                            session_name: userManager.SESSION,
                            session_ver: userManager.SESSION_VER,
                            project_name: userManager.PROJECT
                        }));
                    });
                    */
            }

        })
})(visualizer);
