from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm

#得到url解析发过来的request 
def index(request):
	post_list = Post.objects.all()	
	return render(request,'blog/index.html',context = {
			'post_list':post_list
			})

#用get_object_or_404去model里找到对应的文章
#render渲染页面 传递需要传递的数值
def detail(request,pk):
	post = get_object_or_404(Post, pk = pk)

	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post':post,
		'form':form,
		'comment_list':comment_list
		}
	return render(request,'blog/detail.html',context =context)

def archives(request,year,month):
	post_list = Post.objects.filter(created_time__year = year,
					created_time__month = month
					)
	return render(request,'blog/index.html',context = {'post_list':post_list})


#做分类视图
def category(request,pk):
	cate = get_object_or_404(Category,pk = pk)
	post_list = Post.objects.filter(category = cate).order_by('-created_time')
	return render(request,'blog/index.html',context = {'post_list':post_list})
