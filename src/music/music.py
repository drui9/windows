#!/usr/bin/python
import os
import sys
import time
import random
import signal
import subprocess as sp
from threading import Event
from time import perf_counter_ns

bindir = '/data/data/com.termux/files/usr/bin'
wildcard = '/data/data/com.termux/files/home/storage/music'
files = [os.path.join(wildcard, i) for i in os.listdir(wildcard) if i.split('.')[-1] in ['mp3', 'm4a', 'opus']]

delay = 3
shuffle = True
stop = Event()
playing = Event()
played = list()
random.seed(perf_counter_ns())
wait_timeout = 3

# --
play_cmd = '{}/termux-media-player play'.format(bindir)
info_cmd = '{}/termux-media-player info'.format(bindir)
stop_cmd = '{}/termux-media-player stop'.format(bindir)

# --
def duration(timestr):
  """Convert timestr[d:h:m:s] to total seconds"""
  if timestr.count(':') > 3:
    print('unimplemented time string: {}'.format(timestr))
    return -1
  parts = timestr.split(':')
  seconds = 0
  parts.reverse()
  for idx, item in enumerate(parts):
    part = int(item)
    if idx == 0: # seconds
      seconds += part
    elif idx == 1: # minutes
      seconds += part * 60
    elif idx == 2: # hours
      seconds += part * 60 * 60
    elif idx == 3: # days
      seconds += part * 24 * 60 * 60
  return seconds

# -- sp calls
def call_cmd(command: list):
  task = sp.Popen(
    command,
    stdout=sp.PIPE,
    stderr=sp.PIPE
  )
  task.wait()
  return task.returncode, task.stdout.read(), task.stderr.read()

# -- clean exit
def shutdown(*args, **kwargs):
  global stop
  global playing
  stop.set()
  cmd = stop_cmd.split(' ')
  call_cmd(cmd)
  playing.clear()

# -- configure shutdown
signal.signal(signal.SIGINT, shutdown)

# --
while not stop.is_set():
  if shuffle:
    nxt = random.choice([i for i in files if i not in played])
  else:
    nxt = files[len(played):][0]
  # --
  cmd = play_cmd.split(' ')
  cmd.append(nxt)
  retcode, out, err = call_cmd(cmd)
  if not retcode:
    playing.set()
    played.append(nxt)
    print(out)
    sys.stdout.flush()
  else:
    playing.clear()
    print('Play error: {}', (out, err))
  # --
  if playing.is_set():
    # --
    cmd = info_cmd.split(' ')
    _, out, _= call_cmd(cmd)
    out = out.strip(b'\n').split(b'\n')[-1].decode()
    out = out.split(' ')
    curr, dur = duration(out[-3]), duration(out[-1])
    delta = (dur - curr) - delay
    # -- todo: next, prev, stop
    delta = 5
    # -- wait till end of current song
    stop.wait(timeout=delta)
    playing.clear()

# --
shutdown()
print('played: {}/{} songs'.format(len(played), len(files)))

