import os
import mmap
import time

MEM_SIZE = 1024

file_path = 'tempfile'
if not os.path.exists(file_path):
    with open(file_path, 'wb') as f:
        f.write(os.urandom(MEM_SIZE))

# Open and create mmap
fd = os.open(file_path, os.O_RDWR)
m = mmap.mmap(fd, 0, access=mmap.ACCESS_READ|mmap.ACCESS_WRITE)

m.seek(0)

# --
blob = b'\x00' * 1024
m.write(blob)

# --
m.seek(0)
data = m.read()
print(data, len(data))
os.close(fd)

