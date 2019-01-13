from cryptohandler import CryptoHandler

from http.server import HTTPServer
import _thread
import sys
import os
import rumps
import shelve
import keyring.backends.OS_X 
import keyring

class KeyRingo(rumps.App):

    def __init__(self):
        rumps.App.__init__(self, "🔑", quit_button=None)
    
        self.db = shelve.open("./db")
        tmp = rumps.MenuItem("Run at startup")
        try:
            if self.db['startup'] == True:
                tmp.state = 1
            else:
                tmp.state = 0
        except:
            tmp.state = 0
        
        self.menu.update(tmp)
        
    @rumps.clicked("Run at startup")
    def onoff(self, sender):
        sender.state = not sender.state
        self.db['startup'] = sender.state
        if (sender.state):
            os.system("osascript -e 'tell application \"System Events\" to make new login item with properties {name:\"KeyRingo\", path:\"/Applications/KeyRingo.app\"}'")
        else:
            os.system("osascript -e 'tell application \"System Events\" to delete login item \"KeyRingo\"'")

    @rumps.clicked("Change private key")
    def prefs(self, _): 
        w = rumps.Window(cancel=True, title="Change private key", dimensions=(320, 40))
        res = w.run()
        if res.clicked:
            try:
                int(res.text, 16)
                if len(res.text) is not 64:
                    rumps.alert(title="Error", message="Key size must be 32 bytes")
                else:
                    rumps.alert(title="Success", message="Key updated")
                    keyring.set_password("Ethereum private key", "user", res.text)
            except ValueError:
                rumps.alert(title="Error", message="Key must be an hex value")
            

    @rumps.clicked("Quit")
    def close(self, _):
        self.db.close()
        rumps.quit_application()

if __name__ == '__main__':
    httpd = HTTPServer(('127.0.0.1', 8001), CryptoHandler)
    _thread.start_new_thread(httpd.serve_forever, ())
    KeyRingo().run()
    
    
    
