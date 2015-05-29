#!/usr/bin/python
#coding=gbk

import tornado.web, tornado.ioloop
import motor
import snappy
import traceback
from ProtoMessage_pb2 import HttpPacket,IpPacket,EmailPacket,WhiteProcess
from bson.objectid import ObjectId
import time,datetime
from time import mktime

class WhiteUpdateHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('not get')

    @tornado.web.asynchronous
    def post(self):
        print "start"
        latesttime = self.get_argument("time");
        print latesttime
        try:
            latestaddtime = datetime.datetime.strptime(latesttime,"%Y-%m-%d %H:%M:%S")
        except:
            latestaddtime = 0
        print latestaddtime

        md5str = ""
        db = self.settings['db']
        if latestaddtime:
            db.white_process.find({"addtime":{'$gt':latestaddtime}}).sort([('addtime', 1)]).each(self._get_md5)       
        else:
            db.white_process.find().sort([('addtime', 1)]).each(self._get_md5)

    def _get_md5(self,md5,error):
        if error:
            raise tornado.web.HTTPError(500, error)
        elif md5:
            print md5
            md5time = md5["addtime"]
            md5obj = WhiteProcess()
            md5obj.processname = md5["processname"]
            addtime = md5time.strftime("%Y-%m-%d %H:%M:%S") 
            md5obj.addtime = addtime
            md5obj.processmd5 = md5["md5"]
            md5obj.version = md5["version"]
            protobufmd5 = md5obj.SerializeToString()
            print protobufmd5
            print len(protobufmd5)
            self.write("%s!!!"%protobufmd5)
        else:
            print "finish"
            self.write("")
            self.finish()

class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("not get")

    def saveipdata(self,ipobj,userid,pcid):
        print "ip save\n",ipobj
        try:
            datatimestruct =  time.strptime(ipobj.datatime, "%Y-%m-%d %H:%M:%S")
            datetimeobj = datetime.fromtimestamp(mktime(datatimestruct))
        except:
            datetimeobj = datetime.datetime.now()

        self.settings['db'].res_ip.insert(
        {
            "sip" : ipobj.sip, 
            "user_id" : ObjectId(userid), 
            "protocol": ipobj.protocoltype,
            "iptype" : "0", 
            "flow" : ipobj.flow, 
            "pc_id" : ObjectId(pcid),
            "iswhite" : False, 
            "datetime" : datetimeobj, 
            "riskvalue" : -1, 
            "dport" : ipobj.dport, 
            "sport" : ipobj.sport, 
            "dip" : ipobj.dip,
            "processname":ipobj.processname,
            "processmd5":ipobj.processmd5,
            "length":ipobj.length
        }, callback=self._on_response
        )
        print "ip save ok"

    def savehttpdata(self,httpobj,userid,pcid):
        print "httpobj\n",httpobj
        try:
            datetimestruct =  time.strptime(ipobj.datetime, "%Y-%m-%d %H:%M:%S")
            datetimeobj = datetime.fromtimestamp(mktime(datetimestruct))
        except:
            datetimeobj = datetime.datetime.now()

        self.settings['db'].res_url.insert(
        {
            "sip" : httpobj.sip, 
            "user_id" : ObjectId(userid), 
            "url" : httpobj.httpurl, 
            "riskvalue" : -1, 
            "datetime" : datetimeobj, 
            "pc_id" : ObjectId(pcid), 
            "iswhite" : False, 
            "dport" : httpobj.dport, 
            "urltype" : "0", 
            "sport" : httpobj.sport, 
            "dip" : httpobj.dip,
            "processname":httpobj.processname,
            "processmd5":httpobj.processmd5
        }, callback=self._on_response
        )
        print "http save ok"

    def saveemaildata(self,emailobj,userid,pcid):
        try:
            datetimestruct =  time.strptime(emailobj.datetime, "%Y-%m-%d %H:%M:%S")
            datetimeobj = datetime.fromtimestamp(mktime(datetimestruct))
        except:
            datetimeobj = datetime.datetime.now()
        print emailobj
        if emailobj.sendfrom.find("@")==-1:
            return
        self.settings['db'].res_email.insert(
        {

            "sendbcc" : emailobj.sendbcc.replace(";",""), 
            "sip" : emailobj.sip, 
            "user_id" : ObjectId(userid), 
            "sendfrom" : emailobj.sendfrom.replace(";",""), 
            "riskvalue" : -1, 
            "datetime" : datetimeobj, 
            "pc_id" : ObjectId(pcid), 
            "sendcc" : emailobj.sendcc.replace(";",""), 
            "sendto" : emailobj.sendto.replace(";",""), 
            "dport" : emailobj.dport, 
            "iswhite" : False, 
            "sport" : emailobj.sport, 
            "dip" : emailobj.dip, 
            "subject" : emailobj.subject, 
            "emailtype" : "0", 
            "processname":emailobj.processname,
            "processmd5":emailobj.processmd5
        }, callback=self._on_response
        )
        print "email save ok"

    @tornado.web.asynchronous
    def post(self):
        """Insert a message
        """
        # print self.request.body
        print "get message"
        userid = self.get_argument("userid")
        pcid = self.get_argument("pcid")
        packettype = self.get_argument("type")
        pos = self.request.body.find("&data=")

        if pos==-1:
            self.write('error')
            self.finish()
            return

        snappydata = self.request.body[pos+6:]

        try:
            protodata=snappy.uncompress(snappydata)
            for package in protodata.split("!!!"):

                if len(package) < 10:
                    continue
                if packettype == "1":
                    packetobj = IpPacket()
                    packetobj.ParseFromString(package)
                    self.saveipdata(packetobj,userid,pcid)
                elif packettype == "2":
                    packetobj = EmailPacket()
                    packetobj.ParseFromString(package)
                    self.saveemaildata(packetobj,userid,pcid)
                elif packettype == "3":
                    packetobj = HttpPacket()
                    packetobj.ParseFromString(package)
                    self.savehttpdata(packetobj,userid,pcid)
        except:
            print "error"
            print "print self.request.body",self.request.body
            print "self.request.arguments",self.request.arguments
            traceback.print_exc()
            self.write('ok')
            self.finish()
            return
            
        self.write('ok')
        self.finish()

    def _on_response(self, result, error):
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            pass
            # self.write('ok')
            # print "_on_response ok"
            # self.finish()

class GetPcIDHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("please use post to send data")

    @tornado.web.asynchronous
    def post(self):
        """Insert a message
        """
        print self.request.body

        self.userid = self.get_argument("userid")
        self.mac = self.get_argument("mac")

        db = self.settings['db']
        db.userpc.find_one({"pcid":self.mac,"user_id":ObjectId(self.userid)},callback=self._got_pc)
        
    def _got_pc(self, pc, error):
        if error:
            print "error"
            raise tornado.web.HTTPError(500, error)
        elif pc:
            print "get id"
            self.write(str(pc["_id"]))
            print str(pc["_id"])
            self.finish()
        else:
            print "insert id"
            self.settings['db'].userpc.insert(
            {
                "pcname" : self.mac, 
                "pcid" : self.mac, 
                "user_id" : ObjectId(self.userid), 
                "addtime" : datetime.datetime.now(), 
                }, callback=self._create_userpc
            )
            self.finish()

    def _create_userpc(self, result, error):
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            print "create error"
            self.write(str(result))
            # self.finish()


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""<html><body>
        <form action="/upload/mobile/file/" enctype="multipart/form-data" method="post">
        <p>File: <input type="file" name="file1_516641de2de2bf1bbe5611b9"></p>
        <p><input type="submit" value="Submit"></p>
        </form>
        </body></html>""")

    def post(self):
        # self.set_header("Content-Type", "text/plain")
        bodylist = self.request.body.split("\r\n")
        namelist = ""
        for tmp in bodylist: 
            if tmp.startswith("Content-Disposition:"):
                namelist = tmp.split(";")
                break 
        user = namelist[1].split('"')[1]
        userid = user.split("_")[1].strip()
        filename = namelist[2].split('"')[1]
        filelist = self.request.files[user][0]["body"].strip().split("\r\n")
        print "filelist",filelist
        if filename.find("net_behaviour.txt")!=-1:
            for data in filelist:
                try:
                    fdict={} 
                    fdict["user_id"] = ObjectId(userid)
                    strtick = data.split("]")[0].split("[")[1].strip()
                    fdict["tick"] = float(strtick)
                    strlevel = data.split(strtick)[0].split("<")[1].split(">")[0]
                    fdict["level"] = int(strlevel)
                    fdict["datetime"] = datetime.datetime.strptime(data.split("<")[0].strip(),"%Y-%m-%d %H:%M:%S")
                    detail = data.split("]")[1].strip()
                    detaillist = detail.split(":")
                    fdict["sip"] = detaillist[1]
                    fdict["dip"] = detaillist[3]
                    fdict["riskvalue"] = -1
                    fdict["flow"] = "0"
                    if (len(detaillist)!=4):
                        fdict["version"] = detaillist[4]
                        fdict["transfprotc"] = detaillist[5]
                        fdict["appprotc"] = detaillist[6]
                        fdict["nettype"] = detaillist[7]
                        content = detail.split("%s:"%fdict["nettype"])[1].strip()
                        fdict["content"] = content
                        print "fdict",fdict 
                    else:
                        fdict["version"] = ""
                        fdict["transfprotc"] = ""
                        fdict["appprotc"] = "IP"
                        fdict["nettype"] = ""
                        fdict["content"] = ""
                        print "fdict",fdict
                    self.settings['db'].net_behaviour.insert(
                          fdict,
                          callback=self._on_response)
                except:
                    traceback.print_exc()
                    self.write("failed")
                    self.finish()
                    return 
        elif filename.find("driver_behaviour.txt")!=-1: 
            for data in filelist: 
                try:
                    fdict = {}
                    fdict["user_id"] = ObjectId(userid)
                    datalist = data.split("\t")
                    datetimestr = datalist[0]
                    intindex = 0
                    for index,i in enumerate(datetimestr):
                        if i.isdigit():
                            intindex = index
                            break
                    datetimestr = datetimestr[intindex:]
                    print datetimestr
                    fdict["datetime"] = datetime.datetime.strptime(datetimestr,"%Y-%m-%d %H:%M:%S") 
                    fdict["driver"] = datalist[1] 
                    fdict["dritype"] = datalist[2]
                    fdict["program"] = datalist[3]
                    fdict["flow"] = datalist[4].split(":")[0]
                    fdict["commnum"] = datalist[4].split(":")[1]
                    if fdict["driver"]=="sms":
                        smscontent = data.split("sms_content:")[1]
                        utf8smscontent = smscontent  #.decode('gbk').encode('utf8')
                        fdict["smscontent"] = utf8smscontent
                    else:
                        fdict["smscontent"] = ""
                    fdict["riskvalue"] = -1
                    fdict["flow"] = 1
                    print "fdict",fdict
                    self.settings['db'].driver_behaviour.insert(
                          fdict,
                          callback=self._on_response)
                except:
                    traceback.print_exc()
                    self.write("failed!")
                    self.finish()
                    return
        self.write("ok")
        self.finish()
    def _on_response(self, result, error):
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            pass  

# db = motor.MotorClient('221.2.164.60', 27017).open_sync().InfoSecurity
db = motor.MotorClient('192.168.0.234', 27017).open_sync().InfoSecurity

application = tornado.web.Application([
        (r'/get/pc/addtime/', WhiteUpdateHandler),
        (r'/put/pc/packets/', MessageHandler),
        (r'/get/pc/pcid/', GetPcIDHandler),
        (r'/upload/mobile/file/',UploadFileHandler)
    ], db=db
)

application.listen(8080)
print 'Listening on http://localhost:8080'
tornado.ioloop.IOLoop.instance().start()
