"""
mycroft-irsend : A Mycroft skill for issuing irsend commands

Copyright (C) 2016  Christopher Rogers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from os.path import dirname
from py_irsend import irsend
from subprocess import CalledProcessError

__author__ = 'ChristopherRogers1991'
logger = getLogger(__name__)


def intent_handler(function):
    def new_function(self, message):
        try:
            function(self, message)
        except CalledProcessError as e:
            logger.exception(e.message)
            self.speak_dialog('error')
        except OSError as e:
            logger.exception(e.message)
            self.speak_dialog('not.installed')
    return new_function


class IrsendSkill(MycroftSkill):
    def __init__(self):
        super(IrsendSkill, self).__init__(name="IrsendSkill")
        self.remote_name_table = dict()
        self.code_name_table = dict()
        self.address = self.config.get('address')
        self.device = self.config.get('device')

    def initialize(self):
        self.load_data_files(dirname(__file__))

        try:
            self._register_remotes()
        except OSError:
            logger.warning('irsend does not appear to be installed.')
        except CalledProcessError as e:
            logger.error('Unable to list remotes. Error was: ' + str(e))

        send_code_intent = IntentBuilder("IrsendIntent")\
            .require("SendKeyword")\
            .require("Remote")\
            .require("Code")\
            .optionally("Number")\
            .build()

        self.register_intent(send_code_intent,
                             self.handle_send_code_intent)

        register_remotes_intent = IntentBuilder("RegisterRemotesIntent")\
            .require('RegisterKeyword').build()

        self.register_intent(register_remotes_intent,
                             self.handle_register_remotes_intent)

    def _register_remotes(self):
        for remote in irsend.list_remotes(self.device, self.address):
            for code in irsend.list_codes(remote, self.device, self.address):
                name = code.lower().replace('_', ' ')
                self.code_name_table[name] = code
                self.register_vocabulary(name, 'Code')

            name = remote.lower().replace('_', ' ')
            self.remote_name_table[name] = remote
            self.register_vocabulary(name, 'Remote')

    @intent_handler
    def handle_register_remotes_intent(self, message):
        self._register_remotes()

    @intent_handler
    def handle_send_code_intent(self, message):
        name = message.data.get("Remote")
        remote = self.remote_name_table[name]

        name = message.data.get("Code")
        code = self.code_name_table[name]

        count = message.data.get("Number")
        irsend.send_once(remote, [code], count or 1, self.device, self.address)

    def stop(self):
        pass


def create_skill():
    return IrsendSkill()
