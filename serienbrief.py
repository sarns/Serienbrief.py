import codecs
import os
import re
import subprocess
from PyPDF2 import PdfFileMerger

firstline = 'True'
files = os.listdir()

i = 1

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

                        with codecs.open('Brief_' + str(i) + '.tex','w','utf-8') as MyFile3:
                            MyFile3.write(letter)
                        print(str(i) + ' ' + customer[5])
                        cmd = ['/usr/local/texlive/2015/bin/x86_64-darwin/xelatex','Brief_' + str(i) + '.tex']
                        process = subprocess.call(cmd)

                        os.remove('Brief_' + str(i) + '.tex')
                        os.remove('Brief_' + str(i) + '.out')
                        os.remove('Brief_' + str(i) + '.log')
                        os.remove('Brief_' + str(i) + '.aux')
                        i += 1

        cmd = ['/usr/local/bin/gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=pdfwrite','-sOutputFile=MergedPDF.pdf','*.pdf']
        process = subprocess.call(cmd)

        for element in range(1,i-1):
            os.remove('Brief_' + str(element) + '.pdf')
  
                                                
                    
                
        
