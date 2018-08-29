import math
import socket
from time import ctime

from Config import Config
from LoggerServer.Logger import Log

from BusicnessLayer.GameBusicness import GameBusicness

from Protocal.generate import TransferProtocal_pb2

####################### configuration ############################
BufferSize = Config.BufferSize
MaxDelayTime = Config.MaxDelayTime


def ReceiveDataFromClient(client, address):
    data = b''
    while True:
        buf = client.recv(BufferSize)
        data = data + buf
        if len(buf.strip(b' ')) < BufferSize:
            break
    data = data.strip(b' ')
    Log("[%s] : Receive from [ %s:%i ] . MsgSize : %i" % (ctime(), address[0], address[1], len(data)))
    return data


def SendDataToClient(client, address, data):
    Log("[%s] : Send to [ %s:%i ] . MsgSize : %i" % (ctime(), address[0], address[1], len(data)))
    data = data + (BufferSize - len(data) % BufferSize) * b" "
    pieces = len(data) // BufferSize
    for i in range(pieces):
        client.send(data[i * BufferSize: (i + 1) * BufferSize])


def SendReplyCode(client, resType):
    Reply = TransferProtocal_pb2.ResultType()
    Reply.result = resType
    client.send(Reply.SerializeToString())


def OnDeleteArchiveRequest(client, address, gameLogic):
    Log("[%s] : [ %s:%i ] request deleteArchive." % (ctime(), address[0], address[1]))
    data = ReceiveDataFromClient(client, address)
    accountData = TransferProtocal_pb2.Account()
    accountData.ParseFromString(data)
    res = gameLogic.DeleteArchive(accountData.account)
    # SendReplyCode(client, TransferProtocal_pb2.ResultType.DELETE_ARCHIVE_RES)
    # Log("[%s] : Send to [ %s:%i ] . Msg : reply code[deleteArchiveRes]." % (ctime(), address[0], address[1]))
    Reply = TransferProtocal_pb2.ArchiveOpRes()
    Reply.operation = TransferProtocal_pb2.ArchiveOpRes.DELETE
    if res:
        Reply.hasSucceed = True
    else:
        Reply.hasSucceed = False
    SendDataToClient(client, address, Reply.SerializeToString())
    client.recv(BufferSize)


def OnGetArchiveRequest(client, address, gameLogic):
    Log("[%s] : [ %s:%i ] request getArchive." % (ctime(), address[0], address[1]))
    data = ReceiveDataFromClient(client, address)
    accountData = TransferProtocal_pb2.Account()
    accountData.ParseFromString(data)
    res = gameLogic.GetArchive(accountData.account)
    # SendReplyCode(client, TransferProtocal_pb2.ResultType.GET_ARCHIVE_RES)
    # Log("[%s] : Send to [ %s:%i ] . Msg : reply code[getArchiveRes]." % (ctime(), address[0], address[1]))
    Reply = TransferProtocal_pb2.ArchiveOpRes()
    Reply.operation = TransferProtocal_pb2.ArchiveOpRes.GET
    if res[0]:
        Reply.hasSucceed = True
        Reply.data = res[1]
    else:
        Reply.hasSucceed = False
    SendDataToClient(client, address, Reply.SerializeToString())
    client.recv(BufferSize)


def OnSaveArchiveRequest(client, address, gameLogic):
    Log("[%s] : [ %s:%i ] request saveArchive." % (ctime(), address[0], address[1]))
    data = ReceiveDataFromClient(client, address)
    accountData = TransferProtocal_pb2.Account()
    accountData.ParseFromString(data)
    res = gameLogic.SaveArchive(accountData.account, accountData.data)
    # SendReplyCode(client, TransferProtocal_pb2.ResultType.SAVE_ARCHIVE_RES)
    # Log("[%s] : Send to [ %s:%i ] . Msg : reply code[saveArchiveRes]." % (ctime(), address[0], address[1]))
    Reply = TransferProtocal_pb2.ArchiveOpRes()
    Reply.operation = TransferProtocal_pb2.ArchiveOpRes.ADD
    if res:
        Reply.hasSucceed = True
    else:
        Reply.hasSucceed = False
    SendDataToClient(client, address, Reply.SerializeToString())
    client.recv(BufferSize)


def OnLoginRequest(client, address, gameLogic):
    Log("[%s] : [ %s:%i ] request login." % (ctime(), address[0], address[1]))
    data = ReceiveDataFromClient(client, address)
    accountData = TransferProtocal_pb2.Account()
    accountData.ParseFromString(data)
    res = gameLogic.LogIn(accountData.account, accountData.password)
    # SendReplyCode(client, TransferProtocal_pb2.ResultType.LOGIN_RES)
    # Log("[%s] : Send to [ %s:%i ] . Msg : reply code[loginRes]." % (ctime(), address[0], address[1]))
    Reply = TransferProtocal_pb2.LoginRes()
    if res[0]:
        Reply.hasSucceed = True
    else:
        Reply.hasSucceed = False
        if res[1] == 1:
            Reply.error = TransferProtocal_pb2.LoginRes.INVALIDATED_PASSWORD
        else:
            Reply.error = TransferProtocal_pb2.LoginRes.INVALIDATED_ACCOUNT
    SendDataToClient(client, address, Reply.SerializeToString())
    client.recv(BufferSize)


def OnRegisterRequest(client, address, gameLogic):
    Log("[%s] : [ %s:%i ] request register." % (ctime(), address[0], address[1]))
    data = ReceiveDataFromClient(client, address)
    accountData = TransferProtocal_pb2.Account()
    accountData.ParseFromString(data)
    res = gameLogic.Register(accountData.account, accountData.password)
    # #SendReplyCode(client, TransferProtocal_pb2.ResultType.REGISTER_RES)
    # #Log("[%s] : Send to [ %s:%i ] . Msg : reply code[registerRes]." % (ctime(), address[0], address[1]))
    Reply = TransferProtocal_pb2.RegisterRes()
    if res:
        Reply.hasSucceed = True
    else:
        Reply.hasSucceed = False
        Reply.error = TransferProtocal_pb2.RegisterRes.USER_EXIT
    SendDataToClient(client, address, Reply.SerializeToString())
    client.recv(BufferSize)


ServiceAvailable = \
    {
        TransferProtocal_pb2.RequestType.REGISTER_REQ: OnRegisterRequest,
        TransferProtocal_pb2.RequestType.LOGIN_REQ: OnLoginRequest,
        TransferProtocal_pb2.RequestType.SAVE_ARCHIVE_REQ: OnSaveArchiveRequest,
        TransferProtocal_pb2.RequestType.GET_ARCHIVE_REQ: OnGetArchiveRequest,
        TransferProtocal_pb2.RequestType.DELETE_ARCHIVE_REQ: OnDeleteArchiveRequest,
    }


def RequestProcess(client, address, DBHandlerIndex, HandlerPool):
    try:
        gameLogic = GameBusicness(HandlerPool[DBHandlerIndex])

        # 设置超时时间
        client.settimeout(MaxDelayTime)
        # 接收数据的大小
        buf = client.recv(BufferSize)

        request = TransferProtocal_pb2.RequestType()
        request.ParseFromString(buf.strip(b' '))

        service = ServiceAvailable[request.request]
        service(client, address, gameLogic)
    # 超时后退出
    except socket.timeout:
        Log('[%s] : [ %s:%i ] time out' % (ctime(), address[0], address[1]))
    except ConnectionResetError:
        Log('[%s] : [ %s:%i ] actively disconnected' % (ctime(), address[0], address[1]))
    except Exception:
        Log('[%s] : [ %s:%i ] unknow error happened' % (ctime(), address[0], address[1]))
    finally:
        # 关闭与客户端的连接
        client.close()
