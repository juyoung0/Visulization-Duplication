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
                $('.history-table-container').empty();
                var table = $('<table id="action_history_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody></tbody></thead></table>');
                var parsedData = _.map(data.output, function (item, idx) {
                    switch (item.action) {
                        default:
                            console.log(item.parameter);
                            item.param_label = _.map(_.omit(item.parameter,['block_iden','block_ver']),function (val,key) {
                                return val;
                            }).join(", ");
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
                var header = ["#", "DATE", "SCOPE", "ACTION", "DETAIL"];
                _.forEach(header, function (item, idx) {
                    var th = $('<th>').text(item);
                    tr.append(th);
                });
                thead.append(tr);
                var tbody = table.find('tbody');
                _.forEach(parsedData, function (item, idx) {
                    var tr = $('<tr>');
                    var check_td = $('<td><input name="check-action" class="checkbox" type="checkbox" value="' + item.action_id + '"></td>');
                    var date_td = $('<td></td>').text(visualizer.transformHistroyTimestamp(item.date)).attr('title', item.date);
                    var scope_td = $('<td></td>').text(item.scope);
                    var action_td = $('<td></td>').text(item.action);
                    var detail_td = $('<td></td>').text(item.param_label);
                    tr.append(check_td, date_td, scope_td, action_td, detail_td);
                    if (item.is_undo) {
                        tr.addClass('action-undo');
                    }
                    if (historyManager.UNABLE_UNDO.indexOf(item.action) != -1) {
                        tr.addClass('prevent-undo');
                    }else {
                        tr.addClass('can-undo');
                        tr.css('cursor','pointer');
                    }
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
                        scrollY: '30vh',
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
                                        var x = $('.can-undo input[name="check-action"]');
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
                            $("div.toolbar").html('<div class="btn-group"><a class="btn btn-xs btn-default btn-undo" href="#" title="Undo">Undo</a><a class="btn btn-xs btn-default btn-redo" href="#" title="Redo">Redo</a></div>');
                            $("div.msgbox").html('<div></div>');
                            $(".dropdown-toggle").dropdown();

                            $('#action_history_table >tbody >tr').on('click', function (e) {
                                var thisTr = $(this);
                                if (thisTr.hasClass('prevent-undo')) {
                                    alert("Can't undo this action.");
                                    return;
                                }

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
                                        userManager.showSession(userManager.SESSION, userManager.SESSION_VER);
                                        historyManager.getUnitHistory(userManager.SESSION, userManager.SESSION_VER);
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
                                    if (!data.success) return historyManager.failAjax(data, status);
                                    checked.removeClass('action-undo');
                                    userManager.showSession(userManager.SESSION, userManager.SESSION_VER);
                                    historyManager.getUnitHistory(userManager.SESSION, userManager.SESSION_VER);
                                });
                            });
                            $('#action_history_table').on('draw.dt', function () {
                                //$('#action_history_table').dataTable().fnAdjustColumnSizing();
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
                }
            },
            setupDependentModal: function (data) {
                $('.history-dependent-table-container').empty();
                var table = $('<table id="history_dependent_table" class="display compact" cellspacing="0" width="100%"><thead></thead><tbody></tbody></thead></table>');

                var thead = table.find('thead');
                var tr = $('<tr>');
                var header = ["#", "SESSION", "UNIT", "ACTION", "DEPENDENT UNITS"];
                _.forEach(header, function (item, idx) {
                    var th = $('<th>').text(item);
                    tr.append(th);
                });
                thead.append(tr);
                var tbody = table.find('tbody');
                _.forEach(data, function (item, idx) {
                    var tr = $('<tr>');
                    var check_td = $('<td><input name="check-action" class="checkbox" type="checkbox" value="' + item.action_id + '"></td>');
                    var td1 = $('<td></td>').text(item.session_name + "-" + item.session_ver);
                    var td2 = $('<td></td>').text(item.block_iden + "-" + item.block_ver);
                    var td3 = $('<td></td>').text(item.action);
                    var td4 = $('<td></td>').append(_.map(item.depend, function (item) {
                        var $item = $('<span class="label" style="margin-right:2px">').text(item.block_iden + "-" + item.block_ver);
                        if (item.detail == "Can run") {
                            $item.addClass('label-primary');
                        } else {
                            $item.addClass('label-danger');
                        }
                        return $item;
                    }));
                    tr.append(check_td, td1, td2, td3, td4);
                    tr.data(item);
                    tbody.append(tr);
                });
                $('.history-table-container').append(table);
                var oTable = table.DataTable(
                    {
                        paging: false,
                        scrollY: '30vh',
                        scrollCollapse: true,
                        dom: "ft",
                        autoWidth: true,
                        fixedHeader: true,
                        initComplete: function () {
                            var api = this.api();

                            api.columns().indexes().flatten().each(function (i) {
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
                            });
                            $('#history_dependent_table >tbody >tr').on('click', function (e) {
                                var thisTr = $(this);
                                var checkbox = thisTr.find('input[name="check-dependent-action"]');
                                var checked = checkbox.prop('checked');
                                checked ? checkbox.prop("checked", false) : checkbox.prop("checked", true);
                            });

                            $('#history-dependent-modal').on('shown.bs.modal', function () {
                                oTable.dataTable().adjust();
                            });


                            // undo bind
                            $('.btn-choose-undo').on('click', function (e) {

                            });
                        }
                    });
                $('#history-dependent-modal').modal('show');
            }
        });
})(visualizer);
