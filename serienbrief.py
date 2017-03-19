import codecs
import os
import re
import subprocess

firstline = 'True'
files = os.listdir()

for file in files:
    if file.endswith('.DOC'):
        customer_type = file[0:len(file)-4]
        with codecs.open(file,'r','iso-8859-1') as MyFile:
            for line in MyFile:
                if firstline == 'True':
                    headers = line.split(';')
                    firstline = 'False'
                else:
                    customer = line.split(';')
                    with codecs.open(customer_type + '.tex','r','utf-8') as MyFile2:
                        letter = MyFile2.read()
                        
                        pattern = re.compile('<<Namenszeile>>')
                        letter = pattern.sub(customer[5],letter)

                        pattern = re.compile('<<Strasse>>')
                        letter = pattern.sub(customer[8],letter)

                        pattern = re.compile('<<Land>>')
                        letter = pattern.sub(customer[9],letter)

                        pattern = re.compile('<<PLZ>>')
                        letter = pattern.sub(customer[10],letter)

                        pattern = re.compile('<<Stadt>>')
                        letter = pattern.sub(customer[11],letter)

                        pattern = re.compile('<<AnredeFormel>>')
                        letter = pattern.sub(customer[15],letter)

                        pattern = re.compile('<<Ansprechpartner>>')
                        letter = pattern.sub(customer[16],letter)

                        with codecs.open(customer[5] + '.tex','w','utf-8') as MyFile3:
                            MyFile3.write(letter)
                        cmd = ['/usr/local/texlive/2015/bin/x86_64-darwin/xelatex',customer[5] + '.tex']
                        process = subprocess.call(cmd)

                        os.remove(customer[5] + '.tex')
                        os.remove(customer[5] + '.out')
                        os.remove(customer[5] + '.log')
                        os.remove(customer[5] + '.aux')
                        
      
                                                
                    
                
        
