import os
import subprocess
from PyUtils.Console import Console
from PyUtils.FileUtils import FileUtils
from PyUtils.FileUtils import Exts

class SkyAudioEncoder:

    ERROR_FILE_NOT_FOUND_FUZ = "FUZ file {0} could not be found."
    ERROR_FILE_NOT_FOUND_FUZ = "LIP file {0} could not be found."
    ERROR_FILE_NOT_FOUND_WAV = "WAV file {0} could not be found."
    ERROR_FILE_NOT_FOUND_XWM = "XWM file {0} could not be found."
    ERROR_FILE_NOT_FOUND_LIP = "LIP file {0} could not be found."
    ERROR_FILE_NOT_FOUND_MP3 = "MP3 file {0} could not be found."
    ERROR_FILE_NOT_FOUND_ENCODER = "Encoder application {0} could not be found."
    DEF_BITRATE = 192000
    EXE_XWMAENCODE = "xWMAEncode.exe"
    EXE_FUZ_EXTRACTOR = "fuz_extractor.exe"
    EXE_FFMPEG = "ffmpeg.exe"
    # ENCODING = "utf-8"
    ENCODING = "ISO-8859-1"

    def __init__(self, exe_dir: str):
        exe_dir = exe_dir.replace(os.sep, '\\')
        self.xWMAEncode = os.path.join(exe_dir, SkyAudioEncoder.EXE_XWMAENCODE)
        self.fuz_extractor = os.path.join(exe_dir, SkyAudioEncoder.EXE_FUZ_EXTRACTOR)
        self.ffmpeg = os.path.join(exe_dir, SkyAudioEncoder.EXE_FFMPEG)
        self.last_error = ""
        self.last_stdout = ""
        self.last_ret_code = 0

    def unfuz(self, file):
        fuz_file = FileUtils.change_ext(file, Exts.EXT_FUZ)
        if not os.path.isfile(fuz_file):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_FUZ.format(fuz_file)
            return False
        if not os.path.isfile(self.fuz_extractor):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.fuz_extractor)
            return False
        # .\fuz_extractor.exe -e .\TestAudio01_2.fuz
        cmd = self.fuz_extractor + " -e " + fuz_file
        ret = self._process_command(cmd)
        if not ret:
            return False
        return self.xwm_to_wav(file)

    def mp3_to_wav(self, file):
        mp3_file = FileUtils.change_ext(file, Exts.EXT_MP3)
        wav_file = FileUtils.change_ext(file, Exts.EXT_WAV)
        if not os.path.isfile(mp3_file):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_MP3.format(mp3_file)
            return False
        if not os.path.isfile(self.ffmpeg):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.ffmpeg)
            return False
        # ../App/Bin/ffmpeg.exe -y -i ..\Sandbox\enc3\TestAudio01Gen.mp3 -acodec pcm_u8  -ac 1 -ar 22050 ..\Sandbox\enc3\TestAudio01Gen.wav
        cmd = self.ffmpeg + " -y -i " + mp3_file + " -acodec pcm_u8  -ac 1 -ar 22050 " + wav_file
        print("cmd:" + cmd)
        return self._process_command(cmd)


    def xwm_to_wav(self, file):
        xwm_file = FileUtils.change_ext(file, Exts.EXT_XWM)
        wav_file = FileUtils.change_ext(file, Exts.EXT_WAV)
        if not os.path.isfile(xwm_file):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_XWM.format(xwm_file)
            return False
        if not os.path.isfile(self.xWMAEncode):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.xWMAEncode)
            return False
        # .\xWMAEncode.exe  .\TestAudio01.xwm .\TestAudio01Back.wav
        cmd = self.xWMAEncode + " " + xwm_file + " " + wav_file
        return self._process_command(cmd)

    def wav_to_xwm(self, file):
        xwm_file = SkyAudioEncoder.change_ext(file, Exts.EXT_XWM)
        wav_file = SkyAudioEncoder.change_ext(file, Exts.EXT_WAV)
        if not os.path.isfile(wav_file):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_WAV.format(wav_file)
            return False
        if not os.path.isfile(self.xWMAEncode):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.xWMAEncode)
            return False
        # .\xWMAEncode.exe  -b 192000 .\TestAudio01.wav .\TestAudio01.xwm
        cmd = self.xWMAEncode + " -b " + str(SkyAudioEncoder.DEF_BITRATE) + " " + wav_file + " " + xwm_file
        return self._process_command(cmd)

    def fuz(self, file):
        self.wav_to_xwm(file)
        xwm_file = SkyAudioEncoder.change_ext(file, Exts.EXT_XWM)
        lip_file = SkyAudioEncoder.change_ext(file, Exts.EXT_LIP)
        fuz_file = SkyAudioEncoder.change_ext(file, Exts.EXT_FUZ)
        if not os.path.isfile(xwm_file):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_XWM.format(xwm_file)
            return False
        if not os.path.isfile(lip_file):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_LIP.format(lip_file)
            return False
        if not os.path.isfile(self.fuz_extractor):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.fuz_extractor)
            return False
        # .\fuz_extractor.exe -c TestAudio01.fuz .\TestAudio01.lip .\TestAudio01.xwm
        cmd = self.fuz_extractor + " -c " + " " + fuz_file + " " + lip_file + " " + xwm_file
        return self._process_command(cmd)

    def get_last_ret_code(self):
        return self.last_ret_code

    def get_last_stdout(self):
        return self.last_stdout

    def get_last_error(self):
        return self.last_error

    @staticmethod
    def change_ext(filename, new_ext):
        return os.path.splitext(filename)[0] + "." + new_ext

    def _process_command(self, command, success_ret_code=0):
        """
        Process a command, and checks the return code.
        Notify as sucess if the return code is the expected.
        Stores the console result.
        In case the error, stores the error (retcode, stdout, stderr) information.
        :param command:
    :param success_ret_code:|Q
        :return:
        """
        print("command:" + command)
        [ret, stdout, stderr] = Console.execute(command)
        # [ret, stdout, stderr] = Console.execute("dir")
        print("[ret, stdout, stderr] = " + str([ret, stdout, stderr]))
        str_stdout = str(stdout, SkyAudioEncoder.ENCODING)
        str_stderr = str(stderr, SkyAudioEncoder.ENCODING)
        self.last_ret_code = ret
        if success_ret_code == ret:
            self.last_stdout = str_stdout
            return True
        else:
            self.last_stdout = str_stdout + "\n" + str_stderr
            self.last_error = "Return Code: " + str(ret) + "\n" +\
                              "Stdout:\n" + str_stdout +\
                              "Stderr:\n" + str_stderr
            print("--------------------------------------------")
            print(self.last_stdout)
            print("--------------------------------------------")
            print(self.last_error)
            return False


if __name__ == '__main__':
    print("oi")
    app_dir = "..\\App\\Bin\\"
    dir_files1 = "..\\Sandbox\\enc1\\"
    dir_files2 = "..\\Sandbox\\enc2\\"
    dir_files3 = "..\\Sandbox\\enc3\\"
    file = "TestAudio01"
    file3 = "TestAudio01Gen"
    b_test1 = False
    b_test2 = False
    b_test3 = True

    ret = True
    enc = SkyAudioEncoder(app_dir)
    if b_test1:
        ret = enc.fuz(dir_files1 + file)
    if b_test2:
        ret = enc.unfuz(dir_files2 + file)
    if b_test3:
        ret = enc.mp3_to_wav(dir_files3 + file3)
    if not ret:
        print("Error")
        print(enc.get_last_error())



