import threading

Log = print

f = open("./Log.txt", 'a')

cache = []
mutex = threading.Lock()


def writeFile():
    global cache
    tmp = cache
    mutex.acquire()
    cache = []
    mutex.release()
    f.writelines("\n".join(tmp))
    f.write("\n")
    f.flush()


def writeLog(str):
    mutex.acquire()
    cache.append(str)
    mutex.release()

    if len(cache) > 2:
        thread = threading.Thread(target=writeFile)
        thread.start()


Log = writeLog

# test
'''
import time


def writeLog():
    count = 0
    while True:
        Log("jkjflks %s  %s" % (threading.currentThread().getName(), str( count)))
        count = count + 1
        time.sleep(0.001)


for i in range(10):
    thread = threading.Thread(target=writeLog)
    thread.setName( str(i))
    thread.start()
'''