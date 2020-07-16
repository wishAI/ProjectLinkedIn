from pyquery import PyQuery as pq
import requests as req
import xlsxwriter



# Data Definitions
jobs = ['Analyst', 'Admin', 'Assistant', 'Junior', 'New Grads', 'Entry Level']
job = 'Programmer'
url_linkedin = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=$key$&location=vancouver&trk=public_jobs_jobs-search-bar_search-submit&f_JT=F%2CT%2CC&f_TP=1%2C2&redirect=false&position=1&pageNum=0&start='
url_indeed = 'https://ca.indeed.com/jobs?q=$key$&l=Vancouver%2C+BC&jt=$jt$&fromage=7&start='
jts_indeed = ['fulltime', 'contract', 'temporary']
url_glassdoor = 'https://www.glassdoor.ca/Job/vancouver-$key$-jobs-SRCH_IL.0,9_IC2278756_KO10,19_IP$Page$.htm?jobType=$jt$&fromAge=7&radius=19'
jts_glassdoor = ['fulltime', 'contract', 'temporary']

# make a fake browser agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

results = []



# domain = 'https://ca.linkedin.com'
# path = '/jobs-guest/jobs/api/seeMoreJobPostings/search'
# keywords = '?keywords=' + job
# location = '&location=%E6%B8%A9%E5%93%A5%E5%8D%8E%2C%20BC'
# trk = '&trk=guest_homepage-basic_jobs-search-bar_search-submit'
# other = '&redirect=false&pageNum=0&start='

# template = domain + path + keywords + location + trk + other



# Function Definitions
def search_by_keyword(keyword):
    # print('')
    # print('Fetch linkedin jobs!')
    # print('')
    # start = 0
    # while start < 20000:
    #     # build url and get response
    #     url = url_linkedin.replace('$key$', keyword) + str(start)
    #     res = req.get(url, headers = headers)
    #     if res.status_code != 200 or len(res.text) == 0:
    #         print('No more results.')
    #         break
    #     doc = pq(res.text)
    #     cards = doc('.result-card')

    #     # extract information from html
    #     for card in cards.items():
    #         title = card('.result-card__title').text()
    #         subtitle = card('.result-card__subtitle').text()
    #         location = card('.job-result-card__location').text()
    #         time = card('time').attr('datetime')
    #         href = card('.result-card__full-card-link').attr('href')
            
    #         # add card to results
    #         row = (title, subtitle, location, time, href, 'linkedin')
    #         print(row)
    #         results.append(row)
    #     start += cards.size()

    # print('')
    # print('Fetch Indeed jobs!')
    # print('')
    # for jt in jts_indeed:
    #     start = 0
    #     job_num = 0
    #     count = 0
    #     url_temp = url_indeed.replace('$key$', keyword)
    #     url_temp = url_temp.replace('$jt$', jt)
        
    #     while start < 20000:
    #         url = url_temp + str(start)
    #         res = req.get(url, headers = headers)
    #         doc = pq(res.text)
    #         temp = doc('#searchCountPages').text()
    #         job_num = int(temp.split()[3])
    #         cards = doc('.jobsearch-SerpJobCard')
            
    #         for card in cards.items():
    #             count += 1
    #             title = card('.title a').text()
    #             company = card('.company').text()
    #             location = card('.location').text()
    #             time = card('.date')
    #             href = 'https://ca.indeed.com/' + card('.title a').attr('href')

    #             row = (title, company, location, time, href, 'Indeed')
    #             print(row)
    #             results.append(row)
    #         start += cards.size()
    #         if count >= job_num - 1:
    #             break

    
    print('')
    print('Fetch Glassdoor jobs!')
    print('')
    for jt in jts_glassdoor:
        page_num = 0
        current = 1
        url_temp = url_glassdoor.replace('$key$', keyword)
        url_temp = url_temp.replace('$jt$', jt)

        while current < 2000:
            url = url_temp.replace('$page$', str(current))
            res = req.get(url, headers = headers)
            doc = pq(res.text)
            temp = doc('#ResultsFooter .padVertSm').text()
            page_num = int(temp.split()[3])
            cards = doc('.jobContainer')

            for card in cards.items():
                title = card('.jobEmpolyerName').text()
                subtitle = card.children('a').text()
                location = card('.loc').text()
                href = card.children('a').attr('href')

                row = (subtitle, title, location, '', href, 'glassdoor')
                print(row)
                results.append(row)
            if current >= page_num:
                break
            current += 1


# remove unsatified results
def is_satisfied(result):
    loc = result[2]
    # !!! reversed the logic to in Vancouver, Richmond, and Burnaby
    if ('Vancouver' in loc) or ('Richmond' in loc) or ('Burnaby' in loc):
        return True
    return False            


def linkedin_get_major(href):
    res = req.get(href, headers = headers)
    doc = pq(res.text)
    criterias = doc('.job-criteria__item')
    
    majors = ''
    
    count = 0
    for criteria in criterias.items():
        if count == 3:
            majors = criteria('.job-criteria__text').text()
        count = count + 1

    return majors



# Procedures
# Get all the records by keywords
search_by_keyword('Assistant')
print('')
print('')
print('Found ', len(results), ' records, start filtering.')

results = list(filter(is_satisfied, results))
print(len(results), ' records after filtering.')


# export results
workbook = xlsxwriter.Workbook('results.xlsx')
worksheet = workbook.add_worksheet()

r = 0
worksheet.write(r, 0, 'Company')
worksheet.write(r, 1, 'Job')
worksheet.write(r, 2, 'Major')
worksheet.write(r, 3, 'DDL')
worksheet.write(r, 4, 'Link')

r = 1
for (title, subtitle, location, time, href, site) in results:
    majors = ''
    # if site == 'linkedin':
    #     majors= linkedin_get_major(href)
    worksheet.write(r, 0, subtitle)
    worksheet.write(r, 1, title)
    worksheet.write(r, 2, majors)
    worksheet.write(r, 3, 'None')
    worksheet.write(r, 4, href)
    r += 1
workbook.close()