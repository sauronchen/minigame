# coding=utf-8
import math
from socket import *
from Config import Config
from Protocal.generate import TransferProtocal_pb2

HOST = Config.HOST
PORT = Config.PORT
BufferSize = Config.BufferSize
ADDR = (HOST, PORT)


def receiveDataFromServer(server, address):
    data = b''
    while True:
        buf = server.recv(BufferSize)
        data = data + buf
        if len(buf.strip(b' ')) < BufferSize:
            break
    data = data.strip(b' ')
    return data


def sendDataToServer(server, address, data):
    data = data + (BufferSize - len(data) % BufferSize) * b" "
    pieces = len(data) // BufferSize
    for i in range(pieces):
        server.send(data[i * BufferSize: (i + 1) * BufferSize])


def testRegister() :
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    request = TransferProtocal_pb2.RequestType()
    request.request = TransferProtocal_pb2.RequestType.REGISTER_REQ

    data = request.SerializeToString()
    sendDataToServer(tcpCliSock, ADDR, data)

    request = TransferProtocal_pb2.Account()
    request.account = "hrhtrd4"
    request.password = "fhiuth"

    sendDataToServer(tcpCliSock, ADDR, request.SerializeToString())

    # data = tcpCliSock.recv(BufferSize)
    # ReplyCode = TransferProtocal_pb2.ResultType()
    # ReplyCode.ParseFromString(data)
    #
    # if ReplyCode.result == TransferProtocal_pb2.ResultType.REGISTER_RES:
    data = receiveDataFromServer(tcpCliSock, ADDR)
    tcpCliSock.send("OK".encode())
    result = TransferProtocal_pb2.RegisterRes()
    result.ParseFromString(data)
    #print(str(result.hasSucceed),str(result.error))

    tcpCliSock.close()


def testLogin() :
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    request = TransferProtocal_pb2.RequestType()
    request.request = TransferProtocal_pb2.RequestType.LOGIN_REQ

    data = request.SerializeToString()
    sendDataToServer( tcpCliSock,ADDR,data )

    request = TransferProtocal_pb2.Account()
    request.account = "hrhtr4"
    request.password = "fhfth"

    sendDataToServer(tcpCliSock, ADDR, request.SerializeToString())

    data = receiveDataFromServer(tcpCliSock, ADDR)
    tcpCliSock.send("OK".encode())
    result = TransferProtocal_pb2.LoginRes()
    result.ParseFromString(data)
    #print(str(result.hasSucceed),str(result.error))

    tcpCliSock.close()


def testSaveArchive():
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    request = TransferProtocal_pb2.RequestType()
    request.request = TransferProtocal_pb2.RequestType.SAVE_ARCHIVE_REQ

    data = request.SerializeToString()
    sendDataToServer(tcpCliSock, ADDR, data)

    request = TransferProtocal_pb2.Account()
    request.account = "hrhtr4"
    request.password = "fhiuth"
    request.data = "的韩国空即是色".encode() +  b"u"*20480

    sendDataToServer(tcpCliSock, ADDR, request.SerializeToString())

    data = receiveDataFromServer(tcpCliSock, ADDR)
    tcpCliSock.send("OK".encode())
    result = TransferProtocal_pb2.ArchiveOpRes()
    result.ParseFromString(data)
    #print(str(result.hasSucceed), str(result.operation))

    tcpCliSock.close()


def testGetArchive():
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    request = TransferProtocal_pb2.RequestType()
    request.request = TransferProtocal_pb2.RequestType.GET_ARCHIVE_REQ

    data = request.SerializeToString()
    sendDataToServer(tcpCliSock, ADDR, data)

    request = TransferProtocal_pb2.Account()
    request.account = "hrhtr4"
    request.password = "fhiuth"

    sendDataToServer(tcpCliSock, ADDR, request.SerializeToString())

    data = receiveDataFromServer(tcpCliSock, ADDR)
    tcpCliSock.send("OK".encode())
    result = TransferProtocal_pb2.ArchiveOpRes()
    result.ParseFromString(data)
    #print(str(result.hasSucceed), str(result.operation),len( result.data ))

    tcpCliSock.close()


def testDeletaArchive():
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    request = TransferProtocal_pb2.RequestType()
    request.request = TransferProtocal_pb2.RequestType.DELETE_ARCHIVE_REQ

    data = request.SerializeToString()
    sendDataToServer(tcpCliSock, ADDR, data)

    request = TransferProtocal_pb2.Account()
    request.account = "hrhtr4"
    request.password = "fhiuth"

    sendDataToServer(tcpCliSock, ADDR, request.SerializeToString())

    data = receiveDataFromServer(tcpCliSock, ADDR)
    tcpCliSock.send("OK".encode())
    result = TransferProtocal_pb2.ArchiveOpRes()
    result.ParseFromString(data)
    ##print(str(result.hasSucceed), str(result.operation))

    tcpCliSock.close()


# test
# from concurrent.futures import ThreadPoolExecutor

# ThreadPool = ThreadPoolExecutor(max_workers=20)

task = [
    testRegister,
    testLogin,
    testSaveArchive,
    testGetArchive,
    testDeletaArchive,
]

import time
from threading import Thread
print("Begin\n")
start = time.clock()

for i in range (310):
    t = Thread( target=task[i%4] )
    t.start()
    t.join()
print("end   %s" , str(time.clock() - start))
# 1.001522345800621
# 1s能处理约310条请求

# i = 0
# counter = 0
# works = []
# while i < 100:
#     handler = ThreadPool.submit( task[i% len(task)] )
#     i = i+1
#     works.append(handler)
#
#     removelist = []
#     for job in works:
#         if job.done():
#             counter = counter + 1
#             removelist.append(job)
#     for job in removelist:
#         works.remove( job )
#
# #print( counter )