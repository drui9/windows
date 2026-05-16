import os
import select

fifo_path = '/tmp/myfifo'
os.mkfifo(fifo_path, exist_ok=True)

# Open in non-blocking mode initially
fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)

while True:
    rlist, _, _ = select.select([fd], [], [], 5)
    if fd in rlist:
        data = os.read(fd, 4096)
        if data:
            print(f"Got: {data.decode()}")
        else:
            # EOF - reopen
            os.close(fd)
            fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
