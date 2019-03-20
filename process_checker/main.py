"""
.. createdby: Darren Zhao Xie on 3/19/2019
.. currentmodule:: process_checker.main

Check if the process is running at certain time.
"""
import os
from threading import Thread
from time import sleep
from datetime import datetime
from process_checker.notifiers import Email

CHECK_ITI_FILE_PATH = '/path/to/file1'
CHECK_IL_FILE_PATH = '/path/to/file2'

APP_PROCESS = 'process_name1'
PROCESS_TIME = 5


class ProcessChecker:
    """
    Check if some process is running.
    """
    def __init__(self, iti_last_modified=None, il_last_modified=None):
        self.iti_modified_time = iti_last_modified
        self.il_modified_time = il_last_modified

    def run(self, process_name, process_time):
        """
        if it's the process time and files changed and the process is not running, send out notification email
        :param process_name: the name of the application process
        :param process_time: the time of the process expected to be running
        :return:
        """
        while True:
            if not self.time_check(process_time):
                # if distance >= 2, sleep 1 hour
                if self.distance_hours(process_time) >= 2:
                    sleep(3600)
                # if 2 > distance > 1, sleep 2 minutes
                else:
                    sleep(120)
                continue
            elif not self.file_changed() or self.is_process_running(process_name):
                continue
            else:
                Email().send(subject='ALERT: PROCESS NOT RUNNING ALERT',
                             body=f'{process_name} is not running by {process_time}')
                # sleep 1 hour to avoid infinite email sending
                sleep(3600)

    @staticmethod
    def time_check(process_time):
        """
        Check if the current time is the process time, if so return true, else false.
        :param process_time:
        :return:
        """
        now_hour = datetime.now().hour
        if now_hour == process_time:
            return True
        return False

    @staticmethod
    def is_process_running(process_name):
        """
        Check if process is running, if so return true, else false.
        :param process_name:
        :return:
        """
        current_processes = os.popen("ps -Af").read()
        if process_name in current_processes[:]:
            return True
        return False

    def file_changed(self):
        """
        Check file modified time, if changed, update property value and return true, else return false
        :return:
        """
        changed = False
        if os.path.exists(CHECK_ITI_FILE_PATH):
            iti_last_modified = os.path.getmtime(CHECK_ITI_FILE_PATH)
            if iti_last_modified != self.iti_modified_time:
                self.iti_modified_time = iti_last_modified
                changed = True
        if os.path.exists(CHECK_IL_FILE_PATH):
            il_last_modified = os.path.getmtime(CHECK_IL_FILE_PATH)
            if il_last_modified != self.il_modified_time:
                self.il_modified_time = il_last_modified
                changed = True
        return changed

    @staticmethod
    def distance_hours(process_time):
        """
        Check if the distance between process time and current time is bigger than / equal to 2 hours
        :return:
        """
        now_hour = datetime.now().hour
        distance = process_time - now_hour
        return distance if distance > 0 else distance + 24


if __name__ == '__main__':
    thread = Thread(target=ProcessChecker().run(process_name=APP_PROCESS, process_time=PROCESS_TIME))
    thread.start()
