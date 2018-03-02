from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=20,null=False)
	password = models.CharField(max_length=20,null=False)
	phone = models.CharField(max_length=20,blank=True,null=True) 
	credit =  models.IntegerField(default=0,blank=True,null=True)
	head_img = models.ImageField(upload_to='static/head_img',blank=True)

	def __str__(self):
		return self.username


class Task(models.Model):
	STATUS_SIZE = (
			(0, '未被接取'),
			(1, '已被接取'),
			(2, '已完成'),
		)

	task_status =  models.IntegerField(default=0,blank=True,choices=STATUS_SIZE)
	task_title = models.CharField(max_length=20,null=False)
	image = models.ImageField(upload_to='static/img', blank=True, null=True)
	description = models.CharField(max_length=200,blank=True)
	publisher = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	like = models.ManyToManyField(User, related_name='like_user') #收藏
	taker = models.ManyToManyField(User, related_name='take_user') #接取
	tag = models.CharField(max_length=10,null=True)
	time = models.DateTimeField(auto_now=True)
	price = models.CharField(max_length=10,null=True)

	def __str__(self):
		return self.task_title

class Report(models.Model):
	reporter = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	task = models.ForeignKey(Task,on_delete=models.SET_NULL, null=True)
	#被举报者
	image = models.ImageField(upload_to='static/report', blank=True, null=True)
	description = models.CharField(max_length=200,blank=True)
	time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.description