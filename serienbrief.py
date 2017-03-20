import codecs
import os
import re
import subprocess

# Initialize needed variables
firstline = 'True'
i = 1

# get files in current folder
files = os.listdir()

# iterate over all files
for file in files:
    # look for .DOC customer files
    if file.endswith('.DOC'):
        # get customer type
        customer_type = file[0:len(file)-4]
        # open customer file with ISO-8859 encoding
        with codecs.open(file,'r','iso-8859-1') as MyFile:
            # read every line of the file
            for line in MyFile:
                # check if firtst line with header information
                if firstline == 'True':
                    # split header fields
                    headers = line.split(';')
                    firstline = 'False'
                else:
                    # split data fields
                    customer = line.split(';')
                    # open letter template
                    with codecs.open(customer_type + '.tex','r','utf-8') as MyFile2:
                        # read file to string
                        letter = MyFile2.read()
                        # RegEx matching and substitution in template with customer data
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
                        # write substituted letter to .tex
                        with codecs.open('Brief_' + str(i) + '.tex','w','utf-8') as MyFile3:
                            MyFile3.write(letter)
                        print(str(i) + ' ' + customer[5])
                        # typesetting of letters with XeLaTex
                        cmd = ['/usr/local/texlive/2015/bin/x86_64-darwin/xelatex','Brief_' + str(i) + '.tex']
                        process = subprocess.run(cmd)
                        # remove not needed files 
                        os.remove('Brief_' + str(i) + '.tex')
                        os.remove('Brief_' + str(i) + '.out')
                        os.remove('Brief_' + str(i) + '.log')
                        os.remove('Brief_' + str(i) + '.aux')
                        i += 1
         
        # create merge cmd
        cmd = ['/usr/local/bin/gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=pdfwrite','-sOutputFile=MergedPDF.pdf']
        # create filelist for arguments of cmd
        filelist = []
        for element in range(1,i):
            filelist.append('Brief_' + str(element) + '.pdf')
        # merge all PDF letters to one file
        process = subprocess.run(cmd + filelist)
        for element in filelist:
            os.remove(element)
