
class AppEditorCmd:
    VAR_FILENAME = "{file}"
    OPT_PROCESS = "PROCESS"

    def __init__(self, csv_editor_cmd: str):
        self._cmd = csv_editor_cmd
        self._is_process = False
        if csv_editor_cmd != None and csv_editor_cmd.strip().upper() == "PROCESS":
            self._is_process = True

    def is_process(self):
        return self._is_process

    def get_batch(self, filename):
        cmd = self._cmd
        cmd = cmd.replace(AppEditorCmd.VAR_FILENAME, '"{0}"'.format(filename))
        return cmd

