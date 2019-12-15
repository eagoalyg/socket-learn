def index():
    with open('./templates/index.html') as f:
        content = f.read()
    return content

def python_web():
    return open('./templates/python.html').read() 

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8')])
    file_name = env['PATH_INFO']

    if file_name == '/index.py':
        return index()
    elif file_name == '/python.py':
        return python_web()
    else:
        return 'not found'
