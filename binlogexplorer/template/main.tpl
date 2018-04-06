<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Binlog Analyser</title>
    <link rel="stylesheet" href="/static/jquery.dataTables.min.css">
    <style>
        td.details-control {
            background: url('/static/details_open.png') no-repeat center center;
            cursor: pointer;
        }

        tr.shown td.details-control {
            background: url('/static/details_close.png') no-repeat center center;
        }

        td {
            text-align: center;
        }
    </style>
</head>
<body>

<div id="charts">
    <div style="width:49%; display: inline-block">
        <h1 style="text-align: center">Identifiers by Transactions (Top 10)</h1>
        <canvas id="chart-by-transactions"></canvas>
    </div>

    <div style="width:49%; display: inline-block">
        <h1 style="text-align: center">Identifiers by Changes (Top 10)</h1>
        <canvas id="chart-by-changes"></canvas>
    </div>
</div>

<table id="main-data" class="display" cellspacing="0" width="100%">
    <thead>
    <tr>
        <th></th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Total Changes</th>
        <th>Duration</th>
        <th>Identifiers</th>
    </tr>
    </thead>
    <tfoot>
    <tr>
        <th></th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Total Changes</th>
        <th>Duration</th>
        <th>Identifiers</th>
    </tr>
    </tfoot>
</table>

<script src="/static/jquery-1.12.4.min.js"></script>
<script src="/static/jquery.dataTables.min.js"></script>
<script src="/static/Chart.bundle.min.js"></script>
<script src="/static/distinct-colors.min.js"></script>
<script src="/static/Chart.PieceLabel.min.js"></script>
<script src="/static/app.js"></script>
</body>
</html>
