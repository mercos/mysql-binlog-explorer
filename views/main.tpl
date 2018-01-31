<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Binlog Analyser</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css">
    <style>
        td.details-control {
            background: url('https://datatables.net/examples/resources/details_open.png') no-repeat center center;
            cursor: pointer;
        }

        tr.shown td.details-control {
            background: url('https://datatables.net/examples/resources/details_close.png') no-repeat center center;
        }
    </style>
</head>
<body>

<table id="example" class="display" cellspacing="0" width="100%">
    <thead>
    <tr>
        <th></th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Total Changes</th>
        <th>Duration</th>
    </tr>
    </thead>
    <tfoot>
    <tr>
        <th></th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Total Changes</th>
        <th>Duration</th>
    </tr>
    </tfoot>
</table>

<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
<script>

    function format(transaction) {
        var html = '<table width="100%" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
                '<thead>' +
                    '<th width="10%">Command Type</th>' +
                    '<th width="90%">Actual Command</th>' +
                '</thead>' +
                '<tbody>';

        transaction.statements.forEach(function(statement) {
            statement.changes.forEach(function(change) {
                html += '<tr>' +
                            '<td>' + change.command_type + '</td>' +
                            '<td>' + change.actual_command + '</td>' +
                        '</tr>';
            });
        });
        
        html += '</tbody></table>';
        return html;
    }

    $(document).ready(function () {
        var table = $('#example').DataTable({
            "ajax": "binlog-parser/",
            "columns": [
                {
                    "className":      'details-control',
                    "orderable":      false,
                    "data":           null,
                    "defaultContent": ''
                },
                { "data": "start_date" },
                { "data": "end_date" },
                { "data": "total_changes" },
                { "data": "duration" }
            ],
            "order": [[1, 'asc']],
            "lengthMenu": [[25, 50, 100, 500, 1000, 5000], [25, 50, 100, 500, 1000, 5000]]
        });

        $('#example tbody').on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = table.row(tr);

            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        });
    });
</script>
</body>
</html>
