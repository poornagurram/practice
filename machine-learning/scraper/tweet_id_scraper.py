from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

tweet_data = pd.read_csv("C:\\Users\Prudhvi\\Downloads\\hatespeechtwitter.csv")
tweet_ids = list(tweet_data['tweet_id'])
browser = webdriver.Chrome(executable_path=u'C:\\Users\Prudhvi\\Downloads\\chromedriver_win32\\chromedriver.exe')
tweet_text = []

for tid in tweet_ids[:5]:
    url = f'https://twitter.com/anyuser/status/{tid}'
    time.sleep(2)
    browser.get(url)
    time.sleep(1)
    tweets = browser.find_elements_by_xpath("//*[@id=\"react-root\"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[1]")
    if tweets:
        for tweet in tweets:
            tweet_text.append(tweet.text)
    else:
        tweet_text.append('NaN')

tweet_data['tweet_text'] = pd.Series(tweet_text)
tweet_data.to_csv("hate_speech_data.csv")
