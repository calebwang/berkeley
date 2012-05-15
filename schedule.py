#!/usr/bin/python

import os
import re
import shutil
from datetime import datetime
from mechanize import Browser
deptabbreviations = {'e':'engineering', 'cs':'computer science', 'ee':'electrical engineering', 'psych':'psychology'}

class data:
    def __init__(self):
        self.basepath = '/home/caleb/git/berkeley/schedule-data/'
        os.chdir(self.basepath)

    def parsename(self, filename):
        dept = re.search('[a-z]*', filename).group(0)
        cid = re.search('[0-9]{1,3}[a-z]{0,2}', filename).group(0)
        if dept in deptabbreviations:
            dept = deptabbreviations[dept]
        return (dept, cid)

    def init(self, file, ccn, dept = '', cid = ''):
        try:
            if file in os.listdir('.'):
                f = open(file)
                text = f.read()
                f.close()
                if not re.search(str(ccn), text):
                    shutil.move(file, file + '~')
                    dest = open(file, 'w')
                    source = open(file + '~', 'r')
                    checked = False
                    for line in source:
                        if (not checked) and re.search('[0-9]{5}', line):
                            ccns = re.findall('[0-9]{5}', line)
                            newline = 'ccn: '
                            for oldccn in ccns:
                                newline = newline + oldccn + ' '
                            newline = newline + str(ccn) + '\n'
                            dest.write(newline)
                            checked = True
                        else:
                            dest.write(line)
                    dest.close()
                    source.close()
                    os.remove(file + '~')
            else:
                f = open(file, 'w')
                ccn = str(ccn)
                if (dept == '' or cid == ''):
                    deptid = self.parsename(file)
                    dept = deptid[0]
                    cid = deptid[1]
                f.write('department: %s\n'%dept)
                f.write('course number: %s\n'%cid)
                f.write('ccn: %s\n'%ccn)
                f.write('--------------------------------------------------------------------\n')
                f.write('          Date             lecture  enrolled  capacity  percent full\n')
        except IOError, e: 
            print e, '2'
        
    
    def update(self):
        try:
            files = os.listdir('.')
            for pathname in files:
                if re.search('[0-9]', pathname) == None:
                    continue
                file = open(self.basepath + pathname, 'r')
                ccns = re.findall('[0-9]{5}', file.read())
                file.close()
                for ccn in ccns:
                    print pathname, ccn
                    datestring = datetime.ctime(datetime.today())
                    r = reader()
                    data = r.check(ccn)
                    newline = datestring + '     ' + data[0] +  '       ' +  data[1] + '       '  + data[2] + '         ' + '%.3f'%(int(data[1])*1.0/int(data[2]))
                    file = open(self.basepath + pathname, 'a')
                    file.write(newline + '\n')
        except IOError, e:
            print e, '5'
        
    def batchupdate(self, filename):
        f = open(filename)
        for line in f:
            data = re.split(' ', line)
            self.init(data[0], data[1][0:5])
        f.close()    
        self.update()
        
class reader:
    def __init__(self):
        self.br = Browser()

    def check(self, ccn):
        try:
            url = 'http://infobears.berkeley.edu:3400/osc/?_InField1=RESTRIC&_InField2=%s&_InField3=12D2'%ccn
            page = self.br.open(url).read()
            lec = re.findall('[0-9]{3} [A-Z]{3}', page)[0][0:3]
            print lec
            info = re.split('enrollment information', page)[2]
            data = re.findall('[0-9]{1,4}', info)
            enrolled = data[1]
            limit = data[2]
            return (lec, enrolled, limit)
        except IOError, e:
            print e, '7'
            return ('000', '0', '0')

def main():
    d = data()
    d.batchupdate('classes')

main()
