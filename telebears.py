#!/usr/bin/python

import os
import re
import shutil
from mechanize import Browser
from auth import authenticator
from getpass import getpass

class telebears:

    def __init__(self):
        self.br = Browser()
        self.auth = authenticator(self.br)
        
    def login(self):
        user = raw_input('username: ')
        password = getpass('password: ')
        self.auth.login('https://telebears.berkley.edu', user, password)
        
    