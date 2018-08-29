class GameBusicness:
    def __init__(self, DBHandler):
        self.handler = DBHandler[0]
        self.mutex   = DBHandler[1]

    def Register(self, Account, Password):
        self.mutex.acquire()
        PlayerNum = self.handler.HasPlayer(Account)
        self.mutex.release()
        if PlayerNum == 0:
            self.mutex.acquire()
            Res = self.handler.AddPlayer(Account, Password)
            self.mutex.release()
            if Res:
                return True
        return False

    def LogIn(self, Account, Password):
        self.mutex.acquire()
        PlayerNum = self.handler.IsValidAccount(Account, Password)
        self.mutex.release()
        if PlayerNum == 1:
            return True,1
        self.mutex.acquire()
        IsAccountExist = self.handler.HasPlayer( Account )
        self.mutex.release()
        return False,IsAccountExist

    def SaveArchive(self, Account, Archive):
        if isinstance( Archive ,type(b'')):
            Archive = Archive.decode()
        self.mutex.acquire()
        res = self.handler.AddArchive(Account, Archive)
        self.mutex.release()
        return res

    def GetArchive(self, Account):
        self.mutex.acquire()
        res = self.handler.GetArchive(Account)
        self.mutex.release()
        return res[0] != None and len(res[0]) != 0, res[0]

    def DeleteArchive(self, Account):
        self.mutex.acquire()
        res = self.handler.AddArchive(Account, "")
        self.mutex.release()
        return res

'''
# test
from minigame.DataPersistenceLayer.DataPersistenceLayer import Database

IP = "localhost"
Account = "client"
Password = "password"
DatabaseName = "minigame"
db = Database()
db.connect(IP, Account, Password, DatabaseName)

User = "4125899"
Pwd = "1234561"
gb = GameBusicness(db)
testRegister = gb.Register(User, Pwd)
testLogin = gb.LogIn(User, Pwd)
testGetArchive = gb.GetArchive(User)
testSaveArchive = gb.SaveArchive(User, 'ui' * 100)
testGetArchive = gb.GetArchive(User)
testDeleteArchive = gb.DeleteArchive(User)

db.destroy()
'''
