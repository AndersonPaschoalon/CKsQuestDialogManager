import os
from PyUtils.Console import Console
from PyUtils.FileUtils import FileUtils
from PyUtils.FileUtils import Exts


class SkyAudioEncoder:

    RET_SUCCESS = 0
    RET_ERR_AUDIO_FILE_NOT_FOUND = -1
    RET_ERR_ENCODER_EXE_NOT_FOUND = -2
    RET_ERR_PROCESSING = -3
    ERROR_EXT_FILE_NOT_FOUND = "{0} file {1} could not be found."
    ERROR_FILE_NOT_FOUND_ENCODER = "Encoder application {0} could not be found."
    ERROR_COMMAND_EXECUTION = "Error executing command {0}. The return code was {1}"
    DEF_BITRATE = 192000
    EXE_XWMAENCODE = "xWMAEncode.exe"
    EXE_FUZ_EXTRACTOR = "fuz_extractor.exe"
    EXE_FFMPEG = "ffmpeg.exe"
    ENCODING = "ISO-8859-1"
    # # .\xWMAEncode.exe  -b 192000 .\TestAudio01.wav .\TestAudio01.xwm
    CMD_WAV_TO_XWM = "{0} -b {1} \"{2}\" \"{3}\" "
    # fuz_extractor.exe  -e  + fuz_file.fuz
    CMD_UNFUZ = "{0} -e \"{1}\""

    def __init__(self, exe_dir: str):
        """
        Constructor for SkyAudioEncoder. This class is a wrapper over three applications: xWMAEncode, fuz_extractor,
        and ffmpeg, intending to easy the process of converting audio back and forth between Skyrim audio encodings
        (such as FUZ and XWM) and common audio formats (WAV and MP3).
        :param exe_dir: directory where the encoders xWMAEncode, fuz_extractor, and ffmpeg are placed.
        """
        self.current_exe_dir = exe_dir
        exe_dir = exe_dir.replace(os.sep, '\\')
        self.xWMAEncode = os.path.join(exe_dir, SkyAudioEncoder.EXE_XWMAENCODE)
        self.fuz_extractor = os.path.join(exe_dir, SkyAudioEncoder.EXE_FUZ_EXTRACTOR)
        self.ffmpeg = os.path.join(exe_dir, SkyAudioEncoder.EXE_FFMPEG)
        self.last_error = ""
        self.last_stdout = ""
        self.last_ret_code = 0
        self.last_command = ""
        self.troubleshoot_stdout = ""

    def get_exe_dir(self):
        """
        Returns the execution directory of the current instance of the encoder.
        :return:
        """
        return self.current_exe_dir

    def unfuz(self, file: str):
        """
        Decode a file in FUZ format into XWM, LIP and WAV file formats, with the same file names.
        :param file: fuz file name.
        :return: Return the flag RET_SUCCESS in case of success, and an error flag in case of failure.
        """
        fuz_file = FileUtils.change_ext(file, Exts.EXT_FUZ)
        if not os.path.isfile(fuz_file):
            self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("FUZ", fuz_file)
            return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        if not os.path.isfile(self.fuz_extractor):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.fuz_extractor)
            return SkyAudioEncoder.RET_ERR_ENCODER_EXE_NOT_FOUND
        # .\fuz_extractor.exe -e .\TestAudio01_2.fuz
        cmd = SkyAudioEncoder.CMD_UNFUZ.format(self.fuz_extractor, fuz_file)
        cmd = self.fuz_extractor + " -e " + fuz_file
        ret = self._process_command(cmd)
        if ret != SkyAudioEncoder.RET_SUCCESS:
            return ret
        return self.xwm_to_wav(file)

    def mp3_to_wav(self, file: str):
        """
        Converts a mp3 file into wav.
        :param file: mp3 audio file.
        :return: Return the flag RET_SUCCESS in case of success, and an error flag in case of failure.
        """
        mp3_file = FileUtils.change_ext(file, Exts.EXT_MP3)
        wav_file = FileUtils.change_ext(file, Exts.EXT_WAV)
        if not os.path.isfile(mp3_file):
            self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("MP3", mp3_file)
            return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        if not os.path.isfile(self.ffmpeg):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.ffmpeg)
            return SkyAudioEncoder.RET_ERR_ENCODER_EXE_NOT_FOUND
        # ../App/Bin/ffmpeg.exe -y -i ..\Sandbox\enc3\TestAudio01Gen.mp3 -acodec pcm_u8  -ac 1 -ar 22050 ..\Sandbox\enc3\TestAudio01Gen.wav
        cmd = self.ffmpeg + " -y -i \"" + mp3_file + "\" \"" + wav_file + "\""
        return self._process_command(cmd)

    def xwm_to_wav(self, file: str):
        """
        Converts a XWM file into WAV format.
        :param file: the file name of the xwm file.
        :return: Return the flag RET_SUCCESS in case of success, and an error flag in case of failure.
        """
        xwm_file = FileUtils.change_ext(file, Exts.EXT_XWM)
        wav_file = FileUtils.change_ext(file, Exts.EXT_WAV)
        if not os.path.isfile(xwm_file):
            self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("XWM", xwm_file)
            return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        if not os.path.isfile(self.xWMAEncode):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.xWMAEncode)
            return SkyAudioEncoder.RET_ERR_ENCODER_EXE_NOT_FOUND
        # .\xWMAEncode.exe  .\TestAudio01.xwm .\TestAudio01Back.wav
        cmd = self.xWMAEncode + "  \"" + xwm_file + "\"  \"" + wav_file + "\""
        return self._process_command(cmd)

    def wav_to_xwm(self, file: str):
        """
        Converts a WAV file into XWM format.
        :param file: the file name of the WAV file.
        :return: Return the flag RET_SUCCESS in case of success, and an error flag in case of failure.
        """
        xwm_file = SkyAudioEncoder.change_ext(file, Exts.EXT_XWM)
        wav_file = SkyAudioEncoder.change_ext(file, Exts.EXT_WAV)
        if not os.path.isfile(wav_file):
            self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("WAV", wav_file)
            return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        if not os.path.isfile(self.xWMAEncode):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.xWMAEncode)
            return SkyAudioEncoder.RET_ERR_ENCODER_EXE_NOT_FOUND
        # .\xWMAEncode.exe  -b 192000 .\TestAudio01.wav .\TestAudio01.xwm
        cmd = SkyAudioEncoder.CMD_WAV_TO_XWM.format(self.xWMAEncode, str(SkyAudioEncoder.DEF_BITRATE), wav_file, xwm_file)
        return self._process_command(cmd)

    def fuz(self, file: str):
        """
        Generate fuz file from XWM and LIP files.
        :param file:
        :return:
        """
        self._try_to_gen_xwm(file, force_generation=False)
        xwm_file = SkyAudioEncoder.change_ext(file, Exts.EXT_XWM)
        lip_file = SkyAudioEncoder.change_ext(file, Exts.EXT_LIP)
        fuz_file = SkyAudioEncoder.change_ext(file, Exts.EXT_FUZ)
        if not os.path.isfile(xwm_file):
            self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("XWM", xwm_file)
            return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        if not os.path.isfile(lip_file):
            self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("LIP", lip_file)
            return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        if not os.path.isfile(self.fuz_extractor):
            self.last_error = SkyAudioEncoder.ERROR_FILE_NOT_FOUND_ENCODER.format(self.fuz_extractor)
            return SkyAudioEncoder.RET_ERR_ENCODER_EXE_NOT_FOUND
        # .\fuz_extractor.exe -c TestAudio01.fuz .\TestAudio01.lip .\TestAudio01.xwm
        cmd = self.fuz_extractor + " -c " + " \"" + fuz_file + "\"  \"" + lip_file + "\"  \"" + xwm_file + "\""
        return self._process_command(cmd)

    def get_last_encodder_ret_code(self):
        """
        Returns the last error code from the encoder
        :return:
        """
        return self.last_ret_code

    def get_last_stdout(self):
        """
        Returns the last stdoutput from the last executed command.
        :return:
        """
        return self.last_stdout

    def get_last_error(self):
        """
        Returns the last error message.
        :return:
        """
        return self.last_error

    def get_last_command(self):
        """
        Returns the last command executed.
        :return:
        """
        return self.last_command

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
        self.last_command = command
        [ret, stdout, stderr] = Console.execute(command)
        str_stdout = "stdout:\n" + str(stdout, SkyAudioEncoder.ENCODING) + " \nstderr:\n" +\
                     str(stderr, SkyAudioEncoder.ENCODING)
        self.last_ret_code = ret
        self.last_stdout = str_stdout
        if success_ret_code == ret:
            return SkyAudioEncoder.RET_SUCCESS
        else:
            self.last_error = SkyAudioEncoder.ERROR_COMMAND_EXECUTION.format(command, str(ret))
            # executing troubleshooting routine to gatter information
            self._troubleshooting()
            return SkyAudioEncoder.RET_ERR_PROCESSING

    def _troubleshooting(self):
        """
        Gatter some information to help troubleshooting.
        :return:
        """
        [ret, stdout, stderr] = Console.execute("dir")
        self.troubleshoot_stdout = str(stdout, SkyAudioEncoder.ENCODING) + "stderr:\n" + \
                                   str(stderr, SkyAudioEncoder.ENCODING)

    def _try_to_gen_xwm(self, file: str, force_generation: bool):
        """
        Tries to generate a XWM file if it does not exit.
        It first tries to generate if from wav. If the wav file does not exit, try from a mp3 file.
        :return:
        """
        xwm_file = FileUtils.change_ext(file, Exts.EXT_XWM)
        mp3_file = FileUtils.change_ext(file, Exts.EXT_MP3)
        wav_file = FileUtils.change_ext(file, Exts.EXT_WAV)
        # xwm does not exit, try to create
        if (not os.path.isfile(xwm_file)) or force_generation:
            # try to create from wav if exists
            if os.path.isfile(wav_file):
                self.wav_to_xwm(file)
            # try to create from mp3 if exist
            elif os.path.isfile(mp3_file):
                self.mp3_to_wav(file)
                self.wav_to_xwm(file)
            if not os.path.isfile(xwm_file):
                self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("XWM", xwm_file)
                return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        # it exists
        return SkyAudioEncoder.RET_SUCCESS

    def try_to_gen_wav(self, file: str, force_generation: bool):
        xwm_file = FileUtils.change_ext(file, Exts.EXT_XWM)
        mp3_file = FileUtils.change_ext(file, Exts.EXT_MP3)
        wav_file = FileUtils.change_ext(file, Exts.EXT_WAV)
        # wav does not exit, try to create
        if (not os.path.isfile(wav_file)) or force_generation:
            # try to create from wav if exists
            if os.path.isfile(xwm_file):
                self.xwm_to_wav(file)
            # try to create from mp3 if exist
            elif os.path.isfile(mp3_file):
                self.mp3_to_wav(file)
            if not os.path.isfile(wav_file):
                self.last_error = SkyAudioEncoder.ERROR_EXT_FILE_NOT_FOUND.format("WAV", wav_file)
                return SkyAudioEncoder.RET_ERR_AUDIO_FILE_NOT_FOUND
        # it exists
        return SkyAudioEncoder.RET_SUCCESS

    @staticmethod
    def change_ext(filename, new_ext):
        """
        Helper to change the extension from a filename
        :param filename:
        :param new_ext:
        :return:
        """
        return os.path.splitext(filename)[0] + "." + new_ext

if __name__ == '__main__':
    # print("oi")
    app_dir = "..\\App\\Bin\\"
    dir_files1 = "..\\Sandbox\\enc1\\"
    dir_files2 = "..\\Sandbox\\enc2\\"
    dir_files3 = "..\\Sandbox\\enc3\\"
    file = "TestAudio01"
    file3 = "TestAudio01Gen"
    b_test1 = True
    b_test2 = False
    b_test3 = False
    ret = True
    enc = SkyAudioEncoder(app_dir)

    if b_test1:
        ret = enc.fuz(dir_files1 + file)
        if ret != SkyAudioEncoder.RET_SUCCESS:
            print(enc.get_last_error())

    if b_test2:
        # print("Gererating XWM and LIP from FUZ")
        ret = enc.unfuz(dir_files2 + file)
        if ret != SkyAudioEncoder.RET_SUCCESS:
            print(enc.get_last_error())
        # print("Gererating WAV from XWM")
        ret = enc.xwm_to_wav(dir_files2 + file)
        if ret != SkyAudioEncoder.RET_SUCCESS:
            print(enc.get_last_error())

    if b_test3:
        # print("Gererating MP3 to WAV")
        ret = enc.mp3_to_wav(dir_files3 + file3)
        if ret != SkyAudioEncoder.RET_SUCCESS:
            print(enc.get_last_error())



