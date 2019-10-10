import string
class StringUtil:
    @staticmethod
    def ChangeListToString(myList):
        delimiter=','
        return delimiter.join(myList)

    @staticmethod
    def ChangeListToCondition(fieldname,myList):
        result=""
        for item in myList:
            if result=="":
                result+="'"+item+"'"
            else:
                result+=",'"+item+"'"
        if len(myList)==1:
            result=" "+fieldname+"="+result
        elif len(myList)>1:
            result=" "+fieldname+" in ("+result+")"
        else:
            result=""
        return result
    @staticmethod
    def OnlyCharNum(s):
        s2=s.lower()
        format='abcdefghijklmnopqrstuvwxyz0123456789'
        for c in s2:
            if not c in format:
                s=s.replace(c,'')
        return s

    @staticmethod
    def getPinyin(string):
        if string == None:
            return None
        lst = list(string)
        charLst = []
        for l in lst:
            firstChar = ''
            if l=='1' or l=='2' or l=='3' or l=='4' or l=='5' or l=='6' or l=='7' or l=='8' or l=='9' or l=='0':
                firstChar=l
            elif  l in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                firstChar=l.upper()
            elif l in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S','T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                firstChar = l
            else:
                str1 = l.encode('gbk')
                try:
                    ord(str1)
                    firstChar=str1
                except:
                    asc = str1[0] * 256 + str1[1] - 65536
                    if asc >= -20319 and asc <= -20284:
                        firstChar= 'A'
                    elif asc >= -20283 and asc <= -19776:
                        firstChar = 'B'
                    elif asc >= -19775 and asc <= -19219:
                        firstChar = 'C'
                    elif asc >= -19218 and asc <= -18711:
                        firstChar = 'D'
                    elif asc >= -18710 and asc <= -18527:
                        firstChar = 'E'
                    elif asc >= -18526 and asc <= -18240:
                        firstChar = 'F'
                    elif asc >= -18239 and asc <= -17923:
                        firstChar = 'G'
                    elif asc >= -17922 and asc <= -17418:
                        firstChar = 'H'
                    elif asc >= -17417 and asc <= -16475:
                        firstChar = 'J'
                    elif asc >= -16474 and asc <= -16213:
                        firstChar = 'K'
                    elif asc >= -16212 and asc <= -15641:
                        firstChar = 'L'
                    elif asc >= -15640 and asc <= -15166:
                        firstChar = 'M'
                    elif asc >= -15165 and asc <= -14923:
                        firstChar = 'N'
                    elif asc >= -14922 and asc <= -14915:
                        firstChar = 'O'
                    elif asc >= -14914 and asc <= -14631:
                        firstChar = 'P'
                    elif asc >= -14630 and asc <= -14150:
                        firstChar = 'Q'
                    elif asc >= -14149 and asc <= -14091:
                        firstChar = 'R'
                    elif asc >= -14090 and asc <= -13119:
                        firstChar = 'S'
                    elif asc >= -13118 and asc <= -12839:
                        firstChar = 'T'
                    elif asc >= -12838 and asc <= -12557:
                        firstChar = 'W'
                    elif asc >= -12556 and asc <= -11848:
                        firstChar = 'X'
                    elif asc >= -11847 and asc <= -11056:
                        firstChar = 'Y'
                    elif asc >= -11055 and asc <= -10247:
                        firstChar = 'Z'
                    else:
                        firstChar = '_'
            charLst.append(firstChar)
        return ''.join(charLst)



