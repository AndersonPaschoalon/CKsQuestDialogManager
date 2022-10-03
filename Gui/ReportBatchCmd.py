from datetime import datetime
from Settings.AppInfo import AppInfo


class ReportBatchCmd:

    HTML_REPORT_HEADER = """<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>CodePen - Responsive Tables using LI</title>
  <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
<style>
body {
  font-family: "lato", sans-serif;
}

.container {
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 10px;
  padding-right: 10px;
}

h2 {
  font-size: 26px;
  margin: 20px 0;
  text-align: center;
}
h2 small {
  font-size: 0.5em;
}

.responsive-table li {
  border-radius: 3px;
  padding: 25px 30px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
}
.responsive-table .table-header {
  background-color: #95A5A6;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.responsive-table .table-row {
  background-color: #ffffff;
  box-shadow: 0px 0px 9px 0px rgba(0, 0, 0, 0.1);
}
.responsive-table .col-1 {
  flex-basis: 10%;
}
.responsive-table .col-2 {
  flex-basis: 30%;
}
.responsive-table .col-3 {
  flex-basis: 60%;
}
.responsive-table .col-4 {
  flex-basis: 0%;
}
@media all and (max-width: 767px) {
  .responsive-table .table-header {
    display: none;
  }
  .responsive-table li {
    display: block;
  }
  .responsive-table .col {
    flex-basis: 100%;
  }
  .responsive-table .col {
    display: flex;
    padding: 10px 0;
  }
  .responsive-table .col:before {
    color: #6C7A89;
    padding-right: 10px;
    content: attr(data-label);
    flex-basis: 50%;
    text-align: right;
  }
}
</style>
<!--
<link rel="stylesheet" href="./style.css">
-->
</head>
<body>
<!-- partial:index.partial.html -->
<div class="container">
  <h2>Batch Fuz Export Report Status</h2>
  <ul class="responsive-table">
    <li class="table-header">
      <div class="col col-1">Result</div>
      <div class="col col-2">Report</div>
      <div class="col col-3">Stdout</div>
      <div class="col col-4"></div>
    </li>
    <!-- Upper part-->
"""
    HTML_REPORT_FOOTER = """    <!-- Footer part-->
      </ul>
</div>
<!-- partial -->
  
</body>
</html>
    """
    # 0 - red/blue
    # 1 - ERROR/SUCCESS
    # 2 - Command
    # 3 - Error Code
    # 4 - Error Message
    # 5 - Process Return Code
    # 6 - Console Output
    HTML_REPORT_TABLE = """    <li class="table-row">
      <div class="col col-1" data-label="Job Id"><span style="color:{0}">{1}</span> </div>
      <div class="col col-2" data-label="Customer Name">Command: <span style="font-family:'Courier New'">{2}</span><br> Error Code: {3}<br> Message: {4} <br> Proccess Return Code: {5}</div>
      <div class="col col-3" data-label="Amount">{6}</div>
      <div class="col col-4" data-label="Payment Status"></div>
    </li>
    """


    def __init__(self):
        self.error_flag = False
        self.error_code = 0
        self.error_message = ""
        self.command = ""
        self.stdout = ""
        self.process_code = 0
        self.file_name = ""
        self.exe_dir = ""

    @staticmethod
    def count_errors(list_batch_cmds_reports):
        i = 0
        for item in list_batch_cmds_reports:
            if not item.error_flag:
                i += 1
        return i

    @staticmethod
    def count_success(list_batch_cmds_reports):
        i = 0
        for item in list_batch_cmds_reports:
            if item.error_flag:
                i += 1
        return i

    @staticmethod
    def export_report(list_batch_cmds_reports, app_dir: str):
        app = AppInfo(app_dir)
        filename = "batchCmdReport_"
        now = datetime.now()
        dt_string = now.strftime("-%d-%m-%Y_%H-%M-%S")
        filename = app.settings_obj.docgen_reports + filename + dt_string + ".html"
        html_str = ReportBatchCmd.HTML_REPORT_HEADER
        item: ReportBatchCmd
        for item in list_batch_cmds_reports:
            color = 'blue' if item.error_flag else 'blue'
            result = 'SUCCESS' if item.error_flag else 'ERROR'
            html_item = ReportBatchCmd.HTML_REPORT_TABLE.format(color, result, item.command, item.error_code,
                                                                 item.error_message, item.process_code, item.stdout)
            html_str += html_item
        html_str += ReportBatchCmd.HTML_REPORT_FOOTER
        with open(filename, "w") as text_file:
            text_file.write(html_str)
        return filename
