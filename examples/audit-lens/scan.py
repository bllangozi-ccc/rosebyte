"""Bounded client for the local fixed-function incoming scan gate."""
import hashlib,json,socket,struct

def scan(data,path='/run/rb-native-gate/gate.sock'):
    if not isinstance(data,bytes) or not 1<=len(data)<=262144:raise ValueError('Scan byte limit')
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as client:
        client.settimeout(5);client.connect(path);client.sendall(struct.pack('!I',len(data))+data)
        reply=b''
        while b'\n' not in reply and len(reply)<4096:
            part=client.recv(4096-len(reply))
            if not part:break
            reply+=part
    r=json.loads(reply)
    if not isinstance(r,dict) or r.get('status')!='clean':raise ValueError('Incoming scanner rejected content or is unavailable')
    if type(r.get('size')) is not int or r['size']!=len(data) or r.get('sha256')!=hashlib.sha256(data).hexdigest():raise ValueError('Incoming scan receipt mismatch')
