# mycroft-irsend
A Mycroft skill for issuing [irsend](http://www.lirc.org/html/irsend.html) commands

## Short Demo
https://youtu.be/IQ58dPp8f3M

## Setup

1. Clone this repo into your third party skills folder (the current default is ~/.mycroft/skills, but it used to be ~/.mycroft/third_party_skills; check your global/local mycroft.conf files if you have issues)
  * `cd ~/.mycroft/skills && git clone https://github.com/ChristopherRogers1991/mycroft-irsend.git`
2. `cd` into the resulting `mycroft-irsend` directory
  * `cd ~/.mycroft/skills/mycroft-irsend`
3. If your mycroft instance runs in a virtual environment, activate it
  * `source ~/.virtualenvs/mycroft/bin/activate`
4. Install the required python libraries
  * `pip install -r requirements.txt`
5. Add the block below to your mycoft.conf file (`~/.mycroft/mycroft.conf`)
```
   "IrsendSkill": {
        "address": "<host>:<port>",
        "device": "<device>"
    }
```

If that file did not already exist (this is the first third party skill you have added), wrap that entire block in { }. The finished file should be valid json. If you have issues, use http://jsonlint.com/ to validate the json.

The address and device above are passed directly to irsend. Assuming you are running lirc on your mycroft unit (or the same host), and have only one lirc device, you should be able to leave them blank (e.g. `"address": ""`).

## Sample Phrases
1. List my avilable remotes
2. List the available codes for \<remote\>, e.g. List the available codes for my television
3. What are the available codes for my \<remote\>?
4. Send \<code\> to the \<remote\>, e.g. Send power to the television
5. Register my remotes -- Run this if you've added remotes to lirc, and want Mycroft to pick them up (otherwise they will be picked up on restart)

## Notes
For accurate speach-to-text and intent handling, remote and code names will be convernted to lower-case, and underscores will be converted to spaces, e.g. `SOUND_SYSTEM` will be converted to `sound system`. If you use a different word seperateor, e.g. a hyphen, it will be untouched during the keyword registration process, and mycroft may have difficulty identifying/acting upon your commands.
