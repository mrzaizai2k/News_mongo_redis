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
from bs4 import BeautifulSoup as Soup

from src.utils import check_path, take_device

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    RecursiveUrlLoader,
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

import warnings
import contextlib

import requests
from urllib3.exceptions import InsecureRequestWarning
from transformers import AutoFeatureExtractor, ResNetForImageClassification
import torch
import os
old_merge_environment_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass
            



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
    def __init__(self, max_depth:int = 2, 
                    root_urls:list = ["https://znews.vn/", "https://cafef.vn/"]):
        
        self.max_depth = max_depth
        self.root_urls = root_urls
        self.formatted_docs = []


    def search_news(self)-> list : 
        docs = [] 
        for url in self.root_urls:
            print ('Crawling url:', url)
            loader = RecursiveUrlLoader(
                url=url, max_depth=self.max_depth, 
                extractor=lambda x: Soup(x, "html.parser").text,
                prevent_outside =True, 
            )
            with no_ssl_verification():
                docs.extend(loader.load())

        return docs


    def extract_urls(self, docs):
        # Step 2: Initialize an empty list to store the extracted URLs
        news_url_list = []
        
        # Step 3: Loop through each document in the 'docs' list
        for doc in docs:
            url = doc.metadata['source']
            extension = url.split('.')[-1].lower()
            
            if  (extension in ['html', 'chn']) and (len(url)  > 50 ):
            
                # Step 6: Append the extracted URL to the 'news_url_list'
                news_url_list.append(url)

        return news_url_list
    
    
    def take_news_elements(self, news_url:str) -> str :
        news_url = [news_url]
        loader = NewsURLLoader(urls=news_url, 
                            post_processors=[clean_extra_whitespace],)
        with no_ssl_verification():
            news = loader.load()
        return news

    def take_text_from_link(self, news_url:str) -> str :
        news = self.take_news_elements(news_url)
        news_text = news[0].page_content
        return  news_text
    
    def get_all_news(self):
        docs = self.search_news()
        news_url_list = self.extract_urls(docs)
        for url in news_url_list:
            news = self.take_news_elements(url)
            self.formatted_docs.append(news)
        return self.formatted_docs

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

    news_scraper = NewsScraper()
    formatted_docs = news_scraper.get_all_news()
    print(formatted_docs[2][0].page_content)
    print(formatted_docs[2][0].metadata)
