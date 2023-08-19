from django.urls import path
from rest_framework.authtoken import views
from . import views as api_views

app_name = 'api'
urlpatterns = [
    path('token-auth/', views.obtain_auth_token),

    path('category/list/', api_views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', api_views.CategoryDetail.as_view(), name='category-detail'),
    path('category/create/', api_views.CategoryCreate.as_view(), name='category-create'),

    path('add/email/', api_views.AddEmail.as_view(), name='add-email'),
    path('update/email/', api_views.UpdateEmail.as_view(), name='update-email'),
    path('delete/email/', api_views.DeleteEmail.as_view(), name='delete-email'),

    path('template-email/list/', api_views.TemplateEmailList.as_view(), name='template-email-list'),
    path('template-email/<int:pk>/', api_views.TemplateEmailDetail.as_view(), name='template-email-detail'),
    path('template-email/create/', api_views.TemplateEmailCreate.as_view(), name='template-email-create'),

    
    path('send/email/', api_views.SendEmail.as_view(), name='send-email'),
    path('send/template/email/', api_views.SendTemplateEmail.as_view(), name='send-template-email'),

    path('history/list/', api_views.ListHistory.as_view(), name='list-history'),

]
