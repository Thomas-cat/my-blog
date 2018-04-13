from django.db import models
from django.contrib.auth.models import User
#创建应用的模型 
from django.urls import reverse

#创建目录类 name是里面的字段
class Category(models.Model):
	category_name = models.CharField(max_length = 100)
	def __str__(self):
		return self.category_name


#标签类
class Tag(models.Model):
	tag_name = models.CharField(max_length = 100)
	def __str__(self):
		return self.tag_name


#文章主体类
class Post(models.Model):
	title = models.CharField(max_length = 70)
	#因为字数多 所以使用 TextField类
	body = models.TextField()

	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()
	#文章的摘要 
	excerpt = models.CharField(max_length = 100,blank = True)
	
	#文章要与分类关联 用模型类创建
	category = models.ForeignKey('Category',on_delete = models.CASCADE)
	tags = models.ManyToManyField('Tag',blank = True)
	#user类是django提供的 完成了登录注册等模型的功能
	author = models.ForeignKey(User,on_delete = models.CASCADE)
	
	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})

	
	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created_time']
