def logout():
    return '----logout----'

def login():
    return '----login----'

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8')])
    file_name = env['PATH_INFO']

    if file_name == '/logout.py':
        return logout()
    elif file_name == '/login.py':
        return login()
    else:
        return 'not found'
