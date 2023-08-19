from django.urls import path
from . import views as api_views

app_name = 'role'
urlpatterns = [
	path('user/list/', api_views.UserList.as_view(), name='user-list'),

	path('list/', api_views.RoleList.as_view(), name='role-list'),
	path('detail/<int:pk>/', api_views.RoleDetail.as_view(), name='role-detail'),
	path('create/', api_views.RoleCreate.as_view(), name='role-create'),
	path('update/<int:pk>/', api_views.RoleUpdate.as_view(), name='role-update'),
]