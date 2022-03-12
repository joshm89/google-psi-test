from datetime import datetime
from datetime import date
import csv
import json
import requests

# Define the website name as a single word, e.g. mywebsite. This name is used as part of the csv output filename.
name = 'mywebsite'

# Define the URL to test
url = 'https://www.blacktomato.com/'

# Set the API key. You can get one here: https://developers.google.com/speed/docs/insights/v5/get-started
api_key = 'AIzaSyBm86iApbEJNtNaAFs40LN9LVP5e2Fm5RY'

# Create the desktop and mobile test URLs
m_test_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&locale=en&key={api_key}'
d_test_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=desktop&locale=en&key={api_key}'

today = date.today().strftime('%d/%m/%Y')
now = datetime.now().strftime('%H:%M:%S')
filetime = datetime.today().strftime('%Y%m%d-%H%M%S')

# Check if {name}.csv file exists by trying to open it.
try:
        csvfile = open(f'{name}.csv')

# If the file doesn't exist, create it and add in the header row.
except IOError:
        with open(f'{name}.csv', mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
                writer.writerow(['Date','Time','Platform','Score','FCP','SI','LCP','TTI','TBT','CLS'])

finally:
        csvfile.close()

print(f'\n\nRequesting mobile PSI Score for {url}\n')

# Run mobile score request
result = requests.get(m_test_url).json()
result_string = json.dumps(result)

with open(f'{name}-mobile-{filetime}.json', 'w') as file:
        file.write(result_string)

# Score
m_score = result['lighthouseResult']['categories']['performance']['score']*100
m_fcp = result['lighthouseResult']['audits']['first-contentful-paint']['numericValue']/1000
m_si = result['lighthouseResult']['audits']['speed-index']['numericValue']/1000
m_lcp = result['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']/1000
m_tti = result['lighthouseResult']['audits']['interactive']['numericValue']/1000
m_tbt = result['lighthouseResult']['audits']['total-blocking-time']['numericValue']
m_cls = result['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']

print(f'Mobile Score: {m_score}')
print(f'Mobile FCP: {m_fcp}')
print(f'Mobile SI: {m_si}')
print(f'Mobile LCP: {m_lcp}')
print(f'Mobile TTI: {m_tti}')
print(f'Mobile TBT: {m_tbt}')
print(f'Mobile CLS: {m_cls}\n')

print(f'Requesting desktop PSI Score for {url}\n')

# Run desktop score request
result = requests.get(d_test_url).json()
result_string = json.dumps(result)

with open(f'{name}-desktop-{filetime}.json', 'w') as file:
        file.write(result_string)

# Score
d_score = result['lighthouseResult']['categories']['performance']['score']*100
d_fcp = result['lighthouseResult']['audits']['first-contentful-paint']['numericValue']/1000
d_si = result['lighthouseResult']['audits']['speed-index']['numericValue']/1000
d_lcp = result['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']/1000
d_tti = result['lighthouseResult']['audits']['interactive']['numericValue']/1000
d_tbt = result['lighthouseResult']['audits']['total-blocking-time']['numericValue']
d_cls = result['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']

print(f'Desktop Score: {d_score}')
print(f'Desktop FCP: {d_fcp}')
print(f'Desktop SI: {d_si}')
print(f'Desktop LCP: {d_lcp}')
print(f'Desktop TTI: {d_tti}')
print(f'Desktop TBT: {d_tbt}')
print(f'Desktop CLS: {d_cls}\n\n')

with open(f'{name}.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow([today,now,'Mobile',m_score,m_fcp,m_si,m_lcp,m_tti,m_tbt,m_cls])
        writer.writerow([today,now,'Desktop',d_score,d_fcp,d_si,d_lcp,d_tti,d_tbt,d_cls])

print('CSV file updated. Request complete.')