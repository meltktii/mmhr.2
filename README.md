# MMHR
# try


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MMHR Census</title>
    <link rel="stylesheet" href="sige\summary.css">
</head>
<body class="container mt-4">
    
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="index.php">BMCI</a>
    </div>
</nav>

<aside>
    <div class="sidebar">
        <h2>Upload Excel File</h2>
        <form action="upload.php" method="POST" enctype="multipart/form-data">
            <input type="file" name="excelFile" accept=".xlsx, .xls">
            <button type="submit">Upload</button>

            <button onclick="printTable()" class="btn btn-success">Print Table</button>

        </form>
    </div>
</aside>

<div class="table-responsive">
    <h2 class="text-center mb-4">MMHR Census Summary Table</h2>
    <form action="mmhr_census.php" method="GET">
        <input type="hidden" name="sheet_1" value="<?php echo $selected_sheet_1; ?>">
        <input type="hidden" name="sheet_2" value="<?php echo $selected_sheet_2; ?>">
        <input type="hidden" name="sheet_3" value="<?php echo $selected_sheet_3; ?>">
        <button type="submit" class="btn btn-primary mt-3">View MMHR Census</button>
    </form>

    <form method="GET" class="mb-3">
        <div class="sige">
        <label class="col2-5"></label>
        <select name="sheet_1" onchange="this.form.submit()" class="form-select mb-2">
            <?php foreach ($sheets as $sheet) { ?>
                <option value="<?php echo $sheet; ?>" <?php echo $sheet === $selected_sheet_1 ? 'selected' : ''; ?>>
                    <?php echo $sheet; ?>
                </option>
            <?php } ?>
        </select>
        <label class="col7"></label>
        <select name="sheet_2" onchange="this.form.submit()" class="form-select mb-2">
        <option value="" disabled selected>Select Admission Sheet</option>
            <?php foreach ($sheets_2 as $sheet) { ?>
                <option value="<?php echo $sheet; ?>" <?php echo $sheet === $selected_sheet_2 ? 'selected' : ''; ?>>
                    <?php echo $sheet; ?>
                </option>
            <?php } ?>
        </select>
        <label class="col8"></label>
        <select name="sheet_3" onchange="this.form.submit()" class="form-select mb-2">
        <option value="" disabled selected>Select Discharge Sheet</option>
            <?php foreach ($sheets_3 as $sheet) { ?>
                <option value="<?php echo $sheet; ?>" <?php echo $sheet === $selected_sheet_3 ? 'selected' : ''; ?>>
                    <?php echo $sheet; ?>
                </option>
            <?php } ?>
        </select>
        </div>
    </form>

    <div class="table-responsive1" id="printable">
        <table class="table table-bordered">
            <thead class="table-dark text-center">
            <tr>
                    <th colspan="1" style="background-color: black; color: white;">1</th>
                    <th colspan="2" style="background-color: black; color: white;">2</th>
                    <th colspan="5" style="background-color: black; color: white;">3</th>
                    <th rowspan="1" style="background-color: black; color: white;">4</th>
                    <th rowspan="1" style="background-color: black; color: white;">5</th>
                    <th colspan="2" style="background-color: black; color: white;">6</th>
                    <th rowspan="1" style="background-color: black; color: white;">7</th>
                    <th colspan="2" style="background-color: black; color: white;">8</th>
                    <th colspan="2" style="background-color: black; color: white;">9</th>
                </tr>
                <tr>
                    <th rowspan="2" style="background-color: #c7f9ff;">Date</th>
                    <th colspan="2" style="background-color: yellow;">Employed</th>
                    <th colspan="5" style="background-color: yellow;">Individual Paying</th>
                    <th rowspan="2" style="background-color: yellow;">Indigent</th>
                    <th rowspan="2" style="background-color: yellow;">Pensioners</th>
                    <th colspan="2" style="background-color: #c7f9ff;"> NHIP / NON-NHIP</th>
                    <th rowspan="2" style="background-color: yellow;">Total Admissions</th>
                    <th colspan="2" style="background-color: yellow;">Total Discharges</th>
                    <th colspan="2" style="background-color: yellow;">Accumulated Patients LOHS</th>
                </tr>
                <tr>
                    <th style="background-color: green;">Gov’t</th><th style="background-color: green;">Private</th>
                    <th style="background-color: green;">Self-Employed</th><th style="background-color: green;">OFW</th>
                    <th style="background-color: green;">OWWA</th><th style="background-color: green;">SC</th><th style="background-color: green;">PWD</th>
                    <th style="background-color:rgb(0, 0, 0); color: white;">NHIP</th><th style="background-color: #c7f9ff;">NON-NHIP</th>
                    <th style="background-color: orange;">NHIP</th><th style="background-color: orange;">NON-NHIP</th>
                    <th style="background-color: blue;">NHIP</th><th style="background-color: blue;">NON-NHIP</th>
                </tr>
            </thead>
            <tbody>
                <?php 
                
                $totals = [
                    'govt' => 0, 'private' => 0, 'self_employed' => 0, 'ofw' => 0,
                    'owwa' => 0, 'sc' => 0, 'pwd' => 0, 'indigent' => 0, 'pensioners' => 0,
                    'nhip' => 0, 'non_nhip' => 0, 'total_admissions' => 0, 'total_discharges_nhip' => 0,
                    'total_discharges_non_nhip' => 0, 'lohs_nhip' => 0
                ];

                foreach ($summary as $day => $row) { 
                
                    foreach ($totals as $key => &$total) {
                        $total += $row[$key];
                    }
                ?>
                    <tr>
                        <td class="text-center"> <?php echo $day; ?> </td> 
                        <td class="text-center"> <?php echo $row['govt']; ?> </td>
                        <td class="text-center"> <?php echo $row['private']; ?> </td>
                        <td class="text-center"> <?php echo $row['self_employed']; ?> </td>
                        <td class="text-center"> <?php echo $row['ofw']; ?> </td>
                        <td class="text-center"> <?php echo $row['owwa']; ?> </td>
                        <td class="text-center"> <?php echo $row['sc']; ?> </td>
                        <td class="text-center"> <?php echo $row['pwd']; ?> </td>
                        <td class="text-center"> <?php echo $row['indigent']; ?> </td>
                        <td class="text-center"> <?php echo $row['pensioners']; ?> </td>
                        <td class="text-center" style="background-color: black; color: white;"> <?php echo $row['nhip']; ?> </td>
                        <td class="text-center"> <?php echo $row['non_nhip']; ?> </td>
                        <td class="text-center"> <?php echo $row['total_admissions']; ?> </td>
                        <td class="text-center"> <?php echo $row['total_discharges_nhip']; ?> </td>
                        <td class="text-center"> <?php echo $row['total_discharges_non_nhip']; ?> </td>
                        <td class="text-center"> <?php echo $row['lohs_nhip']; ?> </td>
                        <td class="text-center"> <?php echo $row['non_nhip']; ?> </td>
                    </tr>
                <?php } ?>

                <tfoot class="footer">
                <tr class="table-dark text-center fw-bold">
                    <td style="background-color:rgb(0, 0, 0); color: white;">Total</td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['govt']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['private']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['self_employed']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['ofw']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['owwa']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['sc']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['pwd']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['indigent']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['pensioners']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['nhip']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['non_nhip']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['total_admissions']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['total_discharges_nhip']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['total_discharges_non_nhip']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['lohs_nhip']; ?></td>
                    <td style="background-color:rgb(0, 0, 0); color: white;"><?php echo $totals['non_nhip']; ?></td>
                </tr>
                </tfoot>
            </tbody>
        </table>
    </div>
</div>

<script>
function printTable() {
    var printContents = document.getElementById('printableTable').innerHTML;
    var originalContents = document.body.innerHTML;

    var printWindow = window.open('', '', 'height=500, width=800');
    printWindow.document.write('<html><head><title>Print Table</title>');
    printWindow.document.write('<style>');
    printWindow.document.write('table { width: 100%; border-collapse: collapse; }');
    printWindow.document.write('th, td { border: 1px solid black; padding: 8px; text-align: center; }');
    printWindow.document.write('th { background-color: inherit !important; color: inherit !important; }');
    printWindow.document.write('</style></head><body>');
    printWindow.document.write(printContents);
    printWindow.document.write('</body></html>');
    
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
}
</script>

</body>
</html>


body, h1, h2, form, select, input, button {
    margin: 0;
    padding: 0;
}

body {
    display: flex;
    font-family: Arial, sans-serif;
    background-color: rgb(255, 255, 255);
}

.sidebar {
    width: 250px;
    height: 100vh;
    background-color: #333;
    color: white;
    padding: 20px;
    position: fixed;
}

.sidebar h2 {
    color: #fff;
    margin-bottom: 20px;
}

.sidebar form {
    margin-top: 10px;
}

.sidebar button {
    width: 100%;
    padding: 10px;
    margin: 5px 0;
    border: none;
    background-color: #444;
    color: white;
    cursor: pointer;
    border-radius: 10px;
}

.sidebar input[type="file"] {
    width: 90%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.navbar {
    width: 100%;
    height: 60px;
    background-color: #444;
    color: white;
    padding: 10px 20px;
    text-align: left;
    position: fixed;
    justify-content: space-between;
    top: 0;
    left: 0;
    z-index: 1000;
}

.navbar h1 {
    font-size: 1.5rem;
}

h2{
    position: relative;
    margin-top: 4%;
}

.content {
    margin-left: 270px;
    padding-top: 80px; 
    width: calc(100% - 270px);
    padding: 20px;
}

form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 20px 0;
}

form label {
    font-weight: bold;
}

form select{
    padding: 10px;
    font-size: 1rem;
    margin-left: 15px;
    width: 30%;
    display: flex;
}

form button {
    padding: 10px;
    font-size: 1rem;
    margin-left: 15px;
}

.table-responsive {
    position: relative;
    display: block;
    margin-top: 1%;
    margin-left: auto;
}

.table-responsive1{
    position: relative;
    display: block;
    margin-top: 2%;
    
}

.navbar-brand{
    color: white;
    font-size: 1.5rem;
}

.govt{
    background-color: lime;
}

tr, th, td{
    border: 2px solid black;
    padding: 10px;
}

table{
    overflow-y: auto;
    border: 2px solid black;
}

thead {
    position: sticky;
    top: 8.3%;
    background-color: black; 
    color: rgb(0, 0, 0);
    z-index: 10;
}

tbody{
    text-align: center;
    font-weight: bold;
}

tfoot{
    position: sticky;
    bottom: 0;
    background-color: black;  /* Ensure visibility */
    color: white;
    z-index: 10;
    text-align: center;
}

.sige{
    display: flex;
    justify-content: space-between;
    margin: auto;
    width: 50%;
    
}

@media print {
    body * {
        visibility: hidden; /* Hide everything */
        background-color: white;
    }
    
    table, table * {
        visibility: visible; /* Show the table */
    }
    
    table {
        border: none;
        position: absolute;
        margin-left: -119%;
        margin-top: -19%;
        
    }
    
    th {
        background-color: inherit !important; /* Preserve header color */
        -webkit-print-color-adjust: exact; /* Ensure color prints correctly */
        print-color-adjust: exact;
    }
}

