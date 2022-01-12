# tv-ftp
## Python scripts for ftp download of tv grids
A linux shell cron job was set up to run these files to download weekly TV grid files for Tribune publishing-owned newspapers in Maryland.

The ftplib and PyPDF2 libraries are relied upon for ftp downloading and pdf manipulation respectively.

## cap_tv.py
The cap_tv.py file was the trickiest of the scripts to write. After downloading the PDF file from a password protected Tribune Medias Services site, PyPDF2 is used to split the nine pages and save individual grids (pages) with a specific date. 
