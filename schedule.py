#!/usr/bin/python

import os
import re
from datetime import datetime
from mechanize import Browser

class data:
    def __init__(self):
        self.basepath = '/home/caleb/git/berkeley/schedule-data/'
        os.chdir(self.basepath)

    def parsename(self, filename):
        dept = re.search('[a-z]*', filename).group(0)
        cid = re.search('[0-9]{1,3}[a-z]{0,2}', filename).group(0)
        return (dept, cid)

    def init(self, file, ccn, dept = '', cid = ''):
        if file in os.listdir('.'):
            return
        try:
            f = open(file, 'w')
            ccn = str(ccn)
            if (dept == '' or cid == ''):
                deptid = self.parsename(file)
                dept = deptid[0]
                cid = deptid[1]
                f.write('department: %s\n'%dept)
                f.write('course number: %s\n'%cid)
                f.write('ccn: %s\n'%ccn)
                f.write('------------------------------------------------------------\n')
                f.write('          Date             enrolled  capacity  percent full\n')
        except IOError, e: 
            print e
        
    
    def update(self):
        try:
            for pathname in os.listdir('.'):
                if re.search('[a-z]*[0-9]{1,3}[a-z]{0,2}', pathname) == None:
                    continue
                file = open(self.basepath + pathname, 'r')
                ccn = re.search('[0-9]{5}', file.read()).group(0)
                print pathname, ccn
                file.close()
                datestring = datetime.ctime(datetime.today())
                r = reader()
                data = r.check(ccn)
                newline = datestring+ '     ' +  data[0] + '       '  + data[1] + '         ' + '%.3f'%(int(data[0])*1.0/int(data[1])) + '\n'
                file = open(self.basepath + pathname, 'a')
                file.write(newline)
        except IOError, e:
            print e
        
    def batchupdate(self, filename):
        f = open(filename)
        for line in f:
            data = re.split(' ', line)
            self.init(data[0], data[1])
        self.update()
        f.close()
        
class reader:
    def __init__(self):
        self.br = Browser()

    def check(self, ccn):
        try:
            url = 'http://infobears.berkeley.edu:3400/osc/?_InField1=RESTRIC&_InField2=%s&_InField3=12D2'%ccn
            page = self.br.open(url).read()
            info = re.split('enrollment information', page)[2]
            data = re.findall('[0-9]{1,4}', info)
            enrolled = data[1]
            limit = data[2]
            return (enrolled, limit)
        except IOError, e:
            print e
            return ('0', '0')

d = data()
d.batchupdate('classes')
