from urllib2 import Request, urlopen, URLError, HTTPError




def samplefirst():
    try:
        response = urllib2.urlopen('http://www.alibaidu.com/')
        html = response.read()
        print html
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        print '# everything is fine #'


def samplesecond():
    old_url = 'http://rrurl.cn/b1UZuP'
    req = Request(old_url)
    response = urlopen(req)
    print 'Old url :' + old_url
    print 'Real url :' + response.geturl()



#samplefirst()
samplesecond()