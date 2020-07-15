from pyquery import PyQuery as pq
import requests as req
import xlsxwriter

jobs = ['Analyst', 'Admin', 'Assistant', 'Junior', 'New Grads', 'Entry Level']
job = 'Programmer'



url_linkedin = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=$key$&location=vancouver&trk=public_jobs_jobs-search-bar_search-submit&f_JT=F%2CT%2CC&f_TP=1%2C2&redirect=false&position=1&pageNum=0&start='

# domain = 'https://ca.linkedin.com'
# path = '/jobs-guest/jobs/api/seeMoreJobPostings/search'
# keywords = '?keywords=' + job
# location = '&location=%E6%B8%A9%E5%93%A5%E5%8D%8E%2C%20BC'
# trk = '&trk=guest_homepage-basic_jobs-search-bar_search-submit'
# other = '&redirect=false&pageNum=0&start='

# template = domain + path + keywords + location + trk + other

# make a fake browser agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

results = []

def search_by_keyword(keyword):
    start = 0
    while start < 20000:
        # build url and get response
        url = url_linkedin.replace('$key$', keyword) + str(start)
        print(url)
        # url = template + str(start)
        res = req.get(url, headers = headers)
        if res.status_code != 200 or len(res.text) == 0:
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
            # href = card('.result-card__full-card-link').attr('href')
            
            # add card to results
            row = (title, subtitle, location, time, href)
            print(row)
            results.append(row)
        
        start += cards.size()


search_by_keyword('Assistant')


# remove unsatified results
print('')
print('')
print('Found ', len(results), ' records, start filtering.')
def is_satisfied(result):
    loc = result[2]
    if ('Delta' in loc) or ('Surrey' in loc) or ('delta' in loc) or ('surrey' in loc):
        return False
    return True
results = list(filter(is_satisfied, results))
print(len(results), ' records after filtering.')

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