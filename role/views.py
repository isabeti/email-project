from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from email_project.response import Msg, Action, APIResponse, set_receive
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Role
from .serializers import UserSerializer, RoleSerializer
# Create your views here.

class UserList(APIView):
	def get(slef, request):
		request.msg = Msg()
		actions = [Action.data('Show list of users', 'role:user-list')]

		objects = User.objects.all()
		data = UserSerializer(objects, many=True).data if objects else None

		return Response(APIResponse(request.msg, actions, data))

class RoleList(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('Show list of roles', 'role:role-list')]

		objects = Role.objects.all()
		data = RoleSerializer(objects, many=True).data if objects else None

		return Response(APIResponse(request.msg, actions, data))

class RoleDetail(APIView):
	def get_object(self, pk):
		return get_object_or_404(Role, pk=pk)

	def get(self, request, pk):
		request.msg = Msg()
		actions = [
			Action.data_dt('View role detail', 'role:role-detail', pk),
			Action.data_dt('delete a role', 'role:role-detail', pk, {'position': 'delete'}),
		]

		obj = self.get_object(pk)
		data = RoleSerializer(obj).data if obj else None

		return Response(APIResponse(request.msg, actions,data))

	def post(self, request, pk):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('position') == 'delete':
			obj = self.get_object(pk)
			obj.delete()

			request.msg.Error = (
				('The role has been deleted.')
			)
			actions = Action.redirect_to('role:role-list')
			return Response(APIResponse(request.msg, actions))
		else:
			return Response({'message': 'Error!!! please try again.'}, status=status.HTTP_403_FORBIDDEN	)



class RoleCreate(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('Create a role', 'role:role-create', 
			{
				'user_id': None, 'create_category': 'True or False', 'delete_update_category': 'True or False', 
				'add_email': 'True or False', 'update_delete_email': 'True or False', 'send_email': 'True or False', 
				'active': 'True or False', 
			})]
		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		try:
			create_obj = Role.create_obj(receive)
			request.msg.Success(
				('The role has been created successfully.')
			)
			actions = Action.redirect_to_dt('role:role-detail', pk)
			return Response(APIResponse(request.msg, actions))
		except:
			return Response({'message': 'Error!!! please try again.'}, status=status.HTTP_403_FORBIDDEN)

class RoleUpdate(APIView):
	def get_object(self, pk):
		return get_object_or_404(Role, pk=pk)

	def get(self, request, pk):
		request.msg = Msg()
		actions = [Action.data_dt('Update a role', 'role:role-update', pk,  
			{
				'user_id': None, 'create_category': 'True or False', 'delete_update_category': 'True or False', 
				'add_email': 'True or False', 'update_delete_email': 'True or False', 'send_email': 'True or False', 
				'active': 'True or False', 
			})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request, pk):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		try:
			obj=self.get_object(pk)
			obj.user_id = receive.get('user_id') if receive.get('user_id') else False
			obj.create_category = receive.get('create_category') if receive.get('create_category') else False
			obj.delete_update_category = receive.get('delete_update_category') if receive.get('delete_update_category') else False
			obj.add_email = receive.get('add_email') if receive.get('add_email') else False
			obj.update_delete_email = receive.get('update_delete_email') if receive.get('update_delete_email') else False
			obj.send_email = receive.get('send_email') if receive.get('send_email') else False
			obj.active = receive.get('active') if receive.get('active') else False
			obj.save()

			request.msg.Success = (
				('The role has been updated successfully.')
			)
			actions = Action.redirect_to_dt('role:role-detail', pk)
			return Response(APIResponse(request.msg, actions))
		except:
			return Response({'message': 'Error!!! please try again.'}, status=status.HTTP_403_FORBIDDEN)