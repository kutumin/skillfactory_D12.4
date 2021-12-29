from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import datetime

# Test

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )
                  
    def save(self, request):
        user = super(BaseRegisterForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class Author(models.Model):
    full_name = models.CharField(max_length = 255)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    raiting = models.IntegerField(default = 1)

    def __str__(self):
        return f'{self.user}'

    def update_raiting(self):
        post_raiting = self.post_set.all().aggregate(sumraiting = Sum('post_raiting'))
        authors_post_raiting = 0
        authors_post_raiting = authors_post_raiting + post_raiting.get('sumraiting')

        comment_raiting = self.user.comment_set.all().aggregate(sumraiting1 = Sum('comment_raiting'))
        authors_comment_raiting = 0
        authors_comment_raiting = authors_comment_raiting + comment_raiting.get('sumraiting1')
   
        authors_post_comment_raiting = 0
        j=[]
        m=0
        for i in self.post_set.all():
                j.append(i)
                comment_raiting3 = self.user.comment_set.filter(post=j[m]).aggregate(sumraiting1 = Sum('comment_raiting'))
                authors_post_comment_raiting += comment_raiting3.get('sumraiting1')
                m=m+1 
            
        self.raiting = 3 * authors_post_raiting + authors_post_comment_raiting + authors_comment_raiting
        self.save()
    
class Category(models.Model):
    category_name = models.CharField(max_length = 255, unique = True)	
    def __str__(self):
        return f'{self.category_name}'

class Post(models.Model):
    post = 'PO'
    news = 'NW'
    POSITIONS=[
    (post,'post'), 
    (news,'news'),]
    post_author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices= POSITIONS)
    post_date_created = models.DateField(auto_now_add = True)
    post_detailed_data_created = models.TimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    head_of_post = models.CharField(max_length = 255)
    article_text = models.TextField()
    post_raiting = models.IntegerField(default = 1)

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()

    def preview(self):
        review = self.article_text[:124]+'...'
        return review
 
    def get_absolute_url(self): 
        return f'/news/{self.id}' 

    def __str__(self):
        return f'{self.post_author}:{self.article_text}'

class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User,on_delete = models.CASCADE)
    comment_text = models.TextField()
    comment_date_created = models.DateField(auto_now_add = True)
    comment_raiting = models.IntegerField(default = 1) 
    
    def like(self):
        self.comment_raiting +=1
        self.save()
    
    def dislike(self):
        self.comment_raiting -=1
        self.save()

class Subscriber(models.Model):
    email = models.EmailField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.email

