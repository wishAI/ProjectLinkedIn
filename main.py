from pyquery import PyQuery as pq
import requests as req
import xlsxwriter

job = 'Programmer'
max_results = 500

domain = 'https://ca.linkedin.com'
path = '/jobs-guest/jobs/api/seeMoreJobPostings/search'
keywords = '?keywords=' + job
location = '&location=%E6%B8%A9%E5%93%A5%E5%8D%8E%2C%20BC'
trk = '&trk=guest_homepage-basic_jobs-search-bar_search-submit'
other = '&redirect=false&pageNum=0&start='
start = 0

template = domain + path + keywords + location + trk + other

# make a fake browser agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

results = []
while start < max_results:
    # build url and get response
    url = template + str(start)
    res = req.get(url, headers = headers)
    if res.status_code != 200:
        print('No more results.')
        break
    doc = pq(res.text)
    cards = doc('.result-card__contents')

    # extract information from html
    for card in cards.items():
        title = card('.result-card__title').text()
        subtitle = card('.result-card__subtitle').text()
        location = card('.job-result-card__location').text()
        time = card('time').attr('datetime')
        href = card('a').attr('href')
        # print(card('.result-card__full-card-link'))

        # add card to results
        row = (title, subtitle, location, time, href)
        print(row)
        results.append(row)
    
    start += cards.size()


# export results
workbook = xlsxwriter.Workbook('results.xlsx')
worksheet = workbook.add_worksheet()

r = 0
worksheet.write(r, 0, 'Title')
worksheet.write(r, 1, 'Subtitle')
worksheet.write(r, 2, 'Location')
worksheet.write(r, 3, 'Time')
worksheet.write(r, 4, 'Link')
r = 1
for (title, subtitle, location, time, href) in results:
    worksheet.write(r, 0, title)
    worksheet.write(r, 1, subtitle)
    worksheet.write(r, 2, location)
    worksheet.write(r, 3, time)
    worksheet.write(r, 4, href)
    r += 1
workbook.close()