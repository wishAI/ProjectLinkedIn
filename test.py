from pyquery import PyQuery as pq
import requests as req


# TODO: make url dynamic
# TODO: get all pages
url = 'https://www.linkedin.com/jobs/search?keywords=assistant&location=%E7%BE%8E%E5%9B%BD&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'

result = req.get(url)
doc = pq(result.text)

results = doc('.result-card__contents')
# print(doc('.result-card__contents .result-card__title').text())
for result in results.items():
    print(result('.result-card__title').text())
    print(result('.result-card__subtitle').text())
    print(result('.job-result-card__location').text())
    print(result('time').attr('datetime'))
    print('')

url = 'https://www.linkedin.com/jobs/search?keywords=assistant&location=%E7%BE%8E%E5%9B%BD&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=1'

result = req.get(url)
doc = pq(result.text)

results = doc('.result-card__contents')
# print(doc('.result-card__contents .result-card__title').text())
for result in results.items():
    print(result('.result-card__title').text())
    print(result('.result-card__subtitle').text())
    print(result('.job-result-card__location').text())
    print(result('time').attr('datetime'))
    print('')