import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from googletrans import Translator
import os
import json

# Set up ChromeDriver path
chrome_driver_path = r"C:\Users\Dell\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Function to scrape the first 5 articles from the Opinion section
def scrape_opinion_articles():
    url = 'https://elpais.com/opinion'  # URL for the Opinion section
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Scrape article titles and content
    articles = driver.find_elements(By.CSS_SELECTOR, 'article a')[:5]  # Get first 5 articles

    article_data = []
    for article in articles:
        title = article.text
        link = article.get_attribute('href')
        
        driver.get(link)
        time.sleep(3)  # Wait for the article page to load
        
        content = driver.find_element(By.CSS_SELECTOR, 'div.article-body').text
        image_url = driver.find_element(By.CSS_SELECTOR, 'img.article-image').get_attribute('src') if driver.find_elements(By.CSS_SELECTOR, 'img.article-image') else None
        
        article_data.append({
            'title': title,
            'content': content,
            'image_url': image_url
        })

    return article_data

# Function to translate titles to English
def translate_titles(article_data):
    translator = Translator()
    for article in article_data:
        article['translated_title'] = translator.translate(article['title'], src='es', dest='en').text
    return article_data

# Function to analyze repeated words in translated titles
def analyze_repeated_words(article_data):
    words = []
    for article in article_data:
        words.extend(article['translated_title'].split())

    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

    repeated_words = {word: count for word, count in word_count.items() if count > 2}
    return repeated_words

# Save the scraped data into a JSON file
def save_data_to_json(article_data):
    with open('scraped_data.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)

# Main function to run the script
def main():
    article_data = scrape_opinion_articles()
    article_data = translate_titles(article_data)
    repeated_words = analyze_repeated_words(article_data)

    # Print results
    print("Translated Titles:")
    for article in article_data:
        print(f"Title: {article['translated_title']}")
    
    print("\nRepeated Words in Translated Titles:")
    for word, count in repeated_words.items():
        print(f"{word}: {count}")

    # Save data to JSON
    save_data_to_json(article_data)

# Run the script
if __name__ == "__main__":
    main()

# Close the WebDriver after completion
driver.quit()
