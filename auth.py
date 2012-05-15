import re
from mechanize import Browser
class auth:
    def __init__(self):
        self.br = Browser()

    def auth(self, target, user, password):
        try:
            self.br.open('https://auth.berkeley.edu/cas/login?service=%s'%target)
            self.br.select_form(nr=0)
            self.br['username'] = user
            self.br['password'] = password
            page = self.br.submit().read()
            errors = re.findall('<h2 id="status" class="error">[^<]*</h2>',page)
            if len(errors) == 0:
                print 'Logged in successfully!'
            else:
                for error in errors: print error[30:-5]
        except IOError, e: print "Couldn't connect: \n", e

        
