from rest_framework import serializers
from myapp.models import *

#用于注册的时候返回json数据

class UserRegisterSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('id', 'username', 'password')

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('id', 'username')

class UserDetailSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('id', 'username', 'phone', 'credit', 'head_img')

# 用于修改用户信息
class UserUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.password = validated_data.get('password', instance.password)
		instance.phone = validated_data.get('phone', instance.phone)
		instance.credit = validated_data.get('credit', instance.credit)
		instance.head_img = validated_data.get('head_img', instance.head_img)
		instance.save()
		return instance

# 返回任务简介
class TaskSummarySerializer(serializers.ModelSerializer):
	publisher_name = serializers.CharField(source='publisher.username')
	head_img = serializers.ImageField(source='publisher.head_img')
	like_num = serializers.SerializerMethodField()

	def get_like_num(self, obj):
		return obj.like.all().count()

	class Meta:
		model = Task
		fields = ('id','publisher_name','tag','price','task_title','head_img','task_status','like_num')

# 任务具体界面
class TaskDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('image','time','description')	
		
# 任务发布界面
class TaskPublishSerializer(serializers.ModelSerializer):
	publisher_name = serializers.CharField(source='publisher.username')
	class Meta:
		model = Task
		fields = ('id','publisher_name','task_title','description','image','tag','price')

	def create(self, validated_data):
		publisher = User.objects.get(**validated_data.pop('publisher'))
		print(publisher)
		task = Task()
		task.publisher = publisher
		task.task_title = validated_data['task_title']
		task.description = validated_data['description']
		task.image = validated_data['image']
		task.tag = validated_data['tag']
		task.price = validated_data['price']
		task.save()
		return task

