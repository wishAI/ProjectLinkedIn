import requests as req

# /seeMoreJobPostings + start
start = 500;
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Programmer&location=%E6%B8%A9%E5%93%A5%E5%8D%8E%2C%20BC&trk=guest_homepage-basic_jobs-search-bar_search-submit&redirect=false&position=3&pageNum=0&currentJobId=1902479105&start=' + str(start)

res = req.get(url, headers = headers)
print(res)
print(res.text)