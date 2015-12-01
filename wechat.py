#-*- coding: UTF-8 -*-
import logging
import sha
import xmltodict
import json
import pymongo
import urllib2
import yaml
import random
import xml.etree.ElementTree as ET


tables = range(1, 100)


def verify(user_data, token):
    logging.warning("wechat.verify -- user_data:%s, token:%s",
                    user_data, token)
    l = []
    l.append(token)
    l.append(user_data.timestamp)
    l.append(user_data.nonce)
    l.sort()
    tempStr = "".join(l)
    tempSha = sha.new(tempStr).hexdigest()
    if tempSha == user_data.signature:
        print "Verify successed ! \n"
        return user_data.echostr
    else:
        print "Verify failed ! \n"
        return False


def xml_string_to_json(xml_str):
    dic_xml = xmltodict.parse(xml_str)
    json_res = json.dumps(dic_xml)
    logging.warning("wechat.xml_string_to_json -- %s, %s", xml_str, json_res)
    return json_res


def read_post_content(user_data):
    root =  ET.fromstring(user_data)
    content = root.find("Content").text.strip()
    return content


def register_sid(wechat_id, splunk_id):
    pass


def arrange_table(wechat_id):
    # table = random.randint(1, 90)
    table = random.choice(tables)
    print "=========="
    print tables

    tables.remove(table)
    print tables
    print len(tables)
    print "=========="

    return table


def lucky_draw():
    current = pymongo.MongoClient().splunkers.current
    lucky_one = current.find()
    return lucky_one


def add_splunker(splunk_id, name="None"):
    current = pymongo.MongoClient().splunkers.current
    if current.find({"splunk_id": splunk_id}).count() == 0:
        current.insert({"splunk_id": splunk_id, "name": name})
    else:
        raise Exception("Splunk id is existing")


def get_client_credential():
    with open("tmp/conf.yaml") as f:
        y = yaml.load(f)
        s = urllib2.urlopen(y["credential_url"]).read()
        j = json.loads(s)
        return j['access_token']


if __name__ == "__main__":
    # print get_client_credential()
    # logging.warning("Set table: %s", arrange_table("wid12321321"))
    print lucky_draw()
    pass
