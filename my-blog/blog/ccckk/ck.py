import requests
import traceback
import urllib3
import os
import time
from lxml import etree
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#网址转换

yzst = '/picture/list/亚洲色图#header'
omst = '/picture/list/欧美色图#header'
pbyph = '/picture/monthly-ranking#header'

jtll = '/story/list/家庭乱伦#header'
llxs = '/story/list/另类小说#header'
xycs = '/story/list/校园春色#header'

bzph = "/video/weekly-ranking#header"
byph = "/video/monthly-ranking#header"
zjgx = "/video/newest#header"

access_url = 'https://ccckk8.com/picture/detail/17301'
check_code = ''
base_url = ''
req = requests.session()
#网址入口以及代理
ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
user_url = 'https://ccckk8.com/user/profile#header'
recharge_url = ''

def get_counts():
	e = open_url(user_url)
	items = e.xpath("//div[@id='body']//span/text()")
	user_class = items[0]
	user_counts = items[1]
	print(user_class,user_counts)
	return [user_class,user_counts]
def recharge_userInfo():
	global recharge_url
	ready_ok()
	print(recharge_url)
	with open('./code.txt','r')as f:
		data = f.read()
	data = eval(data)
	data = {'c1':data[1],'c2':data[0]}
	req.post(recharge_url,headers=ua,verify=False,timeout=5,data=data)
	print(data)
def get_userInfo():
	e = open_url(user_url)
	items = e.xpath('//h3/text()')[0:2]
	code_items = [item.split(' ')[1] for item in items]
	with open('./code.txt','w')as f:
		f.write(str(code_items))
def open_url(url,data={},params={},t=10):
	try:
		if url.find('http')==-1:
			url = 'https://'+url
		a = req.get(url,headers=ua,verify=False,timeout = t,params=params,data=data)
		html = a.content.decode("utf-8")
		e = etree.HTML(html)
	except:
		e = ''
		traceback.print_exc()
	return e
	
def get_redirect(url):
	global check_code 
	try:
		e = open_url(url)
		text = e.xpath('//p[1]/text()')
		if text[0].find('请使用')!=-1:
			ret = 'https://'+text[0].split(' ')[2]
		else:
			ret = ''
		if text[0].find('上面输入')!=-1:
			check_code = text[0].split(' ')[2]
	except:
		ret = ''
	return ret

def get_videoLink(url,data={},params={}):
	global base_url
	title = []
	href = []
	cover=[]
	try:
		e= open_url(url,data,params)
		title = e.xpath("//div[@id='body']//div//img/@alt")
		cover = e.xpath("//div[@id='body']//div//img/@src")
		cover = [base_url+x for x in cover]
		href = e.xpath("//div[@id='body']//div//a/@href")
		href = [base_url+x for x in href]
	except: 
		print("获取视频链接出错")
	return [title,href,cover]

def get_pictureLink(url,data={},params={}):
	global base_url
	title = []
	href = []
	cover = []
	try:
		e= open_url(url,data,params)
		title = e.xpath("//div[@id='body']//div//img/@alt")
		cover = e.xpath("//div[@id='body']//div//img/@src")
		cover = [base_url+x for x in cover]
		href = e.xpath("//div[@id='body']//div//a/@href")
		href = [base_url+x for x in href]
	except: 
		print("获取图片链接出错")
	return [title,href,cover]
def get_novelLink(url,data={},params={}):
	global base_url
	title = []
	href = []
	try:
		e= open_url(url,data,params)
		title = e.xpath("//div[@class='item-title']/a/h3/text()")
		title = [x.replace('\n','').replace(' ','') for x in title]
		href = e.xpath("//div[@class='item-title']/a/@href")
		href = [base_url+x for x in href]
	except:	
		print("获取文章链接出错")
	return [title,href]
def check(url):
	global check_code,base_url
	get_redirect(url)
	ret = open_url(url,{},{'ccc':check_code},3)
	if ret=='':
		print('check失败')
	else:
		print("check成功")

def get_novel(url):
	check(url)
	e = open_url(url)
	text = e.xpath("//div[@id='body']/div[1]/text()")
	print(text)
	tmp =''
	for item in text:
		tmp+=item
	return	tmp 

def get_picture(url):
	global base_url
	check(url)
	e = open_url(url)
	pics = e.xpath("//p/img/@src")
	pics = [base_url+pic for pic in pics]
	return pics
def ready_ok():
	global base_url,access_url,recharge_url
	base_url = get_redirect(access_url)
	recharge_url = base_url+'/user/czhf'
	check_tmp = get_pictureLink(base_url+yzst)
	check(check_tmp[1][0])
def get_category(cate,ty,page):
	ready_ok()
	s = eval(ty)
	params = {'page':page}
	if cate==1:
		ret = get_pictureLink(base_url+s,{},params)
	elif cate==2:
		ret = get_novelLink(base_url+s,{},params)
	else:
		ret = get_videoLink(base_url+s,{},params)
	return ret
