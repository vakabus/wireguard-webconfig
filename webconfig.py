from flask import Flask, request, redirect, Response
from functools import wraps
import sys
import time

app = Flask(__name__)
if len(sys.argv) == 1:
    print("Config filename unspecified!!")
    exit(1)
config_file = sys.argv[1]
username = ''
password = ''

def check_auth(user, passwd):
    """This function is called to check if a username /
    password combination is valid.
    """
    global password
    global username

    if password == '':
        with open(config_file, 'r') as cf:
            for line in cf:
                if "Password" in line:
                    password = line[line.rfind(' ')+1:-1]
                    if password == 'UNSET':
                        password = ''
                if "Username" in line:
                    username = line[line.rfind(' ')+1:-1]
    if username == '' or password == '':
        print("Empty username and/or password!!! Access denied!!!")
        return False
    result = user == username and passwd == password

    # Simple bruteforcing prevention
    if result is False:
        time.sleep(0.5)
    return result

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
@requires_auth
def root():
    config = ''
    peer_counter = 0
    with open(config_file, 'r') as cf:
        for line in cf:
            line = line[:-1]
            if line.startswith("PrivateKey"):
                config += 'PrivateKey = THIS_IS_SECRET_PLEASE_DONT_READ<br/>'
            elif line.startswith("[I"):
                config += "<b>" + line + "</b><br/>"
            elif line.startswith("[Peer"):
                peer_counter += 1
                config += "<b>" + line + "</b> <a href='/remove_peer?c={}'>(-)</a><br/>".format(peer_counter)
            else:
                config += line + "<br/>"
        
    page = '''
    <!doctype html><html><body>
    {}<hr/><h2>Add new peer:</h2>
    <form method='GET' action='/add_peer'>
        <input type='text' name='name' placeholder='Device name' required='true' />
        <input type='text' name='pubkey' placeholder='Public key' required='true' />
        <input type='text' name='ips' placeholder='Allowed IPs' required='true' />
        <input type='submit' value="Add" />
    </form>
    </body>
    '''

    return page.format(config)

@app.route("/add_peer", methods=['GET', 'POST'])
@requires_auth
def add_peer():
    peer_conf = '''
[Peer]
# {name}
PublicKey = {pubkey}
AllowedIPs = {ips}
'''
    dev_name = request.values['name']
    pubkey = request.values['pubkey']
    ips = request.values['ips']

    peer_conf = peer_conf.format(name=dev_name, pubkey=pubkey, ips=ips)

    with open(config_file, 'a') as cf:
        cf.write(peer_conf)

    return redirect('/')

@app.route("/remove_peer", methods=['GET', 'POST', 'DELETE'])
@requires_auth
def remove_peer():
    peer_counter = 0
    config = ''
    removing = False
    peer_to_remove = int(request.values['c'])
    with open(config_file, 'r') as cf:
        for line in cf:
            if line.startswith('[Peer'):
                peer_counter += 1
                if peer_to_remove == peer_counter:
                    removing = True
            elif line == '\n':
                removing = False
            if not removing:
                config += line
    
    # normalize config file
    config = config.replace('\n\n\n', '\n\n')
    if config.endswith('\n\n'):
        config = config[:-1]

    with open(config_file, 'w') as cf:
        cf.write(config)

    return redirect('/')

if __name__ == "__main__":
    app.run(port=51821)