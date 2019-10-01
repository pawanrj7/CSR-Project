from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from user_accounts.models import UserProfile 
from django.conf import settings
# Create your models here.

# class Join(models.Model):
#     joined = models.BooleanField(default=False, primary_key = True)
#     blog_posts = models.ForeignKey(blog_posts, on_delete=models.CASCADE)
from django.contrib.auth import get_user_model
User = get_user_model()

class blog_posts(models.Model):
    InitiativeTitle = models.CharField(max_length=200, unique = True)
    requirements = models.TextField(default= " ")
    name = models.CharField(max_length=100)
    budget = models.PositiveIntegerField(default = 0)
    location = models.CharField(max_length=100, default = "")
    details = models.TextField(default="No details abour this CSR event are present")
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending', blank=True)
    # num_of_attendees = models.PositiveIntegerField(default=0, blank=True)
    # join = models.BooleanField(default= False)
    # join = models.ForeignKey(Join, on_delete=models.CASCADE)
    def __str__(self):
        return self.InitiativeTitle

    def __unicode__(self):
        return self.title

    def get_post_url(self):
        return reverse('post_edit', kwargs={'pk': self.pk})

    def list(self):
        return self.attendees

# class Joining(models.Model):
#     blog_posts = models.ForeignKey(blog_posts,verbose_name='blog_posts', on_delete=models.CASCADE)
#     user = models.ForeignKey(User,verbose_name='Joinee',on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username



# def join(self, user):
#     joining = Joining.objects.create(user = user,
#                                                     blog_posts = self,
#                                                     )

# def unjoin(self, user):
#     Joining = Joining.objects.get(user = user, blog_posts = self)
#     Joining.delete()
