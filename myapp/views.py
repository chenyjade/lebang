from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.

from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from myapp.permissions import IsOwnerOrReadOnly
from myapp.serializers import *


#用于登录

class UserLoginAPIView(generics.GenericAPIView):
   queryset = User.objects.all()
   serializer_class = UserRegisterSerializer
   permission_classes = (AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('username')
       password = data.get('password')
       user = User.objects.get(username__exact=username)
       if user.password == password:
           serializer = UserSerializer(user)
           new_data = serializer.data
           # 记忆已登录用户
           self.request.session['user_id'] = user.id
           return Response(new_data, status=HTTP_200_OK)
       return Response('password error', HTTP_400_BAD_REQUEST)


#用于注册

class UserRegisterAPIView(APIView):
   queryset = User.objects.all()
   serializer_class = UserRegisterSerializer
   permission_classes = (AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('username')
       password = data.get('password')
       if User.objects.filter(username__exact=username):
           return Response("用户名已存在",HTTP_400_BAD_REQUEST)
       serializer = UserRegisterSerializer(data=data)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response(serializer.data,status=HTTP_200_OK)
       return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# 修改用户信息
class UserUpdateAPIView(APIView):
	queryset = User.objects.all()
	serializer_class = UserUpdateSerializer
	def get(self, request, format=None):
		name = request.GET.get('username')
		user = User.objects.filter(username__exact=name)
		#serializer = UserUpdateSerializer(user)
		if user:
			serializer = UserUpdateSerializer(user, many=True)
			return Response(serializer.data,status=HTTP_200_OK)
		return Response(request.data, status=HTTP_400_BAD_REQUEST)

	def post(self, request, format=None):
		data = request.data
		user = User.objects.get(id=data.get('id'))
		serializer = UserUpdateSerializer(user,data=data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data,status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

	
#任务发布

class TaskPublishAPIView(APIView):
	queryset = Task.objects.all()
	serializer_class = TaskPublishSerializer
	def post(self, request, format=None):
		data = request.data
		print (data['image'])
		print (type(data['image']))
		serializer = TaskPublishSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data,status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# 任务详细界面
class TaskDetailAPIView(generics.GenericAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskDetailSerializer
	def get(self, request, format=None):
		base_id = int(request.GET.get('task_id'))
		user_id = int(request.GET.get('user_id'))
		task = Task.objects.get(id=base_id)
		if task:
			user = User.objects.get(id=user_id)
			task_list = user.like_user.all()
			serializer = self.get_serializer(task)
			r = serializer.data
			r['like'] = 0
			if task in task_list:
				r['like'] = 1
			return Response(r,status=HTTP_200_OK)
		return Response("id not in database", status=HTTP_400_BAD_REQUEST)

# 任务梗概
class TaskSummaryAPIView(generics.GenericAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSummarySerializer
	def get(self, request, format=None):
		base_id = int(request.GET.get('id'))
		# if base_id > length:
		# 	return Response("已达到任务列表末尾",status=HTTP_400_BAD_REQUEST)
		user_id = request.session['user_id']
		user = User.objects.get(id=user_id)
		if base_id == 0:
			task = Task.objects.filter(task_status=0).exclude(publisher=user).order_by("-time")
			if len(task) > 10:
				task = task[0:10]
			serializer = self.get_serializer(task, many=True)
			# serializer = TaskSummarySerializer(task, many=True)
			return Response(serializer.data,status=HTTP_200_OK)
		task = Task.objects.filter(id__gt=base_id).exclude(publisher=user).filter(task_status=0)
		if len(task) > 10:
			task = task[0:10] 
		serializer = self.get_serializer(task, many=True)
		return Response(serializer.data,status=HTTP_200_OK)
#任务删除

class TaskDeleteAPIView(APIView):
	queryset = Task.objects.all()
	def post(self, request, format=None):
		data = request.data
		task = Task.objects.filter(id=data['id'])
		#print (task)
		if task:
			task.task_status = 2
			return Response(request.data,status=HTTP_200_OK)
		return Response(request.data, status=HTTP_400_BAD_REQUEST)

# 接取和喜欢任务
class TaskLikeAPIView(APIView):
	queryset = Task.objects.all()
	def post(self, request, format=None):
		data = request.data
		user = User.objects.get(id=data['user_id'])
		if user:
			task = Task.objects.get(id=data['task_id'])
			task.like.add(user)
			task.save()
			return Response(request.data,status=HTTP_200_OK)
		return Response(request.data, status=HTTP_400_BAD_REQUEST)

class TaskTakeAPIView(APIView):
	queryset = Task.objects.all()
	def post(self, request, format=None):
		data = request.data
		user = User.objects.get(id=data['user_id'])
		if user:
			task = Task.objects.get(id=data['task_id'])
			task.take.add(user)
			task.save()
			return Response(request.data,status=HTTP_200_OK)
		return Response(request.data, status=HTTP_400_BAD_REQUEST)			

# 我收藏的任务
class UserLikeAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = TaskSummarySerializer
	def get(self, request, format=None):
		user_id = int(request.GET.get('user_id'))
		user = User.objects.get(id=user_id)
		task = user.like_user.all()
		serializer = self.get_serializer(task, many=True)
		return Response(serializer.data,status=HTTP_200_OK)

# 我接取的任务
class UserTakeAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = TaskSummarySerializer
	def get(self, request, format=None):
		user_id = int(request.GET.get('user_id'))
		user = User.objects.get(id=user_id)
		task = user.take_user.all()
		serializer = self.get_serializer(task, many=True)
		return Response(serializer.data,status=HTTP_200_OK)

# 我发布的任务
class UserMyPublishAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = TaskSummarySerializer
	def get(self, request, format=None):
		user_id = int(request.GET.get('user_id'))
		user = User.objects.get(id=user_id)
		task = Task.objects.filter(publisher = user)
		serializer = self.get_serializer(task, many=True)
		return Response(serializer.data,status=HTTP_200_OK)	

# 任务被谁点赞/领取
class TaskByAPIView(generics.GenericAPIView):
	queryset = Task.objects.all()
	serializer_class = UserDetailSerializer
	def get(self, request, format=None):
		task_id = int(request.GET.get('task_id'))
		query = request.GET.get('query')
		task = Task.objects.get(id=task_id)
		if query == 'like':
			users = task.like.all()
		elif query == 'take':
			users = task.taker.all()
		else:
			return Response("illegal query",status=HTTP_400_BAD_REQUEST)	
		serializer = self.get_serializer(users, many=True)
		return Response(serializer.data,status=HTTP_200_OK)	

# 分配/结束 任务
class UserActionAPIView(APIView):
	queryset = Task.objects.all()
	def post(self, request, format=None):
		data = request.data
		query = data['query']
		my_id = request.session['user_id']
		owner = User.objects.get(id=my_id)
		task = Task.objects.get(id=data['task_id'])
		if task.publisher != owner:
			return Response("permission denied", status=HTTP_400_BAD_REQUEST)
		if query == 'distribute':
			user = User.objects.get(id=data['user_id'])
			task.taker.add(user)
			task.task_status = 1
			task.save()
			return Response(request.data,status=HTTP_200_OK)
		elif query == 'finish':
			users = task.taker.all()
			for user in users:
				user.credit += 10
			task.task_status = 2
			user.save()
			task.save()
			return Response(request.data,status=HTTP_200_OK)
		return Response(request.data, status=HTTP_400_BAD_REQUEST)

# 取消我like/take的任务
class UserCancelAPIView(APIView):
	queryset = Task.objects.all()
	def post(self, request, format=None):
		data = request.data
		query = data['query']
		my_id = request.session['user_id']
		if data['user_id'] != my_id:
			return Response("permission denied", status=HTTP_400_BAD_REQUEST)
		user = User.objects.get(id=data['user_id'])
		if query == 'take':
			task = Task.objects.get(id=data['task_id'])
			task.taker.remove(user)
			user.credit -= 20
			task.task_status = 0
			user.save()
			task.save()
			return Response(request.data,status=HTTP_200_OK)
		elif query == 'like':
			task = Task.objects.get(id=data['task_id'])
			task.like.remove(user)
			user.credit -= 5
			user.save()
			task.save()
			return Response(request.data,status=HTTP_200_OK)
		return Response(request.data, status=HTTP_400_BAD_REQUEST)
# 举报
class ReportAPIView(APIView):
	def post(self, request, format=None):
		data = request.data
		user = User.objects.get(id=data['user_id'])
		task = Task.objects.get(id=data['task_id'])
		report = Report.objects.create(reporter=user,task=task,image=data['image'],description=data['description'])
		report.save()

		return Response(request.data,status=HTTP_200_OK)
class UserViewSet(generics.GenericAPIView):
   queryset = User.objects.all()
   serializer_class = UserSerializer