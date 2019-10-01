from django.contrib import admin
from .models import blog_posts
from user_accounts.models import UserProfile 
# Register your models here.
admin.site.register(blog_posts)
# admin.site.register(unjoin)
# admin.site.register(Joining)