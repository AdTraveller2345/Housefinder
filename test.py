from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True  # Run in headless mode
driver = webdriver.Chrome(options=options)

city = "den-bosch"
url = f"https://myhousing.nl"
driver.get(url)

# Wait for JavaScript content to load
time.sleep(5)  # You can also use WebDriverWait for better control

# Save full rendered HTML
with open(f"{city}_rendered_page.html.txt", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
