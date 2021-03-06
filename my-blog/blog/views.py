from django.shortcuts import render,get_object_or_404
import logging 
from django.http import HttpResponse
from django.db.models import Q
from .models import Post,Category,Tag
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
from .ccckk.ck import *
from .lottery.lottery import *
from .proxy.ccckk8 import recharge_ccckk8
import json
import time


#
##以下为彩票接口
def lottery_clear(requests):
	author = requests.GET.get("author")
	clearData(author)
	data = {'statue':'success'}
	return HttpResponse(json.dumps(data),content_type="application/json")
def lottery_get(requests):
	author = requests.GET.get("author")
	data = transData(author)
	return HttpResponse(json.dumps(data),content_type="application/json")
def lottery_update(requests):
	author = requests.GET.get("author")
	result = requests.GET.get("result")
	updateData(author,result)
	data = {'statue':'success'}
	return HttpResponse(json.dumps(data),content_type="application/json")
##接口到此结束




#以下为接口ccckk
##获取首页目录数据
def ccckk_userInfo(requests):
	data = get_counts()
	return HttpResponse(json.dumps(data),content_type="application/json")
def ccckk_homePage(requests):
	cate = int(requests.GET.get('cate'))
	ty = requests.GET.get('type')
	page = int(requests.GET.get('page'))
	data = get_category(cate,ty,page)
	return HttpResponse(json.dumps(data),content_type="application/json")
##获取内容详情数据
def ccckk_detailPage(requests):
	cate = int(requests.GET.get('cate'))
	url = requests.GET.get('url')
	if cate == 2:
		ret = get_novel(url)
		data = {'text':ret}
	elif cate == 1:
		ret = get_picture(url)
		data = {'pictureLins':ret}
	return HttpResponse(json.dumps(data),content_type="application/json")

#ccckk接口到此为止

def time_tool(requests):
	t = requests.GET.get('t')
	if t!=None:
		a = time.localtime(int(t))
		time_string = "%s-%s-%s  %s:%s"%(a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min)
		time_string = {'time_string':time_string}
	else:
		time_string = {'time_string':'none'}
	return HttpResponse(json.dumps(time_string),content_type="application/json")
		
class TagView(ListView):
	model = 'Post'
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	def get_queryset(self):
		tg = get_object_or_404(Tag,pk = self.kwargs.get('pk'))
		return Post.objects.all().filter(tags = tg)
def recharge(requests):
	q = requests.GET.get('q')
	msg = '输入充值链接'
	if q!= None:
		ret = recharge_ccckk8(q)
		if ret!=0:
			msg = '充值故障,请用你的想象力撸管吧'
		else:
			msg = '充值成功,切记强撸灰飞烟灭'
	return render(requests,'blog/recharge.html',context = {'msg':msg})

def search(request):
	q = request.GET.get('q')
	error_msg = ''
	if not q:
		error_msg = '请输入关键词'
		return render(request,'blog/index.html',context = {'error_msg':error_msg})
	post_list = Post.objects.filter(Q(title__icontains = q)| Q(body__icontains=q))
	if not post_list:
		error_msg = '没有找到该关键字'
	return render(request,'blog/index.html',context = {'error_msg':error_msg,'post_list':post_list,'key_word':q})
#得到url解析发过来的request 

class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 2
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator,page,is_paginated)
		context.update(pagination_data)

		request = self.request
		if request.META.get('HTTP_X_FORWARDED_FOR'):  
			ip =  request.META['HTTP_X_FORWARDED_FOR']  
		else:  
			ip = request.META['REMOTE_ADDR']  
		context['ip'] = ip
		return context
	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			return {}
		left_has_more = False
		right_has_more = False
		#用户当前请求的页数
		page_index = page.number
		#总页数
		total_pages = paginator.num_pages
		#获得整个分页码数，比如分了四页[1，2，3，4]
		page_range = paginator.page_range
		first_index = (page_index-2)if(page_index-2>1) else 1
		last_index = (page_index+2)if(page_index+2<total_pages) else total_pages

		page_index = list(page_range[first_index-1:last_index])


		if (page_index[0]>1):
			page_index.insert(0,'...')
			page_index.insert(0,1)
		if (page_index[-1]< total_pages):
			page_index.append('...')
			page_index.append(total_pages)
		data = {
		'page_index':page_index,
		}
		return data
#用get_object_or_404去model里找到对应的文章
#render渲染页面 传递需要传递的数值
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'
	def get_context_data(self,*args,**kwargs):
		context = super(PostDetailView,self).get_context_data(*args,**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({'form':form,'comment_list':comment_list})
		return context



class ArchivesView(IndexView):
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return Post.objects.filter(created_time__year = year,created_time__month = month)
	def get_context_data(self,**kwargs):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		context = super().get_context_data(**kwargs)
		date_time = str(year)+'年 '+str(month)+'月'
		context['date_time'] = date_time
		return context

#做分类视图
class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
		return Post.objects.filter(category = cate)
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
		context['category'] = cate
		return context
