#!/usr/bin/python3

#Unix Programming-COMP20200 Assignment 5
#Author: Shane Malone
#Student Number: 17308336

#Usage
#-l followed by filename is the log file to process
#-n gives number of unique IP addresses in log file
#-t list top N IP addresses ny requests
#-L list all requests by a particular IP
#-d List all requests on a given date in ddMMMyyyy format

import getopt
import sys
import re
from collections import Counter
from heapq import nlargest
import socket



options, remainder = getopt.getopt(sys.argv[1:] , 'l:nt:v:L:d:')
regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' #Matches format of an ip address

#Read IP addresses from log file and make a list
def ip_reader(filename):
	with open(filename) as f:
		ip_list = []
		for line in f:
			split = line.split()
			ip_list.append(split[0])
		i = 0
		#If we have found an invalid IP address remove it
		for pattern in ip_list:
			try:
				socket.inet_aton(pattern)
			except socket.error:
				ip_list.pop(i)
			i+=1
		return(ip_list)

#Count appearances of IPs in list
def count(ip_list):
	visits = Counter(ip_list)
	key = '::1' #ensures leftover string removed from dictionary
	if key in visits:
		visits.pop(key)
	return visits

#Number of requests by given IP
def num_request(address):
	for key, value in visits.items():
		if key == address:
			print('Number of requests: ', value)

#Prints top N ip addresses by number of requests			
def top_IP(N):
	print('IP \t Number of Requests')
	largest = nlargest(N, visits, key=visits.get)
	for i in largest:
		print(i, '	', visits[i])

#searches the log file for all lines with given IP and prints them
def file_search(key, filename):
	with open(filename) as search:
		for line in search:
			if key in line:
				print(line)

#Prints number of requests by each IP on a given date
def date_search(date, filename):
	ip_list_d = []
	s = " "
	with open(filename) as search:
		for line in search:
			if date in line:
				split = line.split()
				ip_list_d.append(split[0])
	visits_d = count(ip_list_d)
	print('IP \t\t Number of Requests')
	for key, value in visits_d.items():
		print(key, '\t\t', value)


if __name__ == "__main__":
	#Parses input line checking for options
	for opt, arg in options:
		if opt in '-l':
			filename = arg
			visits = count(ip_reader(filename))

		elif opt in '-n':
			print('We have ', len(visits), 'IP Addresses')

		elif opt in '-t':
			N = int(arg)
			top_IP(N)

		elif opt in '-v':
			num_request(arg)

		elif opt in '-L':
			address = arg
			file_search(address, filename)

		elif opt in '-d':
			date = arg[:2] + '/' + arg[2:5] + '/' + arg[5:9] #Match format of date in the file
			date_search(date, filename)
			
