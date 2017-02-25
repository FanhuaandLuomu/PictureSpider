#coding:utf-8
import time
import math
import os
import urllib2
import urllib
from lxml import etree
import threading

def get_html(url):
	html=urllib2.urlopen(url).read()
	return html

def get_labels(html):
	page=etree.HTML(html)
	hrefs=page.xpath('//*[@class="system cl"]/ul[1]/li/a')
	href_list=[]
	for href in hrefs:
		href_list.append([href.text,href.attrib['href']])
	return href_list

# def get_pageNum(href):
# 	html=get_html(href)
# 	page=etree.HTML(html)
# 	# pageTag=page.xpath('//div[@class="g_page"]/a[not(@class="after")][last()]')
# 	count=page.xpath('//*[@id="content"]/div/div[1]/div/div/strong')
# 	if len(count)>0:
# 		count=count[0].text.strip().split()[1]
# 		pageNum=int(math.ceil(int(count)*1.0/18))
# 	else:
# 		pageNum=1
# 	return pageNum


def get_each_href(path,href):

	html=get_html(href)
	page=etree.HTML(html)
	hrefs=page.xpath('//*[@class="mimglist cl"]/li/a/img')
	href_list=[]
	for ihref in hrefs:
		href_list.append([ihref.attrib['title'],ihref.attrib['data-original']])
	create_folder_and_save(path,href_list)

def create_folder_and_save(path,href_list):
	path='siji'+os.sep+path
	if not os.path.exists(path):
		os.mkdir(path)
	for item in href_list:
		urllib.urlretrieve(item[1],path+os.sep+item[0]+'.jpg')

def main():
	global website
	website='http://www.4j4j.cn/zmbz/'

	path='siji'
	if not os.path.exists(path):
		os.mkdir(path)

	html=get_html(website)
	href_list=get_labels(html)
	for ihref in href_list:
		print ihref[0],ihref[1]
	# get_each_href(href_list[0][0],href_list[0][1])
	threads=[]
	for item in href_list:
		threads.append(threading.Thread(target=get_each_href,
										args=(item[0],item[1],)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

if __name__ == '__main__':
	main()

