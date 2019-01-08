# coding:utf-8
import urllib, urllib2, base64, sys
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time, datetime, os, sys
#import requests
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import xlrd
#import xlwt
#from urllib import parse
import urllib
import codecs
import chardet
from word import get_location

'''测试企查查登录界面验证'''

reload(sys)
sys.setdefaultencoding('utf-8')


#click_word = '\u62a2'
#img = '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'
#lo(img,click_word)
#exit()

def yanzheng():
    url = 'https://www.qichacha.com/user_login'

    # brower = webdriver.Chrome(chrome_options = chromeOptions)
    brower = webdriver.Chrome()
    # brower.maximize_window()
    brower.set_window_size(1600, 900)
    brower.get(url)

    brower.find_element_by_xpath('//*[@id="normalLogin"]').click()


    time.sleep(3)
    source = brower.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    ActionChains(brower).drag_and_drop_by_offset(source,308,0).perform()    #滑动滑块

    time.sleep(2)

    click_word = brower.find_element_by_xpath('//*[@id="nc_1__scale_text"]/i').text  #获取要点击的文字
    click_word = click_word.replace('“','').replace('”','')
    click_word = repr(click_word)
    #print click_word

    img = brower.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img').get_attribute("src")   #获取网页中图片的base64编码
    img = img.replace('data:image/jpg;base64,','')

    get_location(img,click_word)   #获取文字位置

    location = get_location(img,click_word)
    #print location
    x = location['left']*1.27       #百度ocr返回的是图片180*180 ， 网页中实际的尺寸是230*230  ，230/180=1.27  应该是屏幕分辨率的原因
    #print x
    y = location['top']*1.27
    #print y
    img_element = brower.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img')
    ActionChains(brower).move_to_element_with_offset(img_element, x, y).click().perform()

    brower.find_element_by_xpath('//*[@id="user_login_normal"]/button').click()



while True:
    try:
        yanzheng()
    except:
        continue
    else:
        break













