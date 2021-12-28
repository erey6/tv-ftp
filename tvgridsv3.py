# /usr/bin/python
import os
import datetime
import calendar
import ftplib
from ftplib import FTP
from datetime import date
from PyPDF2 import PdfFileWriter, PdfFileReader
import smtplib
from dotenv import load_dotenv

load_dotenv()

FTP_LOGIN = os.getenv('FTP_LOGIN')
FTP_PW = os.getenv('FTP_PW')

ftp = FTP('ftp9.tmstv.com')
ftp.login(FTP_LOGIN, FTP_PW)
# ftp.cwd("/ftptest/")


# returns a dictionary in format {'1':['SUN,'0323'}
def filenamer():
    code_dict = {}
    for i in range(3, 10):
        pub_date = datetime.datetime.today() + datetime.timedelta(days=i)
        pub_day = calendar.day_name[pub_date.weekday()][:3].upper()
        pub_string = pub_date.strftime('%m%d')
        codes = pub_day + '-' + pub_string
        i = i - 2
        code_dict[i] = codes
        code_dict[i + 9] = codes
    return code_dict
    


def main():
    # os.chdir('/pdfs/')
    os.chdir(os.path.expanduser('~/tvgrids/program/pdfs'))
    filename = 'annadly.pdf'
    print('37')
    ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write) 
    ftp.quit()
    
    inputpdf = PdfFileReader(open(filename, "rb"))
    print("42")
    for i in range(inputpdf.numPages):
        print('44')
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        n = i + 1
        with open('%s.pdf' % n, 'wb') as outputStream:
            output.write(outputStream)
        z = n + 9
        with open('%s.pdf' % z, 'wb') as outputStream:
            output.write(outputStream)

    code_dict = filenamer()
    print("Codedict ", code_dict)
    for i in range(1, 10):
        x = i + 9
        if i == 1:
            newname = 'ph-ac-tvgrid-full-' + \
                code_dict[i] + '-CMYK.pdf'
            newnamebw = 'ph-ac-tvgrid-full-' + \
                code_dict[x] + '-BW.pdf'

        elif i == 2:
            newname = 'ph-ac-tvgrid-' + \
                code_dict[1] + '-CMYK.pdf'
            newnamebw = 'ph-ac-tvgrid-' + \
                code_dict[1] + '-BW.pdf'

        elif i == 8:
            newname = 'ph-ac-tvgrid-full-' + \
                code_dict[7] + '-CMYK.pdf'
            newnamebw = 'ph-ac-tvgrid-full-' + \
                code_dict[7] + '-BW.pdf'

        elif i == 9:
            newname = 'ph-ac-tvgrid-' + \
                code_dict[7] + '-CMYK.pdf'
            newnamebw = 'ph-ac-tvgrid-' + \
                code_dict[7] + '-BW.pdf'

        else:
            newname = 'ph-ac-tvgrid-' + \
                code_dict[i - 1] + '-CMYK.pdf'
            newnamebw = 'ph-ac-tvgrid-' + \
                code_dict[i - 1] + '-BW.pdf'

        oldname = str(i) + '.pdf'
        os.rename(oldname, newname)
        oldnamebw = str(x) + '.pdf'
        os.rename(oldnamebw, newnamebw)





try:
    main()
except ftplib.all_errors as e:
    ftp.quit()
    # os.chdir(os.path.expanduser('~/Desktop/CapitalTv/'))
    logf = open('download.log', 'a')
    entry = str(e) + str(datetime.datetime.now()) + '\n'
    logf.write(entry)
    logf.close()
