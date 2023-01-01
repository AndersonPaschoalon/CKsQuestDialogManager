import os
import shutil
from QuestExports.Consts import Consts


class SkyrimRepository:
    """
    This class is responsible for executing oprations inside the Skyrim installation folder, such as listing
    and copying files.
    """

    @staticmethod
    def get_dialog_export_files(skyrim_root: str) -> list:
        """
        Return all the expoted dialog files names inside Skyrim root directory.
        :param skyrim_root: The skyrim root directory.
        :return: list of exported dialog files.
        """
        all_files = [f for f in os.listdir(skyrim_root) if os.path.isfile(os.path.join(skyrim_root, f))]
        # filter all exported files from creation kit
        export_dialog_files = []
        for nth_file in all_files:
            if (nth_file.startswith(Consts.EXPORT_DIALOG_PREFIX) and
                    nth_file.endswith(Consts.EXPORT_DIALOG_EXT)):
                export_dialog_files.append(nth_file)
        return export_dialog_files

    @staticmethod
    def get_scene_dialog_files(skyrim_root: str) -> list:
        """
        Return all the scene dialog files names inside Skyrim root directory.
        :param skyrim_root: The skyrim root directory.
        :return: list of exported dialog files.
        """
        all_files = [f for f in os.listdir(skyrim_root) if os.path.isfile(os.path.join(skyrim_root, f))]
        # filter all exported files from creation kit
        export_dialog_files = []
        for nth_file in all_files:
            if (nth_file.startswith(Consts.EXPORT_SCENE_PREFIX) and
                    nth_file.endswith(Consts.EXPORT_SCENE_EXT)):
                export_dialog_files.append(nth_file)
        return export_dialog_files

    @staticmethod
    def import_skyrim_files(skyrim_root: str, local_root: str) -> bool:
        if not os.path.exists(skyrim_root):
            return False
        if not os.path.exists(local_root):
            return False
        # dialog files
        dialog_files = SkyrimRepository.get_dialog_export_files(skyrim_root)
        for file in dialog_files:
            shutil.copy2(os.path.join(skyrim_root, file), local_root)
        # Scene files
        scene_files = SkyrimRepository.get_scene_dialog_files(skyrim_root)
        for file in scene_files:
            shutil.copy2(os.path.join(skyrim_root, file), local_root)
        return True


if __name__ == '__main__':
    src = 'C:\Program Files (x86)\Steam\steamapps\common\Skyrim'
    dst = ".\\sandbox\\default"
    SkyrimRepository.import_skyrim_files(src, dst)


