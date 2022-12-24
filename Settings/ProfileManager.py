from PyUtils.Logger import Logger
import lxml.etree as ET
from Settings.AppInfo import AppInfo
from Settings.Profile import Profile
import os
import shutil
import traceback
import re


class ProfileManager:
    DEFAULT_PROFILE_NAME = "Default"
    STR_TRUE = "TRUE"

    def __init__(self):
        self._log = Logger.get()
        self._app = AppInfo()
        self._list_profile_files = [
            self._app.settings_file,
            self._app.csv_actors,
            self._app.csv_scene_order,
            self._app.csv_comments
        ]

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
        if not self._check_profile_name(profile_name):
            return False, "Profile must have only alphanumeric characters, - and _."

        # check if already exists
        ret, msg = self.profile_exist(profile_name)
        if ret:
            ret_msg = "Profile " + profile_name + " already exist. " + msg
            self._log.warn(ret_msg)
            return False, ret_msg

        # create a copy of the files settings.xml, Actors.csv, SceneOrder.csv and Comments.csv, following the rule
        self._log.debug("Creating backups for new profile")
        for file in self._list_profile_files:
            ret = self._backup_file(file, profile_name)
            if not ret:
                ret_msg = "Error creating backup files for new profile!"
                self._log.error(ret_msg)
                return False, ret_msg

        # create new profile entry
        ret, msg = self._add_new_profile(profile_name, comment)
        if not ret:
            return False, "Cant create new profile entry. Reason:" + msg
        else:
            return True, "Success"

    # ok
    def activate_profile(self, profile_to_activate):
        """
        Activate a given profile. The application MUST BE RESTARTED, otherwise can cause unpredictable behaviour.
        This method:
        (1) Checks of the profile_to_activate is already activated
            yes - returns True, and an status message
            no - continue
        (2) Check if profile_to_activate exists
            no - returns False, and an error message
            yes - continue
        (3) Rename the files to backup format <file-name>.<profile-name>.<extension>
        (4) Remove the <profile-name> from the profile files to be activated
        (5) Update profile configuration file.
        :param profile_to_activate:
        :return:
        """
        profile_to_activate.strip()
        list_profiles = self.get_profile_name_list()
        p_current = self.get_active_profile_name()

        # (1)
        if p_current == profile_to_activate:
            return True, "Profile is already active."

        # (2)
        if not (profile_to_activate in list_profiles):
            return False, "Profile " + profile_to_activate + " does not exit!"

        # (3)
        self._ensure_files_exist()
        self._log.debug("Rename the files to backup format <file-name>.<profile-name>.<extension>")
        for file in self._list_profile_files:
            ret = self._rename_add_backup_label(file_path=file, profile_name=p_current)
            if not ret:
                ret_msg = "Error creating backup files for new profile!"
                self._log.error(ret_msg)
                return False, ret_msg

        # (4)
        status_msg = ""
        for file in self._list_profile_files:
            ret = self._rename_remove_backup_label(final_path=file, profile_name=profile_to_activate)
            if not ret:
                ret_msg = "Error activating profile file " + file
                self._log.warn(ret_msg)
                status_msg += ret_msg + ", "
        self._ensure_files_exist()

        # (5)
        self._update_profile_flag(profile_name=p_current, is_active=False)
        self._update_profile_flag(profile_name=profile_to_activate, is_active=True)

        return ret, status_msg

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

    # ok
    def update_profile(self, new_profile_name, new_profile_description):
        """
        Rename the current active profile.
        :param new_profile_name:
        :return:
        """
        new_profile_name = new_profile_name.strip()
        p_current = self.get_active_profile_name()

        # Check the name
        if new_profile_name == p_current:
            return True, "Profile already has this name."
        # check profile name format
        new_profile_name = new_profile_name.strip()
        if not self._check_profile_name(new_profile_name):
            return False, "Profile must have only alphanumeric characters, - and _."

        # rename the entry in the config file
        self._update_profile(current_name=p_current,
                             profile_name=new_profile_name,
                             comment=new_profile_description)

    def update_target_profile(self, target_profile, new_profile_name, new_profile_description):
        print("todo")

    # ok
    def delete_profile(self, profile_name):
        profile_name = profile_name.strip()
        p_current = self.get_active_profile_name()

        # Check the name
        if profile_name == p_current:
            return False, "Cannot delete active profile. Change current active profile, and try again."

        # delete all files
        for file in self._list_profile_files:
            self._delete_backup_file(config_file_base=file, profile_name=profile_name)

        # remove entry from xml
        self._remove_node(profile_name=profile_name)

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
                active_str = str(child.attrib["active"]).strip().upper()
                p.active = True if active_str == ProfileManager.STR_TRUE else False
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

    def get_active_profile_name(self):
        ret, list_profiles, msg = self.get_profile_list()
        if not ret:
            # no profile is active, use Default as active
            return ProfileManager.DEFAULT_PROFILE_NAME
        for p in list_profiles:
            if p.active:
                return p.name
        return ProfileManager.DEFAULT_PROFILE_NAME

    ####################################################################################################################
    # helpers
    ####################################################################################################################

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

    def _remove_node(self, profile_name: str):
        if not os.path.exists(self._app.profiles_file):
            return False, "Profiles configuration file does not exist!"
        try:
            profile_name = profile_name.strip()
            tree = ET.parse(self._app.profiles_file)
            root = tree.getroot()
            for child in root:
                try:
                    if child.attrib["name"] != profile_name:
                        continue
                    else:
                        root.remove(child)
                except:
                    self._log.error("** Error: Exception caught at _update_profile!")
                    self._log.error("** Error: " + traceback.format_exc())
                    return False, "Exception caught: " + str(traceback.format_exc())
            pretty = ET.tostring(tree, encoding="utf-8", pretty_print=True)
            with open(self._app.profiles_file, "w") as f:
                f.write(pretty.decode("utf-8"))
            return True, "Success"
        except:
            self._log.error("** Error: Exception caught at _update_profile!")
            self._log.error("** Error: " + traceback.format_exc())
            return False, "Exception caught: " + str(traceback.format_exc())

    def _update_profile(self, current_name, profile_name: str, comment: str):
        if not os.path.exists(self._app.profiles_file):
            return False, "Profiles configuration file does not exist!"
        try:
            tree = ET.parse(self._app.profiles_file)
            root = tree.getroot()
            current_name.strip()
            profile_name.strip()
            for child in root:
                try:
                    if child.attrib["name"] == current_name:
                        child.attrib["name"] = profile_name
                        child.attrib["comment"] = comment
                except:
                    self._log.error("** Error: Exception caught at _update_profile!")
                    self._log.error("** Error: " + traceback.format_exc())
                    return False, "Exception caught: " + str(traceback.format_exc())
            pretty = ET.tostring(tree, encoding="utf-8", pretty_print=True)
            with open(self._app.profiles_file, "w") as f:
                f.write(pretty.decode("utf-8"))
            return True, "Success"
        except:
            self._log.error("** Error: Exception caught at _update_profile!")
            self._log.error("** Error: " + traceback.format_exc())
            return False, "Exception caught: " + str(traceback.format_exc())

    def _update_profile_flag(self, profile_name: str, is_active: bool):
        if not os.path.exists(self._app.profiles_file):
            return False, "Profiles configuration file does not exist!"
        try:
            tree = ET.parse(self._app.profiles_file)
            root = tree.getroot()
            profile_name.strip()
            for child in root:
                try:
                    if child.attrib["name"] == profile_name:
                        child.attrib["active"] = str(is_active)
                except:
                    self._log.error("** Error: Exception caught at _update_profile!")
                    self._log.error("** Error: " + traceback.format_exc())
                    return False, "Exception caught: " + str(traceback.format_exc())
            pretty = ET.tostring(tree, encoding="utf-8", pretty_print=True)
            with open(self._app.profiles_file, "w") as f:
                f.write(pretty.decode("utf-8"))
            return True, "Success"
        except:
            self._log.error("** Error: Exception caught at _update_profile!")
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

    def _delete_backup_file(self, config_file_base, profile_name):
        dir_name = os.path.dirname(config_file_base)
        base_name = os.path.basename(config_file_base)
        file_name, file_extension = os.path.splitext(base_name)
        bkp_name = os.path.join(dir_name, file_name + "." + profile_name + file_extension)
        if os.path.exists(bkp_name):
            os.remove(bkp_name)
            return True
        else:
            return False

    def _rename_remove_backup_label(self, final_path, profile_name):
        dir_name = os.path.dirname(final_path)
        base_name = os.path.basename(final_path)
        file_name, file_extension = os.path.splitext(base_name)
        bkp_name = os.path.join(dir_name, file_name + "." + profile_name + file_extension)
        self._log.info("rename " + bkp_name + " -> " + final_path)
        try:
            os.rename(bkp_name, final_path)
            return True
        except:
            self._log.warn("Exception renaming files: " + traceback.format_exc())
            return False

    def _rename_add_backup_label(self, file_path, profile_name):
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        file_name, file_extension = os.path.splitext(base_name)
        bkp_name = os.path.join(dir_name, file_name + "." + profile_name + file_extension)
        self._log.info("rename " + bkp_name + " -> " + file_path)
        try:
            os.rename(file_path, bkp_name)
            return True
        except:
            self._log.warn("Exception renaming files: " + traceback.format_exc())
            return False

    def _ensure_files_exist(self):
        for file in self._list_profile_files:
            if not os.path.exists(file):
                self._log.warn("For some reason, the file " + file + "does not exit. Creating empty file...")
                with open(file, 'w'):
                    pass
                self._log.info("Empty file " + file + " was created.")

    def _check_profile_name(self, prof_name: str):
        prof_name = prof_name.strip()
        if re.fullmatch("[A-Za-z0-9\-_]+", prof_name):
            return True
        else:
            return False




