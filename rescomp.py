#!/usr/bin/python

import re
from mechanize import Browser
from getpass import getpass
try:
    
    br = Browser()
    br.open('https://auth.berkeley.edu/cas/login?service=https://net-auth-b.housing.berkeley.edu/cgi-bin/pub/nac-web-auth/nac-auth?requested_url=')
    br.select_form(nr=0)
    br['username'] = raw_input('username: ')
    br['password'] = getpass('password: ')
    page = br.submit().read()
    errors = re.findall('<h2 id="status" class="error">[^<]*</h2>',page)
    if len(errors) == 0:
        print 'Logged in successfully!'
    else:
        for error in errors: print error[30:-5]
except IOError, e: print "Couldn't connect to wireless login page: \n", e

