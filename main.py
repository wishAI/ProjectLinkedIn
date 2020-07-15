from pyquery import PyQuery as pq
import requests as req

job = 'Assistant'

domain = 'https://ca.linkedin.com'
path = '/jobs-guest/jobs/api/seeMoreJobPostings/search'
keywords = '?keywords=' + job
location = '&location=%E6%B8%A9%E5%93%A5%E5%8D%8E%2C%20BC'
trk = '&trk=guest_homepage-basic_jobs-search-bar_search-submit'
other = '&redirect=false&pageNum=0&start='
start = 0

url = domain + path + keywords + location + trk + other + str(start)

# make a fake browser agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
