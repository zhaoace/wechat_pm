#-*- coding: UTF-8 -*-
import web
import wechat

urls = (
    '/', 'index',
)


class index:

    def GET(self):
        user_data = web.input()
        token = "splunktoken"
        if len(user_data) == 0:
            return "No input"
        else:
            return wechat.verify(user_data, token)

    def POST(self):
        print "---- POST start ---"
        user_data = web.data()
        wx_content = wechat.read_post_content(user_data)
        if "splunkers" == wx_content:
            print "注册注册注册"
        elif "lucky_draw" == wx_content:
            print "大抽奖"
        else:
            print "啥操作？" + wx_content

        # json_res = wechat.xml_string_to_json(user_data)
        print "---- POST end ---"
        return "success"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
