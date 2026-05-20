from multiprocessing import Process
import sys

# --
def compute():
  return print(sys.stdin.fileno(), id(sys.stdin))

print(sys.stdin.fileno(), id(sys.stdin))
proc = Process(target=compute)
proc.start()
proc.join()

# nb: main thread stdout != proc stdout
