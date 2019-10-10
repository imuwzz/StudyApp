import sqlite3
class SqliteUtil:
    @staticmethod
    def CreateDB(db):
        try:
            conn = sqlite3.connect(db)
            conn.close()
        except Exception as e:
            print("创建数据库失败！",e)
    @staticmethod
    def Exec(db,sql):
    #执行SQL语句
        try:
            conn=sqlite3.connect(db)
            conn.execute(sql)
            conn.commit()
            conn.close()
            print('创建成功')
        except Exception as e:
            print('执行sql语句发生错误')

    @staticmethod
    def Query(db,sql,nStart=0,nNum=-1):
        try:
            rt=[]
            conn = sqlite3.connect(db)
            cur=conn.execute(sql)
            if(nStart==0) and (nNum==1):
                rt.append(cur.fetchone())
            else:
                rs=cur.fetchall()
                if nNum==-1:
                    rt.extend(rs[nStart:])
                else:
                    rt.extend(rs[nStart:nStart+nNum])
            conn.close()
            return rt
        except Exception as e:
            print("查询发生错误",e)

    @staticmethod
    def GetTablesInDB(db):
        return SqliteUtil.Query(db,"SELECT name FROM sqlite_master WHERE type='table' order by name")


