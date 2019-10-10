import cx_Oracle
import datetime
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
class DBUtil:
    def __init__(self,uname='system',upwd='wzz1977032719790621wlh',server='localhost',port='1521',sid='fdcpgk'):
        self.__uname=uname
        self.__upwd=upwd
        self.__server=server
        self.__port=port
        self.__sid=sid
        self.__conn=None
        self.__ReConnect()
    def __ReConnect(self):
        try:
            if not self.__conn:
                self.__conn=cx_Oracle.connect(self.__uname,self.__upwd,self.__server+':'+self.__port+'/'+self.__sid)
            else:
                pass
        except Exception as e:
            print("连接Oracle发生错误！",e)
    def __del__(self):
        if self.__conn:
            self.__conn.close()
            self.__conn=None
    def __NewCursor(self):
        try:
            cur=self.__conn.cursor()
            if cur:
                return cur
            else:
                print("#Error# GetNew Cursor Failed")
                return None
        except Exception as e:
            print("获取游标出错！",e)
    def __DelCursor(self,cur):
        if cur:
            cur.close()
    def Query(self,sql,nStart=0,nNum=-1):
        try:
            rt=[]
            cur=self.__NewCursor()
            if not cur:
                return rt
            cur.execute(sql)
            if(nStart==0) and (nNum==1):
                rt.append(cur.fetchone())
            else:
                rs=cur.fetchall()
                if nNum==-1:
                    rt.extend(rs[nStart:])
                else:
                    rt.extend(rs[nStart:nStart+nNum])
            self.__DelCursor(cur)
            return rt
        except Exception as e:
            print("查询发生错误",e)
    def Exec(self,sql):
        try:
            rt=None
            cur=self.__NewCursor()
            if not cur:
                return rt
            rt=cur.execute(sql)
            self.__conn.commit()
            self.__DelCursor(cur)
            return rt
        except Exception as e:
            print("执行SQL命令时发生错误！",e)

    def UpdateTable(self,sql):
        return self.Exec(sql)
    def GetFieldValueToSingleStrFromDb(self,fieldname,tablename,condition):
        try:
            sql="select "+fieldname+" from "+tablename+" "+condition
            rt=self.Query(sql,0,1)
            return rt[0][0]
        except Exception as e:
            print("查询单个字段值发生错误",e)
    def GetFieldValueToStrListFromDb(self,fieldname,tablename,condition):
        try:
            sql="select "+fieldname+" from "+tablename+" "+condition
            rt=self.Query(sql)
            results=[]
            for row in rt:
                results.append(row[0])
            return results
        except Exception as e:
            print("查询字段值列表发生错误")
    def GetFieldValueToStrTupleFromDB(self,fieldname,tablename,condition):
        try:
            sql="select "+fieldname+" from "+tablename+" "+condition
            rt=self.Query(sql)
            return tuple(rt)
        except Exception as e:
            print("查询字段值元组时发生错误")
    def ReadBlobToString(self,fieldname,tablename,condition):
        try:
            sql="select "+fieldname+" from "+tablename+" "+condition
            rt=self.Query(sql)
            if len(rt)>0:
                return bytes.decode(rt[0][0].read(),encoding='GBK')
            else:
                return ""
        except Exception as e:
            print("读取BLOB数据到字符串",e)

    def WriteBlob(self,fieldname,tablename,condition,content):
        try:
            sql="update "+tablename+" set "+fieldname+"=:blobData "+condition
            cur=self.__conn.cursor()
            cur.setinputsizes(blobData=cx_Oracle.BLOB)
            cur.execute(sql,{'blobData':content})
            self.__conn.commit()
            self.__DelCursor(cur)
        except Exception as e:
            print("向数据库写入BLOB时发生错误",e)
    def WriteFileToBlob(self,fieldname,tablename,condition,filename):
        try:
            file = open(filename, 'rb')
            content = file.read()
            file.close()
            self.WriteBlob(fieldname,tablename,condition,content)
        except Exception as e:
            print("向数据库写入BLOB时发生错误",e)

    def GetRowCount(self,sql):
        try:
            rt=self.Query(sql)
            if rt==None:
                return 0
            else:
                return len(rt)
        except Exception as e:
            print("获取数据表记录时发生错误",e)
    def GetRandomFieldValueToStrGroupFromDb(self,fieldname,tablename,condition,rowcount):
        try:
            sql="select distinct "+fieldname+" from (select * from "+tablename+" "+condition+" order by dbms_random.value() ) where rownum<="+rowcount
            rt=self.Query(sql)
            results=[]
            for row in rt:
                results.append(row[0])
            return results
        except Exception as e:
            print("随机获取指定数量的数据记录发生错误！",e)
    def GetRangeFieldValueToStrGroupFromDb(self,fieldname,tablename,condition,minrow,maxrow):
        try:
            oldcondition=condition
            ordercondition=''
            if condition!='':
                pos=condition.index('order')
                if pos >=0:
                    ordercondition=condition[pos:]
                    condition=condition[0:pos-1]
                    oldcondition=condition
                condition+= ' and rownum<='+str(maxrow)+" "
            else:
                condition=" where rownum<="+str(maxrow)+' '
            if oldcondition!="":
                if ordercondition=='':
                    condition+=" minus select * from (select * from "+tablename+" "+oldcondition+" "+ordercondition+") where rownum<="+str(minrow)+" "
                else:
                    condition+=" minus select * from (select * from "+tablename+" "+oldcondition+" "+ordercondition+") "+" where rownum<="+str(minrow)
            else:
                condition+=" minus select * from "+tablename+" where rownum<="+str(minrow)+" "
            result= self.GetFieldValueToStrGroupsFromDb(fieldname,tablename,condition)
            return  result
        except Exception as e:
            print("读取分页数据发生错误",e)

    def GetFieldValueToStrGroupsFromDbByRange(self,fieldname,tablename,condition,minrow,maxrow):
        try:
            fieldlist=fieldname.split(',')
            sql="select "+fieldname+" from "+tablename+" "+condition
            rt=self.Query(sql,minrow,maxrow-minrow)
            fieldcount=len(fieldlist)
            results=[]
            for c in range(0,fieldcount):
                tmpresults=[]
                for row in rt:
                    tmpresults.append(row[c])
                results.append(tmpresults)
            return results
        except Exception as e:
            print("获取多个字段值列表时发生错误！",e)


    def GetFieldValueToStrGroupsFromDb(self,fieldname,tablename,condition):
        try:
            fieldlist=fieldname.split(',')
            sql="select "+fieldname+" from "+tablename+" "+condition
            rt=self.Query(sql)
            fieldcount=len(fieldlist)
            results=[]
            for c in range(0,fieldcount):
                tmpresults=[]
                for row in rt:
                    tmpresults.append(row[c])
                results.append(tmpresults)
            return results
        except Exception as e:
            print("获取多个字段值列表时发生错误！",e)
    def GetTbjxByTBid(self,tbid):
        return self.GetFieldValueToSingleStrFromDb('BJX','XTGLK.ZLFL_MSFF_TAB',"where TBID='"+tbid+"'")
    def GetTbidByTbjx(self,tbjx):
        return self.GetFieldValueToSingleStrFromDb('TBID','XTGLK.ZLFL_MSFF_TAB',"where BJX='"+tbjx+"'")
    def GetFieldExceptMrzd(self,tbid):
        return self.GetFieldValueToStrListFromDb("MCJX","XTGLK.ZLFL_MSFF_FIELD","where TBID='"+tbid+"' and MCJX not in('FLID','ID','MJ','SJLY','SJSJ','LRSJ') order by SXH")
    def GetFieldType(self,tbid,zdmc):
        return self.GetFieldValueToSingleStrFromDb("ZDLX","XTGLK.ZLFL_MSFF_FIELD","where TBID='"+tbid+"' and MCJX='"+zdmc+"'")
    def GetFlid(self,tbid):
        return self.GetFieldValueToSingleStrFromDb("FLID","XTGLK.ZLFL_MSFF_TAB","where TBID='"+tbid+"'")
    def TestDataExist(self,sql):
        return self.GetRowCount(sql)

    def UpdateTable(self,sql):
        return self.Exec(sql)
    def GetTableRowID(self):
        b_id=self.GetFieldValueToSingleStrFromDb("rawtohex(SYS_GUID())","dual","")
        return b_id

    def InsertToTable_NotFullField(self,table,fieldnames,fieldvalues):
        try:
            tbid=self.GetTbidByTbjx(table)
            fields=self.GetFieldExceptMrzd(tbid)
            fieldlist=""
            for field in fields:
                if fieldlist=="":
                    fieldlist=field
                else:
                    fieldlist+=","+field
            fieldlist+=",FLID,ID,MJ,SJLY,SJSJ,LRSJ"


            fieldcount=len(fields)
            sqlText='insert into '+table+'('+fieldlist+') values('
            for fc in range(0,fieldcount):
                fieldname=fields[fc]

                if fieldname not in fieldnames:

                    fieldtype=self.GetFieldType(tbid,fieldname)
                    fieldvalue=''
                    if fieldtype=="数字":
                        if fieldvalue=='':
                            fieldvalue='0'
                    else:
                        if fieldtype=="日期" or fieldtype=="数字":
                            if fieldvalue.index("to_date")<0 and fieldvalue!="":
                                fieldvalue='to_date(\''+fieldvalue+'\',\'YYYY/MM/DD HH24:MI:SS\')'
                            else:
                                fieldvalue='to_date(\'1000-01-01\',\'YYYY/MM/DD HH24:MI:SS\')'
                        else:
                            if fieldtype=="文本":
                                fieldvaue=self.GetFieldValueToSingleStrFromDb("MRZ","XTGLK.ZLFL_MSFF_FIELD_INFO","where TBID='"+tbid+"' and ZDMC='"+fieldname+"'")
                            else:
                                if fieldvalue=="":
                                    fieldvalue='N\'aa\''
                    includeDate=fieldvalue.find('to_date')
                    if fieldvalue!="N'aa'" and includeDate==-1 and fieldtype!='数字':
                        if fc==0:
                            sqlText+='\''+fieldvalue+'\''
                        else:
                            sqlText+=',\''+fieldvalue+'\'';
                    else:
                        if fc==0:
                            sqlText+=fieldvalue
                        else:
                            sqlText+=","+fieldvalue
                else:
                    index=fieldnames.index(fieldname)
                    fieldvalue=fieldvalues[index]
                    fieldtype=self.GetFieldType(tbid,fieldname)

                    if fieldtype=="数字":
                        if fieldvalue=="":
                            fieldvalue="0"
                    else:
                        if fieldtype=="日期" or fieldtype=="数字":
                            if fieldvalue.index("to_date")<0 and fieldvalue!="":
                                fieldvalue="to_date('"+fieldvalue+"','YYYY/MM/DD HH24:MI:SS')"
                            else:
                                fieldvalue="to_date('1000-01-01','YYYY/MM/DD HH24:MI:SS')"
                        else:
                            if fieldtype=="文本":
                                pass
                            else:
                                if fieldvalue=="":
                                    fieldvalue="N'aa'"
                    includeDate=fieldvalue.find('to_date')
                    if fieldvalue!="N'aa'" and includeDate==-1 and fieldtype!='数字':
                        if fc==0:
                            sqlText+='\''+fieldvalue+'\''
                        else:
                            sqlText+=',\''+fieldvalue+'\'';
                    else:
                        if fc==0:
                            sqlText+=fieldvalue
                        else:
                            sqlText+=","+fieldvalue
            flid=self.GetFlid(tbid)
            id=self.GetTableRowID()
            mj='内部资料'
            sjly='用户输入'
            sjsj=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            lrsj=sjsj
            sqlText+=",'"+flid+"'"
            sqlText+=",'"+id+"'"
            sqlText+=",'"+mj+"'"
            sqlText+=",'"+sjly+"'"
            sqlText+=",to_date('"+sjsj+"','YYYY/MM/DD HH24:MI:SS')"
            sqlText+=",to_date('"+lrsj+"','YYYY/MM/DD HH24:MI:SS')"
            sqlText+=")"

            rt=self.Exec(sqlText)
            dataExist=self.TestDataExist("select * from "+table+" where ID='"+id+"'")
            if  dataExist>0:
                return id
            else:
                return ""
        except Exception as e:
            print("向数据库中插入部分字段数据时发生错误",e)

    def InsertToOracle(self, table, fieldvaluelist):
        try:
            fieldnames = []
            fieldtypes = []
            tbid = self.GetTbidByTbjx(table)
            fieldnames = self.GetFieldExceptMrzd(tbid)
            flid = self.GetFlid(tbid)
            fieldcount = len(fieldnames)

            fieldlist = ""
            for field in fieldnames:
                if fieldlist == "":
                    fieldlist = field
                else:
                    fieldlist += "," + field
            fieldlist += ",FLID,ID,MJ,SJLY,SJSJ,LRSJ"

            sqlText = "insert into " + table+"("+fieldlist+ ") values("

            for fc in range(0,fieldcount):
                fieldname = fieldnames[fc]
                fieldvalue = fieldvaluelist[fc]
                fieldtype = self.GetFieldType(tbid, fieldname)
                if fieldtype == "数字":
                    if fieldvalue == "":
                        fieldvalue = "0"
                else:
                    if fieldtype == "日期" or fieldtype == "数字":
                        if fieldvalue.index("to_date") < 0 and fieldvalue != "":
                            fieldvalue = "to_date('" + fieldvalue + "','YYYY/MM/DD HH24:MI:SS')"
                        else:
                            fieldvalue = "to_date('1000-01-01','YYYY/MM/DD HH24:MI:SS')"
                    else:
                        if fieldtype == "文本":
                            pass
                        else:
                            if fieldvalue == "":
                                fieldvalue = "N'aa'"
                includeDate = fieldvalue.find('to_date')
                if fieldvalue != "N'aa'" and includeDate == -1 and fieldtype != '数字':
                    if fc == 0:
                        sqlText += '\'' + fieldvalue + '\''
                    else:
                        sqlText += ',\'' + fieldvalue + '\'';
                else:
                    if fc == 0:
                        sqlText += fieldvalue
                    else:
                        sqlText += "," + fieldvalue

            id = self.GetTableRowID()
            mj = '内部资料'
            sjly = '用户输入'
            sjsj = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            lrsj = sjsj
            sqlText += ",'" + flid + "'"
            sqlText += ",'" + id + "'"
            sqlText += ",'" + mj + "'"
            sqlText += ",'" + sjly + "'"
            sqlText += ",to_date('" + sjsj + "','YYYY/MM/DD HH24:MI:SS')"
            sqlText += ",to_date('" + lrsj + "','YYYY/MM/DD HH24:MI:SS')"
            sqlText += ")"

            rt = self.Exec(sqlText)

            dataExist = self.TestDataExist("select * from "+table+" where ID='" + id + "'")
            if dataExist > 0:
                return id
            else:
                return ""
        except Exception as e:
            print("向数据库插入全部字段值时发生错误",e)
    









