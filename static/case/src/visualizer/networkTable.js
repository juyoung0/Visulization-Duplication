/**
 * Created by dryji on 2017-03-08.
 */
(function (parent) {
    _.extend(parent,
        {
            createNetworkTable: function (data, status) {
                //if (!data.success) return moduleNetwork.failAjax(data, status);
                console.log(data);
                console.log('network Table');
                _.forEach(data.output, function (item) {
                   item['p_value'] =item['p_value'].toFixed(2);
                });
                $('div.network-table-container').empty();
                var table = $('<table id="network_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody style="word-break:break-all;"></tbody></thead></table>');
                var thead = table.find('thead');
                var tr = $('<tr>');
                var header = ["#", "COUNT", "P_VALUE", "PATHWAY"];
                //if (data['output']['header'] != null) header = data.output.header;

                // header process
                _.forEach(header, function (item, idx) {
                    var th = $('<th>').text(item);
                    tr.append(th);
                });
                thead.append(tr);

                // body process
                var tbody = table.find('tbody');
                _.forEach(data.output, function (item, idx) {

                    var tr = $('<tr>');
                    _.forEach(header, function (key) {
                        var td = $('<td>');
                        td.text(item[key.toLowerCase()]);
                        tr.append(td);
                    });
                    tbody.append(tr);
                });

                $('div.network-table-container').append(table);
                var oTable = table.DataTable(
                    {
                        "columnDefs": [{
                            "searchable": false,
                            "orederable": false
                        }, {width: "10%"}, {width: "10%"}, {width: "70%"}],
                        paging: false,
                        scrollY: '100%',
                        dom: '<f<t>>',
                        //ordering:false,
                        //autoWidth:true
                    });

                //indexing
                oTable.on('order.dt search.dt', function () {
                    oTable.column(0, {search: 'applied', order: 'applied'}).nodes().each(function (cell, i) {
                        cell.innerHTML = i + 1;
                    });
                    $('#network_table').dataTable().api().columns.adjust();
                }).draw();
            }
        });
})(visualizer);