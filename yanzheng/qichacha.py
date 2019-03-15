# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:45:12 2018

@author: win 10
"""

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
from word import get_location   #识别图片验证码，返回文字坐标



if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class Spider(object):

    def __init__(self):
        self.filepath = 'download'
        self.crm_excel_file = 'C:\Users\win7\Desktop\qicc.xlsx'
        #self.crm_excel_file = 'qicc.xlsx'
    
        url = 'https://www.qichacha.com/user_login'

        #chromeOptions = webdriver.ChromeOptions()
        #chromeOptions.add_argument("--proxy-server=http://118.182.33.6:42801")

        #brower = webdriver.Chrome(chrome_options = chromeOptions)
        brower = webdriver.Chrome()
        # brower.maximize_window()
        brower.set_window_size(1600,900)
        brower.get(url)

        brower.find_element_by_xpath('// *[ @ id = "qrcodeLoginPanel"] / div[2] / div / div[3] / a[2]').click()

        brower.switch_to.frame(0)
        brower.find_element_by_id('switcher_plogin').click()
        brower.find_element_by_name('u').send_keys('546454228')
        brower.find_element_by_name('p').send_keys('xxxxxxxxxxxxxxxx')
        brower.find_element_by_id('login_button').click()
        time.sleep(10)
        brower.find_element_by_xpath('//*[@id="bindwxModal"]/div[1]/div[1]/div[1]/button/span').click()
       

        self.brower = brower
    
    #获取excel中的name并加入列表
    def excelData(self):
        excel = xlrd.open_workbook(self.crm_excel_file)
        table = excel.sheets()[0] 
        
        cname_arr = []
        
        # 总行数
        nrows = table.nrows
        for i in range(nrows):
        # for i in range(10):
            #if i == 0:
            #    continue
            cname = table.row_values(i)[0]
            cname_arr.append(cname)
        return cname_arr
    
    
    #print excelData()




    '''搜索公司名并获得搜索后的页面'''
    def searchCompany(self, name):
        brower = self.brower

        #name_arr = self.excelData()

        #search_url = 'https://www.qichacha.com'
        #brower.get(search_url)

        search_url = 'https://www.qichacha.com/search?key=' + str(name)
        brower.get(search_url)


        #brower.find_element_by_xpath('//*[@id="searchkey"]').send_keys(name)
        #brower.find_element_by_xpath('//*[@id="V3_Search_bt"]').click()


        htmlstr = brower.page_source

        return htmlstr



    def getHtml(self, html_name):
        f = open(html_name, 'r')
        #print(f.read())
        return f.read()


    def yanzheng(self):
        brower = self.brower
        click_word = brower.find_element_by_xpath('//*[@id="nc_1__scale_text"]/i').text  # 获取要点击的文字
        click_word = click_word.replace('“', '').replace('”', '')
        click_word = repr(click_word)
        #print click_word

        img = brower.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img').get_attribute("src")  # 获取网页中图片的base64编码
        img = img.replace('data:image/jpg;base64,', '')

        get_location(img, click_word)  # 获取文字位置

        location = get_location(img, click_word)
        #print location
        x = location['left'] * 1.27  # 百度ocr返回的是图片180*180 ， 网页中实际的尺寸是230*230  ，230/180=1.27
        # print x
        y = location['top'] * 1.27
        # print y
        img_element = brower.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img')
        ActionChains(brower).move_to_element_with_offset(img_element, x, y).click().perform()


    
    '''检查搜索的公司名是否完全匹配，并且输出匹配的公司信息网址'''
    def findCompanyHref(self, html, name):
        brower = self.brower
        #html = self.getHtml()
        soup = BeautifulSoup(html, 'lxml')

        '''如果出现验证，等待20s'''
        h = str(soup)
        h = h.find('您的操作过于频繁，验证后再操作')
        if h >= 0:
            source = brower.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            ActionChains(brower).drag_and_drop_by_offset(source, 308, 0).perform()  # 滑动滑块
            time.sleep(2)
            #source = brower.find_element_by_id("nc_1_n1z")
            #ActionChains(brower).drag_and_drop_by_offset(source,500,0).perform()
            #self.yanzheng()
            #exit()
            try:
                self.yanzheng()
            except:
                self.yanzheng()


            '''
            while True:
                try:
                    self.yanzheng()
                except:
                    print 'noooo'
                    continue
                else:
                    print 'ok'
                    break
            '''

        #name = '<em>%s</em>' % name

        com_list = soup.select('.m_srchList')[0]
        #print com_list.tbody.tr.encode('gb2312')
        #find_name = com_list.tbody.tr.select('td')[1].a.em.em.string.encode('gb2312')
        #find_name = com_list.tbody.tr.select('td')[2].a
        find_tbody = com_list.tbody.select('tr')[0].select('td')[1].a.strings
        find_name = ''
        for ii in find_tbody:
            find_name +=ii
        #print name
        #print find_name

        if str(name) == str(find_name):
            # company_url = com_list.tbody.tr.select('td')[1].a['href'].encode('gb2312')
            company_url = com_list.tbody.tr.select('td')[1].a['href']
            address = 'https://www.qichacha.com' + company_url
            return address
        else:
            return False
                
    
    def saveHtml(self, html, name, html_name):
        address = self.findCompanyHref(html, name)
        brower = self.brower
        brower.get(address)
        htmlstr = brower.page_source

        #File = open('./download/' + str(html_name),'wb')
        File = codecs.open('C:\\Users\\win7\\Desktop\\download\\' + str(html_name),'wb','utf-8')
        File.write(htmlstr)
        File.flush()
            
    def main(self):
        company_arr = self.excelData()
        n=0
        for com in company_arr:
            #html_name=str(n) + '.html'
            html = self.searchCompany(com)

            try:
                match = self.findCompanyHref(html, com)
            except IndexError:
                match = False
                #time.sleep(20)


            if match == False:
                print com
                continue

            #html_name = str(com).encode('gb2312') + '.html'
            try:
                html_name = str(com).encode('gb2312') + '.html'
            except UnicodeEncodeError:
                f=open('C:\\Users\\win7\\Desktop\\char_error.txt','a')
                f.write(str(com).encode('gb18030')+'\n')
                f.close()
                continue

            #html_name = str(com) + '.html'
            self.saveHtml(html, com, html_name)
                #n +=1

if __name__ == "__main__":
    s = Spider()
    s.main()
    #s.findCompanyHref('国药控股国大药房有限公司')
    #s.searchCompany(u'国药控股国大药房有限公司')
    #s.saveHtml('x.html',htmlstr)
    







