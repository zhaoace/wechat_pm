#-*- coding: UTF-8 -*-
import web
import sha
import xml.etree.ElementTree as ET
import xmltodict
import json

urls = (
    '/', 'index'
)


class index:

    def GET(self):
        user_data = web.input()
        token = "Token"

        if len(user_data) == 0:
            return "No input"

        l = []
        l.append(token)
        l.append(user_data.timestamp)
        l.append(user_data.nonce)

        l.sort()
        tempStr = "".join(l)
        tempSha = sha.new(tempStr).hexdigest()

        print " signature = ", user_data.signature
        print " tempStr = ", tempStr
        print " tempSha = ", tempSha

        if tempSha == user_data.signature:
            print "Verify successed ! \n"
            return user_data.echostr
        else:
            print "Verify failed ! \n"
            return False

    def POST(self):
        print "---- POST start ---"
        user_data = web.data()
        root = ET.fromstring(user_data)

        xmlStr = u"""
<xml>
<ToUserName><![CDATA[gh_d831d64110df]]></ToUserName>
<FromUserName><![CDATA[ooxuejulxS-Px0LDk77jFSCLXbf0]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[你好，旅行者！]]></Content>
</xml>
"""

        dic_xml = xmltodict.parse(xmlStr)
        json_res = json.dumps(dic_xml)
        # print user_data
        # print root.find("ToUserName").text
        print "json_res=", json_res
        print "---- POST end ---"
        return "success"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
