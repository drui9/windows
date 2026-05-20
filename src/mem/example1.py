import os
import mmap
import time

fifo_path = '/tmp/myfifo'
os.mkfifo(fifo_path, exist_ok=True)

# Open and create mmap
fd = os.open(fifo_path, os.O_RDWR)
m = mmap.mmap(fd, 0, access=mmap.ACCESS_READ)

while True:
    m.seek(0)
    data = m.read()
    if data:
        print(f"Data: {data.decode()}")
    time.sleep(0.1)
