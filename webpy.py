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
        wx_poster =  wechat.get_poster(user_data)
        if "投票" == wx_content[0] or "vote" == wx_content[0].lower():
            wechat.voting(wx_content[0],wx_content[1],wx_poster)
            print wx_content
        else:
            print "无效操作" + wx_content[0]

        print "---- POST end ---"
        return "success"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
