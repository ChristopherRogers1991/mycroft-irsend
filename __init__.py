# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from os.path import dirname
from py_irsend import irsend

__author__ = 'ChristopherRogers1991'
logger = getLogger(__name__)


class IrsendSkill(MycroftSkill):
    def __init__(self):
        self.remote_name_table = dict()
        self.code_name_table = dict()
        super(IrsendSkill, self).__init__(name="IrsendSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        for remote in irsend.list_remotes():
            for code in irsend.list_codes(remote):
                name = code.lower().replace('_', ' ')
                self.code_name_table[name] = code
                self.register_vocabulary(name, 'Code')

            name = remote.lower().replace('_', ' ')
            self.remote_name_table[name] = remote
            self.register_vocabulary(name, 'Remote')

        send_code_intent = IntentBuilder("IrsendIntent")\
            .require("SendKeyword")\
            .require("Remote") \
            .require("Code")\
            .build()

        self.register_intent(send_code_intent,
                             self.handle_send_code_intent)

    def handle_send_code_intent(self, message):
        name = message.metadata.get("Remote")
        remote = self.remote_name_table[name]

        name = message.metadata.get("Code")
        code = self.code_name_table[name]
        try:
            irsend.send_once(remote, [code])
        except Exception as e:
            logger.exception(type(e) + ' ' + e.message)
            self.speak("Error sending I R signal.")

    def stop(self):
        pass


def create_skill():
    return IrsendSkill()
