#!/usr/bin/python

import os
import re
import shutil
from mechanize import Browser
from auth import auth
from getpass import getpass

class telebears:
    def __init__(self):
        self.br = Browser()
        self.a = auth(self.br)
        
    def login(self):
        user = raw_input('username: ')
        password = getpass('password: ')
        self.a.auth('https://telebears.berkley.edu', user, password)
        
    