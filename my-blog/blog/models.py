from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
#创建应用的模型 
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

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
	body = RichTextUploadingField()

	created_time = models.DateTimeField(auto_now_add =True)
	modified_time = models.DateTimeField(auto_now_add = True)
	#文章的摘要 
	excerpt = models.CharField(max_length = 100,blank = True)
	
	#文章要与分类关联 用模型类创建
	category = models.ForeignKey('Category',on_delete = models.CASCADE)
	tags = models.ManyToManyField('Tag',blank = True)
	#user类是django提供的 完成了登录注册等模型的功能
	author = models.ForeignKey(User,on_delete = models.CASCADE)

	#阅读数目	
	views = models.PositiveIntegerField(default = 0)


	def increase_views(self):
		self.views+=1
		self.save(update_fields = ['views'])
	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})

	
	def __str__(self):
		return self.title
	def save(self,*args,**kwargs):
		if not self.excerpt:
			self.excerpt = strip_tags(self.body)[:40]
		super(Post,self).save(*args,**kwargs)

	class Meta:
		ordering = ['-created_time']
