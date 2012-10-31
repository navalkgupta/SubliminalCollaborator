# All of SubliminalCollaborator is licensed under the MIT license.

#   Copyright (c) 2012 Nick Lloyd

#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:

#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHE`R
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.

import sublime
import threading
import time

MESSAGE_FORMAT = 'Collaboration[ %s ]'
PROGRESS_FORMAT = 'Collaboration[ %s ][%s]'
HEARTBEAT_FORMAT = 'Collaboration[ %s ][%s]'

currentMessage = ''
messageLock = threading.Lock()

'''
Thread to maintain the current status message, preventing other plugins from overwriting
the status.
'''
class StatusMaintainingPublisherThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            sublime.set_timeout(self.publish, 100)
            time.sleep(1.0)

    def publish(self):
        global currentMessage
        global messageLock
        messageLock.acquire()
        if len(currentMessage) > 0:
            view = sublime.active_window().active_view()
            view.set_status('subliminal_collaborator', currentMessage)
        messageLock.release()

if not 'STATUS_BAR_UPDATE_THREAD' in globals():
    STATUS_BAR_UPDATE_THREAD = StatusMaintainingPublisherThread()

'''
Publish a basic status message to the status bar.
'''
def status_message(message):
    global currentMessage
    global messageLock
    if STATUS_BAR_UPDATE_THREAD and not STATUS_BAR_UPDATE_THREAD.is_alive():
        STATUS_BAR_UPDATE_THREAD.start()
    messageLock.acquire()
    currentMessage = MESSAGE_FORMAT % message
    messageLock.release()

'''
Publish a progress bar style status message to the status bar.
Progress bar is 10 characters total.
'''
def progress_message(message, progress, total):
    global currentMessage
    global messageLock
    if STATUS_BAR_UPDATE_THREAD and not STATUS_BAR_UPDATE_THREAD.is_alive():
        STATUS_BAR_UPDATE_THREAD.start()
    ticks = int(round(float(progress)/total)) * 10
    space = 10 - ticks
    messageLock.acquire()
    currentMessage = PROGRESS_FORMAT % (message, ('=' * ticks + ' ' * space))
    messageLock.release()

def heartbeat_message(message, heartbeat):
    global currentMessage
    global messageLock
    if STATUS_BAR_UPDATE_THREAD and not STATUS_BAR_UPDATE_THREAD.is_alive():
        STATUS_BAR_UPDATE_THREAD.start()
    messageLock.acquire()
    currentMessage = HEARTBEAT_FORMAT % (message, heartbeat)
    messageLock.release()

def clear_message():
    global currentMessage
    global messageLock
    messageLock.acquire()
    currentMessage = ''
    messageLock.release()
