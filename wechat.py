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


def lucky_draw():
    current = pymongo.MongoClient().splunkers.current
    lucky_one = current.find()
    return lucky_one

def verify_votes(vote_type, candidate):
    if vote_type not in range(1,3):
        return False
    elif candidate not in range(1,4):
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
        collection = VOTE_TYPES[vote_type]
        vote_pool = pymongo.MongoClient().test1[collection]
        if vote_pool.find({"voter": voter}).count() == 0:
            vote_pool.insert({"candidate": candidate, "voter": voter})
            vote_count = vote_pool.find({"candidate": candidate}).count()
            print "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
            return "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
        else:
            vote_pool.find_one_and_update({"voter": voter},  {'$set': {"candidate": candidate}})
            vote_count = vote_pool.find({"candidate": candidate}).count()
            print "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
            return "Thank you , the candidate {0} have {1} votes now.".format(candidate, vote_count)
    else:
        print "别闹了，好好投票。。。"
        return "别闹了，好好投票。。。"



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
    # print lucky_draw()
    voting(1, 2, 3)
    voting(1, 2, 3)
    voting(1, 2, 3)
    voting(1, 2, 3)
    voting(1, 3, 3)
    voting(1, 3, 3)
    voting(1, 3, 3)
    voting(1, 3, 3)
    voting(2, 3, 3)
    voting(2, 5, 3)
    voting(2, "你说啥", 3)
    voting(2, 3, 3)
    voting(2, 3, 3)
    voting(2, 3, 3)
    voting(3, 3, 3)
    voting(3, 3, 3)
    voting(3, 3, 3)
    voting(5, 3, 3)
    voting(3, 3, 3)
    voting(3, 3, 3)
    voting(3, 3, 3)

    pass
