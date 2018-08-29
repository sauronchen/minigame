import pymysql


class Database:
    def Connect(self, ip, user, password, database):
        self.db = pymysql.connect(ip, user, password, database)

        if not self.db:
            return False

        self.cursor = self.db.cursor()
        # 创建user表
        self.cursor.execute('''
                    create table if not exists User(  
                    account     char(20)    not null primary key , 
                    password    varchar(10) not null, 
                    archive     blob        default null 
        )''')
        return True

    def HasPlayer(self, account):
        sql = '''select  count( account )  
               from    User
               where   account = '%s' 
        ''' % account
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return int(res[0])

    def AddPlayer(self, account, password):
        sql = '''insert into User( account,password )
               values ( '%s','%s' )
        ''' % (account, password)
        return self.execWrite(sql)

    def AddArchive(self, account, archive):
        sql = '''update  User
               set     archive = '%s'
               where   account = '%s'  
            ''' % ( archive, account)
        return self.execWrite(sql)

    def GetArchive(self, account):
        sql = '''select  archive
               from    User
               where   account = '%s'
            ''' % account
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def IsValidAccount(self, account, password):
        sql = '''select  count( account )  
               from    User
               where   account = '%s'  and password = '%s'
            ''' % (account, password)
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return int(res[0])

    def execWrite(self, sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            return False

    def Destroy(self):
        self.db.close()


'''
# test
IP = "localhost"
Account = "client"
Password = "password"
DatabaseName = "minigame"
db = Database()
db.connect(IP, Account, Password, DatabaseName)

testHasPlayer = db.HasPlayer("4122121")
testIsValidAccount = db.IsValidAccount("5454653", "546846")
testAddPlayer = db.AddPlayer("412536", "111000")
testAddArchive = db.AddArchive("412536", "d" * 1024)
testGetArchive = db.GetArchive("412536")

db.close()
'''
