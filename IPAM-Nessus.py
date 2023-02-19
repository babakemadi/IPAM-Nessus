#! /usr/bin/env python

"""API connection Python3 code to generate output file to show more information for IP Address from IPAM and in CSV fromat input/output.
The code is written By Babak Emadi Nikoo"""

import requests
import csv
import getpass
import warnings
from os import path

auth_url = "https://ipam.domain.com/api/nessusipam/user/"
base_url = "https://ipam.domain.com/api/nessusipam/addresses/search/"
warnings.filterwarnings('ignore')       #if you use without ssl certificate, you will get some warnings which you can bypass them with this

certs_pem = ssl.get_server_certificate (("ipam.domain.com", 443))

username = input("Username: ")
password = getpass.getpass()

post_response = requests.post(auth_url, verify=certs_pem, auth=(username,password))
post_text_dictionary = dict(post_response.json())
my_token = post_text_dictionary['data']['token']

header = ['IP Address', 'Hostname', 'Description', 'Owner']

input_file_name = input("Enter Your CSV  Input Filename: ")
input_file_name = (input_file_name + ".csv")

output_file_name = input("Enter Your CSV  Output Filename: ")
output_file_name = (output_file_name + ".csv")

if path.exists (input_file_name) == True:
     with open(output_file_name, 'a', newline='', encoding='utf-8') as output_file:
          writer = csv.writer(output_file)
          writer.writerow(header)
     with open (input_file_name, 'r') as input_file:
          for IP_address in input_file:
               url = base_url + IP_address.split(',')[2].rstrip('\n') + '/'
               get_response = requests.get(url, verify=certs_pem, headers={"token": my_token})
               get_response_dictionary = dict(get_response.json())
               if get_response_dictionary['success'] == True:
                    field = dict(get_response_dictionary['data'][0])
                    data = [field['ip'],field['hostname'],field['description'],field['owner']]
                    with open(output_file_name, 'a', newline='', encoding='utf-8') as output_file:
                         writer = csv.writer(output_file)
                         writer.writerow(data)
               else:
                    with open(output_file_name, 'a', newline='', encoding='utf-8') as output_file:
                         data = IP_address.split(',')[2].rstrip('\n'), 'The IP address not find'
                         writer = csv.writer(output_file)
                         writer.writerow(data)
else:
     print ("The Filename you entered is not valid, please do again.....")
     exit