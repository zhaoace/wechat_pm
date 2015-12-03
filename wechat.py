#-*- coding: UTF-8 -*-
import logging
import sha
import xmltodict
import json
import pymongo
import urllib
import urllib2
import yaml
import random
import xml.etree.ElementTree as ET

VOTE_TYPES = {
    1: "gameplayer",
    2: "superstar",
    3: "program"
}


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
    root = ET.fromstring(user_data)
    content = root.find("Content").text.strip().split()
    return content

def get_poster(user_data):
    root = ET.fromstring(user_data)
    poster = root.find("FromUserName").text.strip()
    return poster


def lucky_draw():
    current = pymongo.MongoClient().splunkers.current
    lucky_one = current.find()
    return lucky_one


def verify_votes(vote_type, candidate):
    if not vote_type.isdigit() or not candidate.isdigit():
        return False
    elif int(vote_type) not in range(1, 3):
        return False
    elif int(candidate) not in range(1, 10):
        return False
    else:
        return True


def voting(vote_type, candidate, voter):
    """
        # 投票者 voters
        # 候选人 candidates
        # 选票 vote
    """
    if verify_votes(vote_type, candidate):
        vote_type = int(vote_type)
        candidate = int(candidate)
        print u"处理投票"
        collection = VOTE_TYPES[vote_type]
        vote_pool = pymongo.MongoClient().test1[collection]
        if vote_pool.find({"voter": voter}).count() == 0:
            vote_pool.insert({"candidate": candidate, "voter": voter})
            vote_count = vote_pool.find({"candidate": candidate}).count()
            print "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
            return "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
        else:
            vote_pool.find_one_and_update(
                {"voter": voter},  {'$set': {"candidate": candidate}})
            vote_count = vote_pool.find({"candidate": candidate}).count()
            print "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
            return "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
    else:
        # return u"别闹了，好好投票。。。"
        return "Wrong vote format, please check and retry"


def reply_msg_to_wx_user(user, message):
    access_token = get_client_credential()
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token="+access_token
    print "reply_msg_to_wx_user message:"+message
    values = {
        "touser": user,
        "msgtype": "text",
        "text": {
                "content": message
            }
        }
    json_values = json.dumps(values)
    print json_values
    req = urllib2.Request(url, json_values)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

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
    print verify_votes(u"1",2)
    print verify_votes(1,3)
    print verify_votes(1,4)
    print verify_votes(5,5)
    print verify_votes(1,10)
