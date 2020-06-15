def application(environ, start_response):
    body_404 = "<html><head><meta charset='utf-8'></head><body><h1>404 没有找到页面</h1></body>"
    if environ['location']:
        path = '/home/alex/web/web_admin' + environ['location'].strip()
        try:
            with open(path, "r") as f:
                body = f.read()
            status = '200 OK'
        except Exception as e:
            print(e)
            status = '404 None'
            body = body_404
    else:
        status = '404 None'
        body = body_404
    # ip = environ["ip"]
    # port = environ["port"]
    response_headers = {'Content-Type:': 'text/html', 'Content-length:': str(len(body)), 'Accept-Language:': 'zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3'}
    start_response(status, response_headers)
    return body
