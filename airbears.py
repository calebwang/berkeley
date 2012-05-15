#!/usr/bin/python

import re
from mechanize import Browser
from getpass import getpass
try:
    br = Browser()
    br.open('https://auth.berkeley.edu/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet')
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

