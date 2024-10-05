from flask import Flask, jsonify, request, render_template  # Changed import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file from the templates folder

@app.route('/scrape', methods=['GET'])
def scrape():
    # Get the PNR from the query parameters
    pnr = request.args.get('pnr')

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the PNR status page
    url = f"https://www.confirmtkt.com/pnr-status/{pnr}"
    driver.get(url)

    # Give time for the JavaScript to load
    time.sleep(5)

    # Find the passenger info container by its ID
    try:
        passenger_info_container = driver.find_element(By.ID, "passenger-info-container")
        # Get the entire table HTML
        table_html = passenger_info_container.get_attribute('innerHTML')
    except Exception as e:
        return jsonify({"error": str(e)})

    # Close the browser
    driver.quit()
    return jsonify({"table": table_html})

if __name__ == '__main__':
    app.run(debug=True, port=8081)  # Keep the port as needed
