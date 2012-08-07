import re
from mechanize import Browser
class authenticator:
    def __init__(self, browser):
        self.br = browser

    def authenticate(self, target, user, password):
        try:
            self.br.open('https://auth.berkeley.edu/cas/login?service=%s'%target)
            self.br.select_form(nr=0)
            self.br['username'] = user
            self.br['password'] = password
            page = self.br.submit().read()
            errors = re.findall('<h3 class="calnet-help"',page)
            if len(errors) == 0:
                print 'Logged in successfully!'
            else:
                for error in errors: print error
        except IOError, e: print "Couldn't connect: \n", e

        
