

class BatchCmdReport:


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
    def export_report():
        print("todo")
        # usar o template para gerar o html do report