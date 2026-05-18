import os
import hashlib
import secrets
import random
from time import perf_counter_ns as perf_ns

random.seed(perf_ns())


path = '/data/data/com.termux/files/home/storage/shared/DCIM/Media'

if os.path.exists(path):
  os.chdir(path)
  files = os.listdir(path)
  for f in files:
    fname = secrets.token_hex(16)
    fext = f.split('.')[-1]
    fname = '.'.join((fname, fext))
    os.rename(f, fname)
    # os.system('cat {} > {}'.format(f, fname))
    # os.system('shred {}'.format(f))
    # os.unlink(f)

# --
os.system('termux-media-scan .')

