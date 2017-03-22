import requests
from bs4 import BeautifulSoup
import re
import sys
import os.path

ticker = ''

def get_filings(ticker,filings):
	print '*' * 100
	print 'Starting CIK' , ticker
	print '*' * 100
	# Using the URL to filter for 13F-HR fillings
	url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&count={}'.format(ticker,filings)
	search_result = requests.get(url)
	soup = BeautifulSoup(search_result.text,'html.parser')
	# Using document button id to get to the document page as the result is already filtered for 13F-HR fillings.
	filing_urls = soup.findAll('a', {'id': 'documentsbutton'})[:filings]
	if len(filing_urls) == 0:
		print 'Could not find any 13F filings for this Fund'
		print '-' * 100
		return False
	for url in filing_urls:
		print 'Getting ' , url['href']
		get_info_table(url)

def get_info_table(url):
	file_url = 'https://www.sec.gov' + url.get('href').replace('-index.htm','.txt')
	file_soup = BeautifulSoup(requests.get(file_url).content,'html.parser')
	# some tickers have a prefix ns1: added to the tags so using regex to managed that 
	info_table = file_soup.find_all(re.compile('\infotable$'))

	if len(info_table) <= 0:
		print	'No data available at this url'
		print '-' * 100
		return False
	filing_period = file_soup.find_all('periodofreport')[0].string
	file_name = ticker + '_' + filing_period + '.txt'

	# to save only the latest filling or ammendment for a particular period checking of see if the file already exists
	if os.path.exists(file_name):
		print 'File aredly exists. This may be because latest amemedment alredy saved for this period'
		print '-' * 100
		return False
	write_data(info_table,file_name)

def write_data(info_table,file_name):
	print 'Writing data'
	output_file = open(file_name,'w')
	headings = get_column_headings(info_table[0])
	
	# writing column headings to the txt file without any prefixes to maintian consistency across all tickers
	for heading in headings:
		output_file.write('{}\t'.format(re.sub('(.*?)\:',"",heading)))

	# removing main heading perfix from sub headings so we can use sub headings directly to look for data in the info_table.
	headings = [heading.split('_',1)[1] if '_' in heading else heading for heading in headings] 
	
	for data in info_table:
		output_file.write('\n')
		for heading in headings:
			# Some tickers have specific fields missing only from certain rows so using try except to manage the edge cases
			# E.g. For CIK 0001034771 Nike appears twice but second time it doesnt have the field othermanager in the xml
			try:
				output_file.write('{}\t'.format(data.find_all(heading)[0].string))
			except:
				output_file.write(' \t')	
	output_file.close()
	print 'File saved'
	print '-' * 100

#recursive algorithm to capture all column headings irrespective of fillings format
def get_column_headings(data):
	headings = []
	for i in data:
		if i.name == None:
			pass
		elif i.name != None and len(i)==1:
			headings.append(str(i.name))
		else:
			# adding the main heading prefix so that the page heading shows mainHeading_subHeading if there are sub-headings
			headings.extend([i.name + '_' + j for j in get_column_headings(i)])
	return headings

args = 1

while args < len(sys.argv):
	try:
		nxt = sys.argv[args+1]
	except:
		nxt = None

	if nxt == '-n':
		ticker = sys.argv[args]
		number_of_filings = int(sys.argv[args + 2])
		get_filings(ticker, number_of_filings)
		args += 3
	else:
		ticker = sys.argv[args]
		get_filings(ticker,1)
		args += 1

