#!/usr/bin/python
# coding=utf-8
# "DATASHEET": http://cl.ly/ekot
# https://gist.github.com/kadamski/92653913a53baf9dd1a8
from __future__ import print_function

# Cron setup
# sudo nano speedtest-cron.sh
# */5 * * * * /var/www/html/speedtest/speedtest-cron.sh > /tmp/log.log 2>&1
# sudo chmod +x speedtest-cron.sh

# Run every hour from 9am to 10pm everyday 20min after the hour
# 20 9,10,11,12,13,14,15,16,17,18,19,20,21,22 * * * /var/www/html/speedtest/speedtest-cron.sh > /tmp/speedtest-log.log 2>&1


# cd /home/pi/speedtest
# sudo python speedtest.py

import re
import subprocess
import time

## NEW: Get External IP Adress
import urllib
import re







## NEW:
timestamp = time.strftime("%m.%d.%Y %H:%M:%S")
#print (timestamp)
print("\nStart Script on " + timestamp) 


## NEW: Setup Google Doc Auth
import gspread
from oauth2client.service_account import ServiceAccountCredentials

## NEW: use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\Users\gonzj637\Documents\speedtest\secret.json', scope)
client = gspread.authorize(creds)




## NEW: Get External IP Adress
def get_external_ip():
	site = urllib.urlopen("http://checkip.dyndns.org/").read()
	grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
	address = grab[0]
	return address

if __name__ == '__main__':
	external_ip = (get_external_ip())
	print("External IP:", external_ip)


## NEW: Get Internal IP Adress
import socket
def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
        internal_ip = (get_internal_ip())
        print("Internal IP:", internal_ip)



response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()


ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping[0] = ping[0].replace(',', '.')
download[0] = download[0].replace(',', '.')
upload[0] = upload[0].replace(',', '.')
print ("p ", ping[0], "d ", download[0], "u ", upload[0])




## Update Google Doc Section
## Find a workbook by name and open the first sheet
sheet = client.open("speedtest.net").sheet1
row_values = [ping[0], download[0], upload[0], timestamp, external_ip, internal_ip, "hp"]
row_number = 2
result = sheet.insert_row(row_values, row_number)

print("Updating Google Doc")

