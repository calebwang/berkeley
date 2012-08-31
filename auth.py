import re
from mechanize import Browser
from getpass import getpass
class authenticator:

    def __init__(self, browser):
        self.br = browser

    def login(self, target, user, password):
        try:
            self.br.open('https://auth.berkeley.edu/cas/login?service=%s'%target)
            self.br.select_form(nr=0)
            self.br['username'] = user
            self.br['password'] = password
            page = self.br.submit().read()
            if re.findall('Successful', page):
                print 'Logged in successfully!'
            else:
                print 'Unsuccessful login attempt!'
        except IOError, e: print "Couldn't connect: \n", e
        
    def secure_login(self, target=''):
        username = raw_input('username:' )
        password = getpass('password: ')
        login(target, username, password)
        

        
