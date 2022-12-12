from PyUtils.Logger import Logger
import lxml.etree as ET
from Settings.AppInfo import AppInfo
from Settings.Profile import Profile
import os
import shutil
import traceback


class ProfileManager:

    def __init__(self):
        self._log = Logger.get()
        self._app = AppInfo()

    # ok
    def create_profile(self, profile_name, comment):
        """
        Create a new profile, without activating it it
        :param profile_name:
        :param comment:
        :return: ret, msg - True in case the profile was created; False otherwise, Status message; contains the error
        reason of the ret is False; Success if it is True.
        """
        # check profile name format
        profile_name = profile_name.strip()
        if not str(profile_name).isalnum():
            return False, "Profile Name must be alhanumeric."

        # check if already exists
        ret, msg = self.profile_exist(profile_name)
        if ret:
            ret_msg = "Profile " + profile_name + " already exist. " + msg
            self._log.warn(ret_msg)
            return False, ret_msg

        # create a copy of the files settings.xml, Actors.csv, SceneOrder.csv and Comments.csv, following the rule
        self._log.debug("Creating backups for new profile")
        ret1 = self._backup_file(self._app.settings_file, profile_name)
        ret2 = self._backup_file(self._app.csv_actors, profile_name)
        ret3 = self._backup_file(self._app.csv_scene_order, profile_name)
        ret4 = self._backup_file(self._app.csv_comments, profile_name)

        if ret1 and ret2 and ret3 and ret4:
            # insert new profile entry
            self._log.debug("Create new profile entry!")
            ret, msg = self._add_new_profile(profile_name, comment)
            if not ret:
                return False, "Cant create new profile entry. Reason:" + msg
            else:
                return True, "Success"
        else:
            ret_msg = "Error creating backup files for new profile!"
            self._log.error(ret_msg)
            return False, ret_msg


    def activate_profile(self, new_active_profile):
        """
        Activate a given profile. The application MUST BE RESTARTED, otherwise can cause unpredictable behaviour.
        :param new_active_profile:
        :return:
        """
        ret, list_profiles, msg = self.get_profile_list()
        if not ret:
            return False, msg

        # read the name of the current active profile
        active_profile = ""
        there_is_active = False
        for p in list_profiles:
            if p.active:
                print("ACTIVE PROFILE IS ", p.name)
                there_is_active = True
                active_profile = p.name
        if not there_is_active:
            return False, "There is no current active profile."

        # check if new profile exist
        ret, msg = self.profile_exist(new_active_profile)
        if not ret:
            return False, "Profile to activate does not exist!"
        ret = self._backup_restore_and_activate(file_name=self._app.settings_file,
                                                current_profile=active_profile,
                                                to_activate_profile=new_active_profile)
        ret = self._backup_restore_and_activate(file_name=self._app.csv_actors,
                                                current_profile=active_profile,
                                                to_activate_profile=new_active_profile)
        ret = self._backup_restore_and_activate(file_name=self._app.csv_scene_order,
                                                current_profile=active_profile,
                                                to_activate_profile=new_active_profile)
        ret = self._backup_restore_and_activate(file_name=self._app.csv_comments,
                                                current_profile=active_profile,
                                                to_activate_profile=new_active_profile)
        return ret

    # ok
    def profile_exist(self, profile_name):
        """
        Tells if the profile name exists or not in the profiles.xml file.
        :param profile_name:
        :return: ret, msg
        """
        profile_name.strip()
        ret, list_profiles, msg = self.get_profile_list()
        if not ret:
            return False, msg

        for p in list_profiles:
            if p.name == profile_name:
                return True, "Profile name already exist!"

        return False, "Profile name does not exist!"

    def rename_profile(self, profile_name):
        print("todo")

    def delete_profile(self, profile_name):
        print("todo")

    def profile_info(self, profile_name):
        """
        Returns the information about the profile.
        :param profile_name: comment, active - The comment on the profile tag, True or False
        :return: comment, active - De profile description, True or False.
        """
        profile_name.strip()
        ret, list_profiles, msg = self.get_profile_list()
        for p in list_profiles:
            if p.name == profile_name:
                return p.comment, p.active
        return "", False

    def get_profile_list(self):
        """
        Returns a list of profile objects.
        :return: ret, list_profiles, msg - True or false, the list of Profile objects, The return message.
        """
        if not os.path.exists(self._app.profiles_file):
            return False, [], "Profiles configuration file does not exist!"

        tree = ET.parse(self._app.profiles_file)
        root = tree.getroot()
        list_profiles = []
        for child in root:
            p = Profile()
            try:
                p.name = child.attrib["name"]
                p.comment = child.attrib["comment"]
                p.active = bool(child.attrib["name"])
                list_profiles.append(p)
            except:
                self._log.Error("Cant read attib from profiles.xml")

        return True, list_profiles, "Success"

    def get_profile_name_list(self):
        """
        Returns the list of all profile names registered.
        :return: list_names - the list of all profile names.
        """
        list_names = []
        ret, list_profiles, msg = self.get_profile_list()
        for p in list_profiles:
            list_names.append(p.name)
        return list_names

    def _add_new_profile(self, profile_name, comment):
        if not os.path.exists(self._app.profiles_file):
            return False, "Profiles configuration file does not exist!"

        try:
            tree = ET.parse(self._app.profiles_file)
            root = tree.getroot()

            new_node = ET.SubElement(root, "p")
            new_node.set("name", profile_name)
            new_node.set("comment", comment)
            new_node.set("active", str(False))

            pretty = ET.tostring(tree, encoding="utf-8", pretty_print=True)
            with open(self._app.profiles_file, "w") as f:
                f.write(pretty.decode("utf-8"))
            return True, "Success"

        except:
            self._log.error("** Error: Exception caught at __main__!")
            self._log.error("** Error: " + traceback.format_exc())
            return False, "Exception caught: " + str(traceback.format_exc())

    def _backup_file(self, old_name, profile_name):
        profile_name.strip()
        dir_name = os.path.dirname(old_name)
        base_name = os.path.basename(old_name)
        # file extension already has a . at the beginning
        file_name, file_extension = os.path.splitext(base_name)
        new_name = os.path.join(dir_name, file_name + "." + profile_name + file_extension)
        self._log.info("copy " + old_name + " -> " + new_name)
        return shutil.copy2(old_name, new_name)

    def _rename_file_strip(self, final_name, profile_name):
        dir_name = os.path.dirname(final_name)
        base_name = os.path.basename(final_name)
        file_name, file_extension = os.path.splitext(base_name)
        bkp_name = os.path.join(dir_name, file_name + "." + profile_name + file_extension)
        self._log.info("rename " + bkp_name + " -> " + final_name)
        return os.rename(bkp_name, final_name)

    def _backup_restore_and_activate(self, file_name, current_profile, to_activate_profile):
        ret1 = self._backup_file(file_name, current_profile)
        ret2 = self._rename_file_strip(file_name, to_activate_profile)
        return ret1 and ret2


