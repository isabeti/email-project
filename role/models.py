from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Role(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_user')

	create_category = models.BooleanField(default=False)
	delete_update_category = models.BooleanField(default=False)
	
	add_email = models.BooleanField(default=False)
	update_delete_email = models.BooleanField(default=False)
	send_email = models.BooleanField(default=False)

	active = models.BooleanField(default=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def create_obj(receive):
		return Role.objects.create(
			user_id=receive.get('user_id'), 
			create_category=receive.get('create_category') if receive.get('create_category') else False,  
			delete_update_category=receive.get('delete_update_category') if receive.get('delete_update_category') else False, 
			add_email=receive.get('add_email') if receive.get('add_email') else False, 
			update_delete_email=receive.get('update_delete_email') if receive.get('update_delete_email') else False, 
			send_email=receive.get('send_email') if receive.get('send_email') else False, 
			active=receive.get('active') if receive.get('active') else False, 
		)