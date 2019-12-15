import time


def login():
    return "----login----hello,world %s" % time.ctime()

def register():
    return "----register----hello,world %s" % time.ctime()

def logout():
    return "----logout----hello,world %s" % time.ctime()

def application(file_name):
    if file_name == "/login.py":
        return login()
    elif file_name == "/register.py":
        return register()
    elif file_name == "/logout.py":
        return logout()
    else:
        return "404 not found"
