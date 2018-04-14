from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Post,Category
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
from .proxy.ccckk8 import recharge_ccckk8
def recharge(requests):
	q = requests.GET.get('q')
	msg = '输入充值链接'
	if q!= None:
		if q.find('bid')!= -1:
			ret = recharge_ccckk8(q)
			if ret!=0:
				msg = '充值故障,请用你的想象力撸管吧'
			else:
				msg = '充值成功,切记强撸灰飞烟灭'
		else:
			msg = '链接有错误,请重新输入正确的链接'
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
		return context

	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			return {}
		left_has_more = False
		right_has_more = False
		#用户当前请求的页数
		page_index = page.number-1
		#总页数
		total_pages = paginator.num_pages
		#获得整个分页码数，比如分了四页[1，2，3，4]
		page_range = paginator.page_range

		first_index = (page_index-2)if(page_index-2>0) else 1
		last_index = (page_index+2)if(page_index+2<total_pages-1) else total_pages-2
		page_index = list(page_range[first_index:last_index+1])
		if (page_index[0]-2>0):
			page_index.insert(0,'...')
		if (page_index[-1]+1< total_pages):
			page_index.append('...')
		page_index.insert(0,1)
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
	def get(self,request,*args,**kwargs):
		respon = super(PostDetailView,self).get(request,*args,**kwargs)
		self.object.increase_views()
		return respon
	def get_context_data(self,*args,**kwargs):
		context = super(PostDetailView,self).get_context_data(*args,**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({'form':form,'comment_list':comment_list})
		return context



class ArchivesView(ListView):
	model = Post
	tempate_name = 'blog/index.html'
	context_object_name = 'post_list'
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return Post.objects.filter(created_time__year = year,created_time__month = month)

#做分类视图
class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	def get_queryset(self):
		cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
		return Post.objects.filter(category = cate)
