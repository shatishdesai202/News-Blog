from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.urls import reverse



User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

    

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class Post(models.Model):
    title = models.CharField(max_length=150)
    postImage = models.ImageField()
    overview = models.TextField()
    detail = RichTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, null=True)
    featured = models.BooleanField()
    views = models.IntegerField(default=1)
    previous_post = models.ForeignKey('self',
                                 related_name='p_post',
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,default="none")
    
    next_post = models.ForeignKey('self',
                                 related_name='n_post',
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,default="none")
    
   
    def __str__(self):
        return self.title + "-->" +self.overview

    def get_absolute_url(self):
        return reverse('postpage', kwargs={
            'id': self.id
        })

    @property
    def get_comments(self):
        return self.comments.filter(postby = self.id)

class marketing(models.Model):
    email = models.EmailField(null=True , blank=True)

    def __str__(self):
        return self.email
    
class comment(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    postby = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.content