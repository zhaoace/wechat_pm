import sha
import web


urls = (
    '/', 'index'
)


class index:
    def GET(self):
        print "wechat_verify"

        user_data = web.input()
        token     = "Token"

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

        if tempSha == user_data.signature :
            print "Verify successed ! \n"
            return user_data.echostr
        else :
            print "Verify failed ! \n"
            return False


if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
