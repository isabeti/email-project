from rest_framework import serializers
from .models import Category, Email, History, TemplateEmail

class EmailListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Email
		fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
	emails = EmailListSerializer(many=True)
	class Meta:
		model = Category
		fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
	email = EmailListSerializer(many=True)
	class Meta:
		model = History
		fields = '__all__'

class TemplateEmailSerializer(serializers.ModelSerializer):
	category = CategoryListSerializer()
	class Meta:
		model = TemplateEmail
		fields = '__all__'
