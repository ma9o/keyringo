from ecdsa import SigningKey, SECP256k1
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import binascii
import keyring.backends.OS_X 
import keyring
import _thread

class CryptoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        keyring.set_keyring(keyring.backends.OS_X.Keyring())
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        parsed = urlparse(self.path)
        
        if parsed.path == "/sign":
            message = parsed.query
            res, pub = self.sign(message)
            self.wfile.write(str.encode("{success: true, res: "+str(res)[1:]+", pub: "+str(pub)[1:]+"}"))
        else:
            self.wfile.write(b'{success: false}')

        return

    def sign(self, message):
        raw = keyring.get_password("Ethereum private key", "user")
        data = binascii.unhexlify(raw)
        key = SigningKey.from_string(data, curve=SECP256k1)
        encoded = message.strip().encode("utf-8").hex()
        signature = key.sign(binascii.unhexlify(encoded))
        return (binascii.b2a_hex(signature),binascii.b2a_hex(key.get_verifying_key().to_string()))
        