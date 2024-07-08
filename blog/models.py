from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email = models.EmailField(max_length = 100, unique = True)
    username = models.CharField(blank = True,null = True,max_length = 30,unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self,*args,**kwargs):
        self.email = self.email.lower()
        return super().save(*args,**kwargs)
    @property
    def get_profile(self):
        return ProfileModel.objects.get_or_create(user=self)[0]
    
@receiver(post_save,sender = CustomUser)
def save_username_when_user_is_created(sender,instance,created,*args,**kwargs):
    if created:
        email = instance.email
        sliced_email = email.split('@')[0]
        instance.username = sliced_email
        instance.save()

class ProfileModel(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,unique=True,related_name='profile')
    bio = models.TextField(null=True,blank=True)
    

class Post(models.Model):
    Title = models.CharField(max_length=100)
    Content = models.TextField(max_length=100)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Published_Date = models.DateTimeField(auto_now=True)
    slug = models.SlugField( blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Title

class Comment(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Content = models.TextField()
    Created_date = models.DateTimeField(auto_now=True)
