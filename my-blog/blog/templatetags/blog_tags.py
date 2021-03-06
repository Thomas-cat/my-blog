from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count

#这里是注册了模板 自己编写的简单模板
register = template.Library()

#装饰器
#最近的文章
@register.simple_tag
def get_recent_posts(num = 5):
	return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def get_tags():
	return Tag.objects.annotate(post_num = Count('post')).filter(post_num__gt = 0)
#dates会返回一个文章时间列表 后面参数指定精度
#归档文章
@register.simple_tag
def archives():
	return Post.objects.dates('created_time','month',order = 'DESC')

#分类
@register.simple_tag
def get_categories():
	return Category.objects.annotate(post_num = Count('post')).filter(post_num__gt = 0)
