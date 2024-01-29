import sys
sys.path.append("")

import requests
import re
import time
import random
import json
import urllib3
import ast
from dotenv import load_dotenv
load_dotenv()
import os

urllib3.disable_warnings()
from typing import Literal
from transformers import pipeline
from bs4 import BeautifulSoup
from src.utils import check_path, take_device

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    NewsURLLoader,
)
from unstructured.cleaners.core import clean_extra_whitespace
from langchain.text_splitter import TokenTextSplitter

from langchain_community.llms import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ctransformers import AutoModelForCausalLM, AutoTokenizer
from langchain_openai import OpenAI
from datetime import datetime



class GoogleTranslator:
    def __init__(self):
        pass

    def translate(self, text, to_lang):
        url = 'https://translate.googleapis.com/translate_a/single'

        params = {
        'client': 'gtx',
        'sl': 'auto',
        'tl': to_lang,
        # 'hl': from_lang,
        'dt': ['t', 'bd'],
        'dj': '1',
        'source': 'popup5',
        'q': text
        }
        translated_text = ""
        data = requests.get(url, params=params, verify=False).json()
        sentences = data['sentences']
        for sentence in sentences:
            translated_text += f"{sentence['trans']}\n"
        return translated_text


class NewsScraper:
    '''
    Scape News from https://vnexpress.net/ 
    How to run selenium on linux
    https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2#:~:text=With%20Selenium%20libraries%2C%20Python%20can,using%20Python%20and%20Selenium%20webdriver.
    
    '''
    def __init__(self):
        pass

    def search_stock_news(self, symbol:str = "SSI",
                          date_format:Literal['day', 'week', 'month', 'year']='day')-> list : 
        symbol = symbol.upper()
        url = f"https://timkiem.vnexpress.net/?search_f=&q={symbol}&date_format={date_format}&"

        # Send a GET request to the webpage
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        attemp = 0
        max_attemps = 3
        news_urls = []

        while attemp <= max_attemps:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Assuming the news articles are wrapped in <article> elements
                articles = soup.find_all('article', class_='item-news-common')
                # Iterate through each article and extract the URL
                for article in articles:
                    url = article.get('data-url')
                    if url:
                        news_urls.append(url)

                break
                
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Resetting the Scraper in 10 seconds...")
                time.sleep(10)  
                attemp += 1
                if attemp > max_attemps:
                    print("Max attempts reached. Exiting.")
                    break

        return news_urls

    def search_top_news_cafef(self)-> list:

        url = 'https://cafef.vn/'
        # Send a GET request to the webpage
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        attemp = 0
        max_attemps = 3
        news_urls = []

        while attemp <= max_attemps:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find top news elements
                top_news_elements = soup.find_all('div', class_='top_noibat')
                top_news = top_news_elements[0] if top_news_elements else None

                top_news_links = top_news.find_all('a')
                # Extract and print the links
                for link in top_news_links:
                    news_link = link.get('href')
                    news_link = f'{url}{news_link}'
                    news_urls.append(news_link)

                    # Convert set to list
                    news_urls = list(set(news_urls))
                break
                
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Resetting the Scraper in 10 seconds...")
                time.sleep(10)  
                attemp += 1
                if attemp > max_attemps:
                    print("Max attempts reached. Exiting.")
                    break

        return news_urls
    
    def search_top_news_vnexpress(self)-> list:

        url = 'https://vnexpress.net/kinh-doanh'
        # Send a GET request to the webpage
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        attemp = 0
        max_attemps = 3
        news_urls = []

        while attemp <= max_attemps:
            try:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find news elements
                news_elements = soup.find_all('h3', class_='title_news')
                news_elements.append(soup.find('section', class_='section_topstory_folder'))

                # Extract and return the URLs
                news_urls = [element.find('a').get('href') for element in news_elements if element.find('a')]
                break
                
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Resetting the Scraper in 10 seconds...")
                time.sleep(10)  
                attemp += 1
                if attemp > max_attemps:
                    print("Max attempts reached. Exiting.")
                    break

        return news_urls
    
    def search_top_news(self)-> list:
        news_urls = self.search_top_news_cafef()
        news_urls.extend(self.search_top_news_vnexpress())
        return news_urls
    
    def take_text_from_link(self, news_url:str) -> str :
        news_url = [news_url]
        loader = NewsURLLoader(urls=news_url, 
                            post_processors=[clean_extra_whitespace],)
        news_text = loader.load()
        news_text = news_text[0].page_content
        return  news_text
    

class NewsSummarizer:
    def __init__(self, summarizer = pipeline("summarization", 
                                             model="Falconsai/text_summarization", device = take_device()),
                 translator = GoogleTranslator(),
                 max_length:int=230, 
                 min_length:int=30,
                 ):
        self.summarizer = summarizer
        self.translator = translator
        self.max_length = max_length
        self.min_length = min_length
        
    def summary_text(self,text:str)->str:
        '''Summary short text'''
        sum_text = self.summarizer(text, max_length=self.max_length, 
                                   min_length=self.min_length, do_sample=False)[0]['summary_text']
        return sum_text
    
    def summary_news(self, news:str, chunk_overlap:str = 0)->str:

        text_splitter = TokenTextSplitter(chunk_size=self.max_length * 2,
                                           chunk_overlap=chunk_overlap)
        
        trans_news = self.translator.translate(text=news, to_lang='en')
        text_chunks = text_splitter.split_text(trans_news)
        summary_documents = [self.summary_text(chunk) for chunk in text_chunks]
        summary_text = '\n'.join(summary_documents)

        summary_text = self.translator.translate(text=summary_text, to_lang='vi')
        return summary_text
    

if __name__ == "__main__":

    symbol = 'SSI'
    date_format='year'
    news_scraper = NewsScraper()
    news_list = news_scraper.search_stock_news(symbol=symbol, date_format=date_format)
    news = news_scraper.take_text_from_link(news_url=news_list[0])
    new_summarizer = NewsSummarizer()
    sum_text = new_summarizer.summary_news(news= news)
    