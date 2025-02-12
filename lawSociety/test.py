from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()

try:

    index_errors = []
    starting_index = 32211

    with open("all_sra_numbers.txt", 'r', encoding='utf-8') as file:

        sra_numbers = file.readlines()
        
        for x in range(starting_index, len(sra_numbers)):
            print(f"last index:{x} of {len(sra_numbers)}")
            time.sleep(1)
                        # Open the webpage
            driver.get(f"https://solicitors.lawsociety.org.uk/search/results?Pro=True&Type=1&Name={sra_numbers[x]}")  

            
            try:# Wait for the input field to be visible
                wait = WebDriverWait(driver, 120)  # Timeout of 10 seconds


                # search_input = wait.until(EC.visibility_of_element_located((By.ID, "Pro_Name")))
                
                # search_input.send_keys(sra_numbers[x])

                # search_button = wait.until(EC.element_to_be_clickable((By.ID, "submitsearch")))

                # time.sleep(1)
                # # Click the search button
                # search_button.click()

                # Wait for search results to load (Modify selector if needed)
                results_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-outer")))

                # Get the HTML of the search results
                search_results_html = results_section.get_attribute('outerHTML')

                # Print or process the extracted HTML snippet
                with open(f'./data-html/{sra_numbers[x]}.html', 'w') as file:
                    file.write(search_results_html)
            except Exception as e:
                print(e)
                index_errors.append(x)
                


finally:
    # Close the browser
    for x in index_errors:
        print(x)
    driver.quit()
