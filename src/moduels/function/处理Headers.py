from urllib import parse

def 处理Headers(Headers, 网址链接):
    网址域名 = parse.urlparse(网址链接).netloc
    if 网址域名 == 'b3logfile.com':
        Headers['referer'] = 'https://ld246.com/'
    return Headers

