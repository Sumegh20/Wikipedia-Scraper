# doing necessary imports
import threading
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin  # It is required when we deploy it in any kind of cloud environment
import pandas as pd
from mongoDBOperations import MongoDBManagement  # User define classes
#from FlipkratScrapping import FlipkratScrapper   # User define classes
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import wikipedia as wiki
from selenium.webdriver.common.keys import Keys
import urllib

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)

# Go to the wikipedia page and search the anything and click the search button
driver.get('https://www.wikipedia.org/')
search = driver.find_element_by_xpath('/html/body/div[3]/form/fieldset/div/input')
search_button = driver.find_element_by_xpath("/html/body/div[3]/form/fieldset/button")
search.send_keys('Linear_Regression')
search_button.click()
# End

# Find images and stores them in a file
images = driver.find_elements_by_tag_name('img')
for i,image in enumerate(images):
    src = image.get_attribute('src')
    if src[-3:] in ['png', 'jpg']:
        urllib.request.urlretrieve(src, f"imgs/{i}.png")
# End

# Find ref links and stores them in a file
# groups = driver.find_element_by_class_name('reflist')
# links = groups.find_elements_by_tag_name('a')
# for link in links:
#     href = link.get_attribute('href')
#     if "#" not in href:
#         print(href)
# End

# Summary of a wiki page using wikipedia library
# result = wiki.summary("Linear Regression", sentences = 5)
# result = result.replace(".", '\n')
# print(result)
# End

# abcd = open('wiki.txt','w', encoding='utf-8')
# abcd.write(driver.find_element_by_tag_name("body").text)
# abcd.close()
#
# # importing libraries
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
#
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize, sent_tokenize
#
# # Input text - to summarize
# text = driver.find_element_by_tag_name("body").text
#
# # Tokenizing the text
# stopWords = set(stopwords.words("english"))
# words = word_tokenize(text)
#
# #Creating a frequency table to keep the
# #score of each word
#
# freqTable = dict()
# for word in words:
#     word = word.lower()
#     if word in stopWords:
#         continue
#     if word in freqTable:
#         freqTable[word] += 1
#     else:
#         freqTable[word] = 1
#
# # Creating a dictionary to keep the score
# # of each sentence
# sentences = sent_tokenize(text)
# sentenceValue = dict()
#
# for sentence in sentences:
#     for word, freq in freqTable.items():
#         if word in sentence.lower():
#             if sentence in sentenceValue:
#                 sentenceValue[sentence] += freq
#             else:
#                 sentenceValue[sentence] = freq
#
# sumValues = 0
# for sentence in sentenceValue:
#     sumValues += sentenceValue[sentence]
#
# # Average value of a sentence from the original text
#
# average = int(sumValues / len(sentenceValue))
#
# # Storing sentences into our summary.
# summary = ''
# for sentence in sentences:
#     if (sentence in sentenceValue) and (sentenceValue[sentence] > (2 * average)):
#         summary += " " + sentence
# print(summary)


