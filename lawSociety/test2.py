import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    index_errors = []
    starting_index = 50912  

    # Read the SRA numbers from file
    with open("all_sra_numbers.txt", "r", encoding="utf-8") as file:
        sra_numbers = [line.strip() for line in file.readlines()]  # Strip to remove newline characters

    total_records = len(sra_numbers)
    logging.info(f"Starting scraper from index {starting_index} of {total_records}")

    for x in range(starting_index, total_records):
        logging.info(f"Processing index {x} - SRA Number: {sra_numbers[x]}")
        time.sleep(1)  # Delay to prevent bot detection

        try:
            # Open the webpage
            driver.get(f"https://solicitors.lawsociety.org.uk/search/results?Pro=True&Type=1&Name={sra_numbers[x]}")

            # Wait for results section to be present
            wait = WebDriverWait(driver, 30)  # Set a reasonable timeout
            results_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-outer")))

            # Get the HTML content
            search_results_html = results_section.get_attribute("outerHTML")

            # Save the HTML content to a file
            file_path = f'./data-html/{sra_numbers[x]}.html'
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(search_results_html)

            logging.info(f"Saved HTML data for {sra_numbers[x]} at {file_path}")

        except Exception as e:
            logging.error(f"Error at index {x} (SRA: {sra_numbers[x]}): {e}")
            index_errors.append(x)

finally:
    # Log and print error indices
    if index_errors:
        logging.warning(f"Encountered errors at indices: {index_errors}")
        with open("failed_indices.txt", "w") as f:
            f.write("\n".join(map(str, index_errors)))

    logging.info("Scraper finished. Closing browser.")
    driver.quit()
