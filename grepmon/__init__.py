##############################################################################
# Copyright (c) 2021, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##############################################################################

# Module Imports
import logging
import re
import os
import subprocess
import sys
import textwrap
import time

from termcolor import colored
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

logger = logging.getLogger()

NL = re.compile("\n")
COL = re.compile(":\s*")

def run(cmd):
    data = {}
    output = subprocess.check_output(cmd).decode()

    if output != "":
        for i in re.split(NL, output):
            try:
                [filename, pattern] = re.split(COL, i, maxsplit=1)
                if filename in data:
                    data[filename].append(pattern)
                else:
                    data[filename] = [pattern]
            except ValueError:
                pass
            except:
                logging.debug("Error: %s", i)
    return data

def dump(data):
    clear()
    output = []

    pats = 0
    for filename, patterns in data.items():
        output.append(colored(filename, "green"))

        for pattern in patterns:
            output.append(colored(textwrap.fill(f"— {pattern}", initial_indent="    ", subsequent_indent="      "), "red"))
            pats += 1

    output.append(f"Pattern Matches:    {pats}")
    output.append(f"Files with Matches: {len(data)}")

    print("\n".join(output))

def clear():
    os.system('clear')


class Handler(PatternMatchingEventHandler):

    def __init__(self, cmd):
        self.cmd = cmd
        self.report()
        PatternMatchingEventHandler.__init__(self, self.watchfiles, None, False, True)

    def report(self):
        self.data = run(self.cmd)
        self.watchfiles = self.data.keys()
        clear()
        dump(self.data)

    def on_created(self, event):
        logger.debug("New File: %s", event.src_path)
        self.report()

    def on_deleted(self, event):
        logger.debug("Deleted File: %s", event.src_path)
        self.report()

    def on_modified(self, event):
        logger.debug("Modified File: %s", event.src_path)
        self.report()

    def on_moved(self, event):
        logger.debug("Modified File: %s to %s", event.src_path, event.dest_path)
        self.report()


def watch(cmd):
    handler = Handler(cmd)
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    try:
        while len(handler.watchfiles) > 0:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        sys.exit(0)

def main():
    """Main process called from command-line."""

    if len(sys.argv) <= 1:
        sys.exit(1)

    cmd = sys.argv[1:]

    # Validate Command before Running
    valid = cmd[0] in ["grep", "egrep", "fgrep", "rgrep"]
    if not valid:
        if input(f"Is {cmd[0]} a grep-like utility: ") not in ["y", "Y", "yes"]:
            print(f"Invalid Utility: {cmd[0]}")
            sys.exit(1)

    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.DEBUG)
    watch(cmd)








