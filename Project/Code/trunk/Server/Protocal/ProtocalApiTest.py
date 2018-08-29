# test

from Protocal.generate import TransferProtocal_pb2

request = TransferProtocal_pb2.RequestType()
request.request = TransferProtocal_pb2.RequestType.REGISTER_REQ
data = request.SerializeToString()

result = TransferProtocal_pb2.ResultType()
result.result = TransferProtocal_pb2.ResultType.REGISTER_RES


account = TransferProtocal_pb2.Account()
account.account = "dfsefefsf"
account.password = "feewgrgerg"
account.data = "gdrlgrjmijgg的距离高考家里人".encode()

registerRes = TransferProtocal_pb2.RegisterRes()
registerRes.hasSucceed = True
registerRes.error = TransferProtocal_pb2.RegisterRes.INVALIDATED_ACCOUNT

archiveOp = TransferProtocal_pb2.ArchiveOpRes()
archiveOp.hasSucceed = False
archiveOp.operation = TransferProtocal_pb2.ArchiveOpRes.ADD
archiveOp.data = "dijgim规模i然后554632".encode()


