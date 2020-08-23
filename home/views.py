from django.shortcuts import render, HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    
    if request.method == 'POST':

        name = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # print(name, email, phone, content)
        if len(name) < 2 or len(email) < 2 or len(phone) < 2 or len(content) < 5:
            messages.error(request, "Invalid Form Content !")
        else:
            messages.success(request, "Your Form Has Been Sent Successfully !")
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()

    return render(request, 'home/contact.html')


def search(request):

    if request.method == "GET":
        search_query = request.GET['search_query']
        if len(search_query) > 100:
            posts = []
        else:
            title_posts = Post.objects.filter(title__icontains=search_query)
            content_posts = Post.objects.filter(content__icontains=search_query)
            
            posts = title_posts.union(content_posts)

        return render(request, 'home/search.html', {'posts':posts, 'query':search_query})
