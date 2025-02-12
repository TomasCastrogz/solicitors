# col-md-8 article articles-floated 

from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_requests_session():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--enable-javascript')
    # chrome_options.add_argument('auto-open-devtools-for-tabs')
    chrome_options.add_argument('--window-size=1920,1080')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    driver.get('https://solicitors.lawsociety.org.uk/search/results?Pro=True&Type=1')
    # button = WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.ID, 'ccc-recommended-settings')))
    # button.click()
    # input = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'Quick_Location')))
    # input.send_keys('London, Greater London, EC2V')
    # driver.find_element(By.XPATH, '//div[@id="search-pane-quick"]/form').submit()
    fastoken = WebDriverWait(driver, timeout=120).until(lambda d: d.get_cookie('fastoken'))['value']

    session = requests.Session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'fastoken={}'.format(fastoken),
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    session.headers.update(headers)
    print(session)

    return session



def get_raw_data(url, filename):
    
    session = get_requests_session()
    response = session.get(url)

    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)

        all_details = soup.find('div', class_="search-results-outer")
        time.sleep(1)
        # print(all_details)
        html = all_details.decode_contents()
        text = all_details.get_text(separator="\n", strip=True)
        

        with open(f'./data-text/{filename}.txt', 'w') as file:
            file.write(text)





starting_index = 0


with open("all_urls.txt", 'r', encoding='utf-8') as file:

    urls = file.readlines()
    get_raw_data(urls[0], "paco")
#     for x in range(starting_index, len(urls)):
#         filename = urls[x].split('=')[-1]
#         print(urls[x])
#         print(filename)
#         print(f"last index:{x} of {len(urls)}")
#         get_raw_data(urls[x], filename)

        # print(, x) 
        # a = str(urls[x].split('=')[-1]).strip()
        # if a == "399850":
        #     print(x)
    
    # for url in urls:110639

        