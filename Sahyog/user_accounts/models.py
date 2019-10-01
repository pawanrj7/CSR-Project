from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    Individual = 'Individual'
    Company = 'Company'
    Category_CHOICES = ((Individual, 'Individual'), (Company, 'Company'))
    category= models.CharField(max_length=100,choices=Category_CHOICES,default=Individual)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.BigIntegerField()

    # companies = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='companies', blank=True)

    def __str__(self):
        return self.user.username



    # def company_list(self):
    #     return self.__str__().filter(category = 'company')
    
    # def list(self):
    #     return self.attendees