from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import reverse

class Post(models.Model):
    
    categories = [('National', 'National'), ('International', 'International'),
                  ('Politics', 'Politics'), ('Health', 'Health'), ('Science & Tech.', 'Science & Tech.'), 
                  ('Sports', 'Sports'), ('Entertainment', 'Entertainment'), ('Other', 'Other')]

    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = RichTextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=categories)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title + " -- " + self.author.username 

    def get_absolute_url(self):
        return reverse("blog:blogPost", kwargs = {'pk': self.pk})
    

class Comment(models.Model):

    sno = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Comment By : " + self.owner.username 