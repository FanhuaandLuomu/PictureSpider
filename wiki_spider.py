# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import urllib2
import urllib
from lxml import etree
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector
import time

def get_html(browser,url):
	browser.get(url)
	time.sleep(2)
	html=browser.page_source
	return html

def get_labels(html):
	page=etree.HTML(html)
	hrefs=page.xpath('//*[@id="mw-pages"]/div/div/div/ul/li/a')
	print len(hrefs)
	href_list=[]
	title_list=[]
	for href in hrefs:
		h=website+href.attrib['href']
		t=href.attrib['title']
		# print h,t
		href_list.append(h)
		title_list.append(t)
	return href_list,title_list 

def get_each_href(browser,path,href,title):
	html=get_html(browser,href)
	page=etree.HTML(html)
	hrefs=page.xpath('//pre')
	print len(hrefs)
	content_list=[]
	for href in hrefs:
		# print href.text
		content_list.append(href.text)
	create_folder_and_save(path,content_list,title.split(':',1)[-1].replace(r'/','')+'.txt')

def create_folder_and_save(path,content_list,filename):
	if not os.path.exists(path):
		os.mkdir(path)
	print path+os.sep+filename
	f=open(path+os.sep+filename,'w')
	# print len(content_list)
	# print content_list[0]
	text='\n'.join(content_list)
	f.write(text)
	f.close()
	print '%s load success...' %(filename)
		
def main():
	global website
	website='https://zh.wikipedia.org'
	url = u'https://zh.wikipedia.org/wiki/Category:人物信息框模板'
	browser = webdriver.Firefox()
	html=get_html(browser,url)
	href_list,title_list=get_labels(html)
	print len(href_list),len(title_list)
	path='wiki_template'
	# get_each_href(browser,path,href_list[0],title_list[0])
	for i in range(len(href_list)):
		try:
			get_each_href(browser,path,href_list[i],title_list[i])
		except Exception,e:
			print 'sth err...in %s' %(title_list[i])
			continue
	browser.close()

if __name__ == '__main__':
	main()