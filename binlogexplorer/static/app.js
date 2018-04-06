$(document).ready(function () {

    fillChartData();
    fillBinlogData();

    function fillChartData() {
        $.get({
            url: 'binlog-parser/analysis', success: function (data) {
                data = JSON.parse(data);
                if (data.changes_by_identifier.length === 0 && data.transactions_by_identifier.length === 0) {
                    $("#charts").hide()
                } else {
                    createChart('Changes by ID', 'chart-by-changes', data.changes_by_identifier);
                    createChart('Transactions by ID', 'chart-by-transactions', data.transactions_by_identifier);
                }
            }
        })
    }

    function createChart(label, canvas_id, itens) {
        var top10Labels = [];
        var top10Values = [];
        var othersValue = 0
        var othersLabel = 'Others'
        var pieColors = (new DistinctColors({count: 10, lightMin: 50})).map(function (item) {
            return item.hex()
        }).concat('#000000');

        for (var i = 0; i < itens.length; i++) {
            if (top10Values.length < 10) {
                top10Labels.push(itens[i][0]);
                top10Values.push(itens[i][1]);
            } else {
                othersValue += itens[i][1]
            }
        }

        new Chart(document.getElementById(canvas_id).getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: top10Values.length < 10 ? top10Values : top10Values.concat([othersValue]),
                    backgroundColor: pieColors,
                    label: label
                }],
                labels: top10Labels.length < 10 ? top10Labels : top10Labels.concat([othersLabel])
            },
            options: {
                responsive: true,
                pieceLabel: {
                    render: 'percentage',
                    precision: 0,
                    showZero: true,
                    position: 'outside',
                    overlap: true,
                    showActualPercentages: true
                }
            }
        });
    }

    function createBinlogTable(transaction) {
        var html = '<table width="100%" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
            '<thead>' +
            '<th width="10%">Statement Number</th>' +
            '<th width="10%">Command Type</th>' +
            '<th width="80%">Actual Command</th>' +
            '</thead>' +
            '<tbody>';

        transaction.statements.forEach(function (statement, index) {
            statement.changes.forEach(function (change) {
                html += '<tr>' +
                    '<td align="center">' + index + '</td>' +
                    '<td align="center">' + change.command_type + '</td>' +
                    '<td style="text-align: left">' + change.actual_command + '</td>' +
                    '</tr>';
            });
        });

        html += '</tbody></table>';
        return html;
    }

    function fillBinlogData() {
        var table = $('#main-data').DataTable({
            "ajax": "binlog-parser/",
            "columns": [
                {
                    "className": 'details-control',
                    "orderable": false,
                    "data": null,
                    "defaultContent": ''
                },
                {"data": "start_date"},
                {"data": "end_date"},
                {"data": "total_changes"},
                {"data": "duration"},
                {"data": "identifiers"}
            ],
            "order": [[1, 'asc']],
            "lengthMenu": [[25, 50, 100, 500, 1000, 5000], [25, 50, 100, 500, 1000, 5000]]
        });

        $('#main-data tbody').on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = table.row(tr);

            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                row.child(createBinlogTable(row.data())).show();
                tr.addClass('shown');
            }
        });
    }
});
