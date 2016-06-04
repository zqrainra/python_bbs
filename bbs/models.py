from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=254)
    category = models.ForeignKey('Category')
    content = models.TextField(max_length=10240)
    author = models.ForeignKey('UserProfile')
    publish_date = models.DateTimeField(auto_now_add=True)
    brief = models.TextField(max_length=256)
    #thumb_up = models.ForeignKey('Thumb_up',blank=True)
    #comments = models.ManyToManyField('Comment',blank=True,related_name='article_to_comment')
    head_img = models.ImageField(upload_to='statics/imgs/upload')

    def __unicode__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(unique=True,max_length=64)
    admins = models.ManyToManyField('UserProfile')

    def __unicode__(self):
        return self.name

class ThumbUp(models.Model):
    article = models.ForeignKey('Article')
    user = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.article

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    user_groups = models.ManyToManyField('UserGroup')
    friends = models.ManyToManyField('self',related_name='my_friends')

    def __unicode__(self):
        return '%s' %(self.user)

class UserGroup(models.Model):
    name = models.CharField(max_length=32,unique=True)

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    article = models.ForeignKey('Article')
    user = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=1024)
    parent_comment = models.ForeignKey('self',blank=True,null=True,related_name='pid')

    def __unicode__(self):
        return self.comment