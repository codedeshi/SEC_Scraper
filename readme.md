
# Python Version: Python 2.7

# Packages requred:
- requests
- bs4 : BeautifulSoup
- re
- sys
- os.path

# Summary:
This scraper allows the user to pull 13F- HR fillings for any particular fund using its CIK ticker> 13F-HR filling is filled by mutual funds every quarter to report their holdings. This scraper access these filings on SEC website and saves the holdings data into a text file. By defualt the crawler is set to pull the latest report for the given ticker however it allows the user to pull multiple ticker and multiple reports for a single ticker with single command.

The data can be pulled straight from the command prompt:
- To pull a single file for a fund: 							python crawler.py <CIK>
- To pull several funds at the same time:  				python crawler.py <CIK1> <CIK2> . . .
- To pull multiple/historical reporting: 					python crawler.py <CIK1> -n <number of filing you want to pull>
- To pull multiple filings for multiple tickers:	python crawler.py <CIK1> -n <number of filings1> <CIK2> -n <number of filings2>
- Can also do: 																		python crawler.py <CIK1> -n <number of filings> <CIK2>
	(this will pull the specified number of filings for CIK1 but will pull only the latest filing for CIK2 )


# Some inconsistencies in the reporting strucutre:
I found two kinds of inconsistencies:

	1) Some tickers have a prefix ns1: attached to all the tags in the XML. I used a regex to pull data for tags that end with infotable to manage such edge cases. However, to maintain consistency in headings across all the files I removed the prefixes while writing the headings.

	2) Some tickers have additional columns. To manage such edge cases I used a recursive approach to extract columns heading from the data so all available headings are included. I prioritized capturing all columns over the consistency of data across tickers in this case. 