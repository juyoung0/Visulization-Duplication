/**
 * Created by dryji on 2017-03-08.
 */
(function (parent) {
    _.extend(parent,
        {
            createNetworkTable: function (data) {
                $('div.network-table-container').empty();
                var table = $('<table id="network_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody></tbody></thead></table>');
                var thead = table.find('thead');
                var tr = $('<tr>');
                var header=["#","TERM", "COUNT", "%", "P-VAL", "GENES"];
                if (data['output']['header'] != null) header = data.output.header;

                // header process
                _.forEach(header, function (item, idx) {
                    var th = $('<th>').text(item);
                    tr.append(th);
                });
                thead.append(tr);

                // body process
                var tbody = table.find('tbody');
                _.forEach(data.output,function (item,idx) {
                    var tr = $('<tr>');
                    _.forEach(header,function (key) {
                        var td = $('<td>');
                        td.text(item[key]);
                        td.append(tr);
                    });
                    tbody.append(tr);
                });

                $('div.network-table-container').append(table);

                var oTable = table.DataTable(
                    {
                        "columnDefs": [ {
                            "searchable": false,
                            "orderable": false,
                            "targets": 0
                        } ],
                        paging: false,
                        scrollY: '100%',
                        dom: '<f<t>>',
                        //ordering:false,
                        autoWidth:true
                    });
                oTable.on( 'order.dt search.dt', function () {
                    oTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                        cell.innerHTML = i+1;
                    } );
                } ).draw();
            }
        });
})(visualizer);