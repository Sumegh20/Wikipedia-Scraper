from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")

class WikipediaScrapper:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__) : Something went wrong on installing the chrome driver")

    def openUrl(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            raise Exception(f"(openUrl) : Something went wrong to open the url")

    def getTheSearchPage(self, searchString):
        try:
            search = self.driver.find_element_by_xpath('/html/body/div[3]/form/fieldset/div/input')
            search_button = self.driver.find_element_by_xpath("/html/body/div[3]/form/fieldset/button")
            search.send_keys(searchString)
            search_button.click()
        except Exception as e:
            raise Exception(f"(getTheSearchPage) : Something went wrong to get the search page")

    def getAllImages(self):
        try:
            images_list = []
            images = self.driver.find_elements_by_tag_name('img')
            for image in images:
                src = image.get_attribute('src')
                if src[-3:] in ['png', 'jpg']:
                    images_list.append(src)
            return images_list
        except Exception as e:
            raise Exception(f"(getAllImages) : Something went wrong to get the images")

    def getAllReferencesLinks(self):
        try:
            references_list = []
            groups = self.driver.find_element_by_class_name('reflist')
            links = groups.find_elements_by_tag_name('a')
            for link in links:
                href = link.get_attribute('href')
                if "#" not in href:
                    references_list.append(href)
            return references_list
        except Exception as e:
            raise Exception(f"(getAllReferencesLinks) : Something went wrong to get the images")

    def getAllText(self):
        try:
            text = self.driver.find_element_by_tag_name("body").text
            return text
        except Exception as e:
            raise Exception(f"(getAllText) : Something went wrong to get the text")

    def getTextSummary(self):
        try:
            # Input text - to summarize
            text = self.getAllText()

            # Tokenizing the text
            stopWords = set(stopwords.words("english"))
            words = word_tokenize(text)

            # Creating a frequency table to keep the score of each word
            freqTable = dict()
            for word in words:
                word = word.lower()
                if word in stopWords:
                    continue
                if word in freqTable:
                    freqTable[word] += 1
                else:
                    freqTable[word] = 1

            # Creating a dictionary to keep the score of each sentence
            sentences = sent_tokenize(text)
            sentenceValue = dict()

            for sentence in sentences:
                for word, freq in freqTable.items():
                    if word in sentence.lower():
                        if sentence in sentenceValue:
                            sentenceValue[sentence] += freq
                        else:
                            sentenceValue[sentence] = freq

            sumValues = 0
            for sentence in sentenceValue:
                sumValues += sentenceValue[sentence]

            # Average value of a sentence from the original text
            average = int(sumValues / len(sentenceValue))

            # Storing sentences into our summary.
            summary = ''
            for sentence in sentences:
                if (sentence in sentenceValue) and (sentenceValue[sentence] > (2 * average)):
                    summary += " " + sentence
            return summary
        except Exception as e:
            raise Exception(f"(getSummary) : Something went wrong on the summarizing text")

    def getResultDict(self,searchString):
        try:
            result_dict = {"Topic": searchString,
                           "Images": self.getAllImages(),
                           "References": self.getAllReferencesLinks(),
                           "Summary_text": self.getTextSummary()
                           }
            return result_dict
        except Exception as e:
            raise Exception(f"(getResultDict) : Something went wrong on creating dic")