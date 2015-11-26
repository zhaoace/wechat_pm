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
	
	if len(user_data) == 0 :
	    return "No input"
	
	print "user_data"
	print user_data
        l = []
        l.append(token)
	print "user_data.timestamp = "
	print user_data.timestamp
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

    def POST(self):
	print "---- POST start ---"
	#user_data = web.input()
	user_data = web.data()
	print user_data
	print "---- POST end ---"
        return "success" 


if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
