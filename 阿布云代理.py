
def scrapy_proxy():
    import base64

    # 代理服务器
    proxyServer = "http://http-dyn.abuyun.com:9020"

    # 代理隧道验证信息
    proxyUser = "H01234567890123D"
    proxyPass = "0123456789012345"

    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
    return proxyServer, proxyAuth


def request_proxy():
    # 要访问的目标页面
    # targetUrl = "http://test.abuyun.com"
    #targetUrl = "http://proxy.abuyun.com/switch-ip"
    #targetUrl = "http://proxy.abuyun.com/current-ip"

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H01234567890123D"
    proxyPass = "0123456789012345"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }

    return proxies



