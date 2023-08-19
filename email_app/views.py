from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime, timedelta

from email_project.response import Msg, Action, APIResponse, set_receive
from .serializers import CategoryListSerializer, CategoryDetailSerializer, HistorySerializer, TemplateEmailSerializer
from .models import Category, TemplateEmail, Email, History

from email_project.email_sender import send_new_email
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email_project.settings import EMAIL_HOST_USER
# Create your views here.

# API Category
class CategoryList(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [
			Action.data('view list category', 'api:category-list'),
			Action.data('filter category', 'api:category-list', {'status': 'email or template_email'}),
		]

		objects = Category.objects.filter(delete=False)
		data = CategoryListSerializer(objects, many=True).data if objects else None
		return Response(APIResponse(request.msg, actions, data))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('status') == 'email':
			objects = Category.objects.filter(delete=False, status='email')
			data = CategoryListSerializer(objects, many=True).data if objects else None
			return Response(data)

		elif receive.get('status') == 'template_email':
			objects = Category.objects.filter(delete=False, status='template_email')
			data = CategoryListSerializer(objects, many=True).data if objects else None
			return Response(data)

		else:
			return Response({'message': 'Error!!! please try again.'})

class CategoryDetail(APIView):
	def get_object(self, pk):
		return get_object_or_404(Category, pk=pk)

	def get(self, request, pk):
		request.msg = Msg()
		actions = [
			Action.data_dt('view detail category', 'api:category-detail', pk),
			Action.data_dt('edit category', 'api:category-detail', pk, {'position': 'edit', 'title': None}),
			Action.data_dt('delete category', 'api:category-detail', pk, {'position': 'delete'}),
		]
		obj = self.get_object(pk)
		obj.emails = obj.cat_emails.filter(delete=False)

		data = CategoryDetailSerializer(obj).data if obj else None
		return Response(APIResponse(request.msg, actions, data))

	def post(self, request, pk):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		obj = self.get_object(pk)
		position = receive.get('position')

		if position == 'edit':
			if not receive.get('title'):
				return Response({'message': 'title is required.'}, status=status.HTTP_403_FORBIDDEN)

			obj.title = receive.get('title') 
			obj.save()

			request.msg.Success = (
				('The category has been edited successfully.')
			)
			actions = Action.redirect_to_dt('api:category-detail', pk)
			return Response(APIResponse(request.msg, actions))


		elif position == 'delete':
			obj.delete=True
			obj.save()

			request.msg.Error = (
				('The category has been deleted.')
			)
			actions = Action.redirect_to_dt('api:category-detail', pk)
			return Response(ApiResponse(request.msg, actions))

		else:
			return Response({'message': 'Undefined position.'}, status=status.HTTP_403_FORBIDDEN)


class CategoryCreate(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('create category', 'api:category-create', {'title': None, 'status': 'email or template_email'})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('title') and receive.get('status'):
			obj = Category.create_obj(receive)
			request.msg.Success = (
				('The category has been created successfully.')
			)
			actions = Action.redirect_to('api:category-create')
			return Response(APIResponse(request.msg, actions))

		return Response({'message': 'title and status is required!'}, status=status.HTTP_403_FORBIDDEN)



# API Email
class AddEmail(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('add email', 'api:add-email', {'full_name': None, 'email': None, 'category_id': None, })]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('full_name') and receive.get('email') and receive.get('category_id'):
			if Email.objects.filter(email=receive.get('email'), category_id=receive.get('category_id')):
				return Response({'message': 'full_name, title, email is required!'}, status=status.HTTP_403_FORBIDDEN)

			else:
				obj = Email.create_obj(receive)
				request.msg.Success = (
					('The email has been added successfully.')
				)
				actions = Action.redirect_to_dt('api:category-detail', receive.get('category_id'))
				return Response(APIResponse(request.msg, actions))
			
		else:
			return Response({'message': 'full_name, title, email is required!'}, status=status.HTTP_403_FORBIDDEN)

class UpdateEmail(APIView):
	def get_object(self, id):
		return get_object_or_404(Email, id=id)

	def get(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)
		actions = [Action.data('update email', 'api:update-email', {'full_name': None, 'email': None, 'object_id': None})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('full_name') and receive.get('email') and receive.get('object_id'):
			obj = self.get_object(receive.get('object_id'))
			obj.full_name = receive.get('full_name')
			obj.email = receive.get('email')
			obj.save()
			request.msg.Success = (
				('The email has been updated successfully.')
			)
			actions = Action.redirect_to_dt('api:category-detail', obj.category_id)
			return Response(APIResponse(request.msg, actions))

		else:
			return Response({'message': 'full_name, email, object_id is required!'})

class DeleteEmail(APIView):
	def get_object(self, id):
		return get_object_or_404(Email, id=id)

	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('delete email', 'api:delete-email', {'object_id': None})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('object_id'):
			obj = self.get_object(receive.get('object_id'))
			obj.delete = True
			obj.save()

			request.msg.Error(
				('The email has been deleted.')
			)
			actions = Action.redirect_to_dt('api:category-detail', obj.category_id)
			return Response(APIResponse(request.msg, actions))
		
		else:
			return Response({'message': 'object_id is required!'}, status=status.HTTP_403_FORBIDDEN) 


# API Template email
class TemplateEmailList(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('Show a template email list', 'api:template-email-list'),]

		objects = TemplateEmail.objects.filter(delete=False)
		data = TemplateEmailSerializer(objects, many=True).data if objects else None

		return Response(APIResponse(request.msg, actions, data))

class TemplateEmailDetail(APIView):
	def get_object(self, pk):
		return get_object_or_404(TemplateEmail, pk=pk)

	def get(self, request, pk):
		request.msg = Msg()
		actions = [
			Action.data_dt('Show detail a template email.', 'api:template-email-detail', pk),
			Action.data_dt('Delete template email.', 'api:template-email-detail', pk, {'position': 'delete'}),
		]

		obj = self.get_object(pk)
		data = TemplateEmailSerializer(obj).data if obj else None

		return Response(APIResponse(request.msg, actions, data))

	def post(self, request, pk):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('position') == 'delete':
			obj = self.get_object(pk)
			obj.delete = True
			obj.save()

			request.msg.Error = (
				('The template view has been deleted.')
			)
			actions = Action.redirect_to('api:template-email-list')
			return Response(APIResponse(request.msg, actions))

		else:
			return Response({'message': 'Error!!! please try again.'}, status=status.HTTP_403_FORBIDDEN)

class TemplateEmailCreate(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('Create template email', 'api:template-email-create', 
			{'category_id': None,'title': None,'description': None,'html': None,})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		try:
			create_obj = TemplateEmail.create_obj(receive)

			request.msg.Success = (
				('The template email has been created successfully.')
			)
			action = Action.redirect_to_dt('api:template-email-detail', create_obj.pk)
			return Response(APIResponse(request.msg, action))
		except Exception as e:
			return Response({'message': 'Error!!! please try again.'}, status=status.HTTP_403_FORBIDDEN)


# API send email
class SendEmail(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('send email', 'api:send-email', {'subject': None, 'content': None, 'emails_id': '1,2,3,4,...'})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		if receive.get('subject') and receive.get('content') and receive.get('emails_id'):
			emails = []
			emails_obj = []
			list_emails_id = []

			emails_id = receive.get('emails_id')
			emails_id = emails_id.split(',')

			for i in emails_id:
				try:
					i = int(i)
					list_emails_id.append(i)
				except:
					pass


			for i in list_emails_id:
				if Email.objects.filter(id=i):
					obj = get_object_or_404(Email, id=i)
					emails.append(obj.email)
					emails_obj.append(obj)

			email_subject =  receive.get('subject')
			email_content = receive.get('content')
			destination_email = emails
			send_email = send_new_email(email_subject, email_content, destination_email)

			create_history_obj = History.create_obj(receive, emails_obj, 'email')

			request.msg.Success(
				(f'{len(emails)} out if {len(list_emails_id)} emails were sent successfully.')
			)
			actions = Action.redirect_to('api:send-email')
			return Response(APIResponse(request.msg, actions))

		else:
			return Response({'message': 'subject, content, emails is required!'}, status=status.HTTP_403_FORBIDDEN)


# Send template email
class SendTemplateEmail(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [Action.data('send email', 'api:send-email', {'subject': None, 'emails_id': '1,2,3,4,...', 'template_email_id': None})]

		return Response(APIResponse(request.msg, actions))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)

		try:
			emails = []
			emails_obj = []
			list_emails_id = []

			emails_id = receive.get('emails_id')
			emails_id = emails_id.split(',')

			for i in emails_id:
				try:
					i = int(i)
					list_emails_id.append(i)
				except:
					pass


			for i in list_emails_id:
				if Email.objects.filter(id=i):
					obj = get_object_or_404(Email, id=i)
					emails.append(obj.email)
					emails_obj.append(obj)

			obj = TemplateEmail.objects.get(id=receive.get('template_email_id'))

			html_body = render_to_string("email_app/mail.html", {'html_text': obj.html})
			#e_content = "Dear {user}\nHi\nHope you are going well.\nYou paid {cost} at {date}\n{intent} \nDo not reply to this Email. If you have any questions or concerns, please feel free to contact the company:\nEmail: payment@tecvico.com\n\nThank you.\n\nBest regards\n\n".format(user = instance.user, cost = instance.purchased_amount, date = instance.date_created, intent = instance.payment_intent)
			msg = EmailMultiAlternatives(subject=receive.get('subject'), from_email=EMAIL_HOST_USER, to=emails, body='')
			msg.attach_alternative(html_body, "text/html")
			msg.send()


			create_history_obj = History.create_obj(receive, emails_obj, 'template_email')

			request.msg.Success(
				(f'{len(emails)} out if {len(list_emails_id)} emails were sent successfully.')
			)
			actions = Action.redirect_to('api:send-email')
			return Response(APIResponse(request.msg, actions))

		except:
			return Response({'message': 'subject, template_email_id,  emails is required!'}, status=status.HTTP_403_FORBIDDEN)
			




# API History
class ListHistory(APIView):
	def get(self, request):
		request.msg = Msg()
		actions = [
			Action.data('view all historys', 'api:list-history'),
			Action.data('filter history', 'api:list-history', {'day': None})
		]

		objects = History.objects.all().order_by('-create_at')
		data = HistorySerializer(objects, many=True).data if objects else None
		return Response(APIResponse(request.msg, actions, data))

	def post(self, request):
		request.msg = Msg()
		receive = set_receive(request, request.content_type)
		try:
			day = int(receive.get('day'))
			last_day = datetime.today() - timedelta(minutes=day)
			objects = History.objects.filter(create_at__gt=last_day)

			data = HistorySerializer(objects, many=True).data if objects else None
			return Response(APIResponse(request.msg, {'actions': 'dwa'}, data))
		except Exception as e:
			return Response({'message': 'please enter the of days you want to be filterd!!'}, status=status.HTTP_403_FORBIDDEN)
