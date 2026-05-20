#!/usr/bin/python
import os
import secrets

bindir = '/data/data/com.termux/files/home/storage/dcim/Camera'
binfiles = os.listdir(bindir)

for file in binfiles:
    fpath = os.path.join(bindir, file)
    rname = os.path.join(bindir, secrets.token_hex(8))
    os.rename(fpath, rname)
    print('renamed: {} to {}'.format(fpath, rname))

# todo: binary tree storage404

