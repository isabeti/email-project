from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATUS_CHOICES = (
	('email', 'Email'),
	('template_email', 'Template email'),
)

class Category(models.Model):
	title = models.CharField(max_length=200)
	delete = models.BooleanField(default=False)

	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='email')

	def create_obj(receive):
		return Category.objects.create(title=receive.get('title'), status=receive.get('status'))

class TemplateEmail(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='cat_template_emails')
	title = models.CharField(max_length=100)
	description = models.TextField()
	html = models.TextField()
	
	delete = models.BooleanField(default=False)
	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)

	def create_obj(receive):
		return TemplateEmail.objects.create(
			category_id=receive.get('category_id'), title=receive.get('title'), 
			description=receive.get('description'), html=receive.get('html')
		)

class Email(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='cat_emails')
	full_name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)

	delete = models.BooleanField(default=False)
	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)

	def create_obj(receive):
		return Email.objects.create(category_id=receive.get('category_id'), full_name=receive.get('full_name'), email=receive.get('email'))


class History(models.Model):
	sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sender_email_history')
	email = models.ManyToManyField(Email, null=True, related_name='emails_history')
	subject = models.CharField(max_length=200)
	content = models.TextField(null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='email')

	def create_obj(receive, emails_obj, status):
		if status == 'template_email':
			obj = History.objects.create(subject=receive.get('subject'), status='template_email')
			for i in emails_obj:
				obj.email.add(i)
			return obj

		else:
			obj = History.objects.create(subject=receive.get('subject'), content=receive.get('content'))
			for i in emails_obj:
				obj.email.add(i)
			return obj

