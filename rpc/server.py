from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import os
import shutil
import json

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

path = '~/.tennetnodes'

def remove():
    """removes the nodes from the system."""
    print("remove")
    shutil.rmtree(path)
    return True

def add(ip, walletaddress, country, dna):
    """
    Adds ip to the json files.

    ip -- The ip address this server is contacted from.
    walletaddress -- The walletaddress used.
    country -- The country this ip is in.
    dna -- The dna that this server contains.
    """
    print("add")
    if not os.path.exists(path):
        os.makedirs(path)
    write_json(ip, walletaddress, country, dna)
    return True

def write_json(ip, walletaddress, country, dna):
    """
    Writes the json file.

    ip -- The ip address this server is contacted from.
    walletaddress -- The walletaddress used.
    country -- The country this ip is in.
    dna -- The dna that this server contains.
    """
    data = {'ip':ip, 'wallet':walletaddress, 'country':country, 'dna':dna, 'upload':'0'}
    _write_json(ip, data)

def _write_json(ip, data):
    """Writes data to the filename of ip."""
    filename = '%s/%s.json' % (path, ip)
    print("writing: %s" % str(data))
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def read_json(ip):
    filename = '%s/%s.json' % (path, ip)
    data = None
    print("opening: %s" % filename)
    with open(filename, 'r') as f:
        data = json.load(f)
        print("Reached here.")
    print("read: %s" % str(data))
    return data

def update(ip, newupload):
    """
    Sets newupload as the upload capacity.

    ip -- The used ip address.
    newupload -- The new total uploaded data.
    """
    print("update")
    data = read_json(ip)
    data['upload'] = newupload
    _write_json(ip, data)
    return True

def list_files():
    print("list files")
    if os.path.exists(path):
        return str(os.listdir(path))
    else:
        return "None"

server.register_function(remove)
server.register_function(add)
server.register_function(update)
server.register_function(list_files)

# Run the server's main loop
server.serve_forever()
