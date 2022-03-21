import requests
import json
import os
from datetime import datetime
from datetime import date
from time import sleep
import csv

# Define the test name
name = 'mytest'

# API Key
api_key = ''

path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
file_path_csv = os.path.join(path, f"{name}.csv")
file_path_urls = os.path.join(path, 'urls.txt')

# Check if {name}.csv file exists by trying to open it.
try:
    csvfile = open(file_path_csv)
    print(f'\nThe file {name}.csv was found. Results will be appended to it.')

# If the file doesn't exist, create it and add in the header row.
except IOError:
    with open(f'{file_path_csv}', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow(['Date','Time','URL','Platform','Score','FCP','SI','LCP','TTI','TBT','CLS'])
        print(f'\n{name}.csv created.')

finally:
    csvfile.close()

while True:

    today = date.today().strftime('%d/%m/%Y')
    now = datetime.now().strftime('%H:%M:%S')
    filetime = datetime.today().strftime('%Y%m%d-%H%M%S')

    print('\n================================================================================')
    print(f'{today} {now}: New test for {name}')
    print('================================================================================\n')

    # Open the urls.txt file and loop through each URL
    with open(f'{file_path_urls}') as urlfile:
        for url in urlfile:
            url = url.rstrip('\r\n')
            m_test_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&locale=en&key={api_key}'
            d_test_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=desktop&locale=en&key={api_key}'

            # Run mobile score request
            print(f'Requesting Lighthouse scores for {url}\n')
            result = requests.get(m_test_url).json()

            # Define each mobile metric
            m_score = result['lighthouseResult']['categories']['performance']['score']*100
            m_fcp = result['lighthouseResult']['audits']['first-contentful-paint']['numericValue']/1000
            m_si = result['lighthouseResult']['audits']['speed-index']['numericValue']/1000
            m_lcp = result['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']/1000
            m_tti = result['lighthouseResult']['audits']['interactive']['numericValue']/1000
            m_tbt = result['lighthouseResult']['audits']['total-blocking-time']['numericValue']
            m_cls = result['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']

            print('==========================')
            print('Mobile')
            print('==========================')
            print(f'Score: {m_score}')
            print(f'FCP  : {m_fcp}')
            print(f'SI   : {m_si}')
            print(f'LCP  : {m_lcp}')
            print(f'TTI  : {m_tti}')
            print(f'TBT  : {m_tbt}')
            print(f'CLS  : {m_cls}')
            print('--------------------------\n')

            # Run desktop score request
            result = requests.get(d_test_url).json()
            result_string = json.dumps(result)

            # Define each desktop metric
            d_score = result['lighthouseResult']['categories']['performance']['score']*100
            d_fcp = result['lighthouseResult']['audits']['first-contentful-paint']['numericValue']/1000
            d_si = result['lighthouseResult']['audits']['speed-index']['numericValue']/1000
            d_lcp = result['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']/1000
            d_tti = result['lighthouseResult']['audits']['interactive']['numericValue']/1000
            d_tbt = result['lighthouseResult']['audits']['total-blocking-time']['numericValue']
            d_cls = result['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']

            print('==========================')
            print('Desktop')
            print('==========================')
            print(f'Score: {d_score}')
            print(f'FCP  : {d_fcp}')
            print(f'SI   : {d_si}')
            print(f'LCP  : {d_lcp}')
            print(f'TTI  : {d_tti}')
            print(f'TBT  : {d_tbt}')
            print(f'CLS  : {d_cls}')
            print('--------------------------\n')

            with open(f'{file_path_csv}', mode='a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
                    writer.writerow([today,now,url,'Mobile',m_score,m_fcp,m_si,m_lcp,m_tti,m_tbt,m_cls])
                    writer.writerow([today,now,url,'Desktop',d_score,d_fcp,d_si,d_lcp,d_tti,d_tbt,d_cls])

            print(f'Results saved to {name}.csv.\n\n')
    
    print(f'Keep this window open to run new tests in 1 hour.')

    sleep(3600)