# coding=utf-8
# 创建TCP服务器
import time
import threading
from socket import *
from time import ctime
from concurrent.futures import ThreadPoolExecutor

from Config import Config
from LoggerServer.Logger import Log
from GameServer.GameThread import RequestProcess
from DataPersistenceLayer.DatabaseHandler import Database

####################### configuration ############################
HOST = Config.HOST
PORT = Config.PORT
ADDRESS = (HOST, PORT)
NumMaxConnect = Config.NumMaxConnect
NumThreads = Config.NumThreads

DBHost = Config.DBHost
DBAccount = Config.DBAccount
DBPassword = Config.DBPassword
DatabaseName = Config.DatabaseName
NumMaxDBConnector = Config.NumMaxDBConnector

queue = []


def ProcessConnection(DBHandlerPool, ThreadPool):
    threadHandlers = []

    while True:
        if len(queue) == 0:
            time.sleep(0.01)
            continue

        if len(threadHandlers) == NumThreads:
            removelist = []
            for thandler in threadHandlers:
                if threadHandlers.done():
                    removelist.append(thandler)
            for obj in removelist:
                threadHandlers.remove(obj)

        DBHandler = None
        for handler in DBHandlerPool:
            if not DBHandlerPool[handler]:
                DBHandler = handler
                break

        if len(threadHandlers) < NumThreads and DBHandler != None:
            connect = queue.pop(0)
            DBHandlerPool[handler] = True
            thandler = ThreadPool.submit(RequestProcess, (connect[0], connect[1], DBHandler, DBHandlerPool))
            threadHandlers.append(thandler)
        else:
            time.sleep(0.01)


def Process( DBHandlerPool ):
    currDBHandlerIndex = -1
    while True:
        if len(queue) == 0:
            time.sleep(0.001)
            continue

        connect = queue.pop(0)
        currDBHandlerIndex = (currDBHandlerIndex + 1) % len( DBHandlerPool )
        thread = threading.Thread(target=RequestProcess, args=(connect[0], connect[1],currDBHandlerIndex, DBHandlerPool))
        thread.start()



def main():
    # 创建服务器套接字
    # AF_INET为ip地址族，SOCK_STREAM为流套接字
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # 套接字与地址绑定
    serverSocket.bind(ADDRESS)
    # 监听连接,传入连接请求的最大数
    serverSocket.listen(NumMaxConnect)

    # ThreadPool = ThreadPoolExecutor(max_workers=NumThreads)

    DBHandlerPool = [[Database(), None ] for i in range(NumMaxDBConnector)]
    for handler in DBHandlerPool:
        handler[0].Connect(DBHost, DBAccount, DBPassword, DatabaseName)
        handler[1] = threading.Lock()

    # threading.Thread(target=ProcessConnection, args=(DBHandlerPool, ThreadPool)).start()
    threading.Thread(target=Process, args=( [DBHandlerPool] )).start()

    Log("[%s] : Begin Listening." % ctime())
    while True:
        #        try:
        # 服务器套接字通过socket的accept方法等待客户请求一个连接
        clientSocket, address = serverSocket.accept()
        Log('...connected from: [ %s:%i ]' % (address[0], address[1]))
        queue.append((clientSocket, address))

        # DBHandler = None
        # for handler in DBHandlerPool:
        #     if not DBHandlerPool[handler]:
        #         DBHandler = handler
        #         DBHandlerPool[handler] = True
        #         break
        # thread = threading.Thread(target=RequestProcess, args=(clientSocket, address , DBHandler, DBHandlerPool))
        # thread.start()

'''
        except :
            if not clientSocket._closed :
                clientSocket.close()
            serverSocket.close()

            Log( "[%s] : Error Happened.Exit." % ctime() )
            break
'''

if __name__ == '__main__':
    main()
