#!/usr/bin/python 

import os
import datetime
import calendar
import ftplib
from ftplib import FTP
from datetime import date
from PyPDF2 import PdfFileWriter, PdfFileReader
from dotenv import load_dotenv

FTP_LOGIN = os.getenv('FTP_LOGIN')
FTP_PW = os.getenv('FTP_PW')

ftp = FTP('ftp9.tmstv.com')
ftp.login(FTP_LOGIN, FTP_PW)

#ftp.cwd("/ftptest/")

def page_split(the_file):
	inputpdf = PdfFileReader(open(the_file, "rb"))
	for i in range(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		n = i+1
		with open('%s.pdf' % n, 'wb') as outputStream:
			output.write(outputStream)

#returns a dictionary in format {'1':['SUN,'0323'} 
def filenamer():
   code_dict = {}
   for i in range(3,10):
      pub_date = datetime.datetime.today() + datetime.timedelta(days = i)
      pub_day = calendar.day_name[pub_date.weekday()][:3].upper()
      pub_string = pub_date.strftime('%m%d')
      codes = [pub_day, pub_string]
      i = i-2
      code_dict[i] = codes
   return code_dict

def filesaver():
	code_dict = filenamer()
	for i in range(1,10):
		if i == 1:
			newname = 'ph-ac-tvgrid-full-' + code_dict[i][0] + code_dict[i][1] + '-xnx.pdf'
			oldname = str(i) +'.pdf'
		elif i == 2:
			newname = 'ph-ac-tvgrid-' + code_dict[1][0] + code_dict[1][1] + '-xnx.pdf'	
			oldname = str(i) +'.pdf'			
		elif i == 8:
			newname = 'ph-ac-tvgrid-full-' + code_dict[7][0] + code_dict[7][1] + '-xnx.pdf'
		elif i == 9:
			newname = 'ph-ac-tvgrid-' + code_dict[7][0] + code_dict[7][1] + '-xnx.pdf'
		else:
			newname = 'ph-ac-tvgrid-' + code_dict[i-1][0] + code_dict[i-1][1] + '-xnx.pdf'
		oldname = str(i) +'.pdf'
		os.rename(oldname, newname)

def grab():
   os.chdir('/home/ericreyes/ftptest/tmp')
   filename = 'annadly.pdf'   
   ftp.retrbinary('RETR '+filename, open(filename, 'wb').write)
   ftp.quit()
   page_split(filename)
   filesaver()


def main():
   grab()
  

#def store():
 #  filename = 'testfile.txt'
  # ftp.storbinary('STOR'+filename, open(filename, 'rb'))
   #ftp.quit()
    
try:
   main()
except ftplib.all_errors as e:
   ftp.quit()
   os.chdir('/home/ericreyes/ftptest')
   logf = open('download.log','a')
   entry = str(e) + str(datetime.datetime.now()) + '\n'
   logf.write(entry)
   logf.close()
   
#store()

