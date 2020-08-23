from django.shortcuts import render, reverse, redirect, get_object_or_404,HttpResponseRedirect
from blog.models import Post, Comment
from blog.forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
"""
def blogHome(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'blog/blogHome.html', {'posts':posts})
"""
def blogPost(request, pk):
    post = Post.objects.filter(sno=pk).first()
    comments = post.comments.all().order_by('-timestamp')
    return render(request, 'blog/blogPost.html', {'post':post, 'comments':comments})

# Class Based Views Look ForThe Below Template By Default:
# <appname>/<model>_<viewtype>.html

class PostListView(ListView):
    model = Post
    template_name = 'blog/blogHome.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']


class UserPostListView(ListView):
    model = Post
    template_name = 'home/user_posts.html'
    context_object_name = 'posts'

    # We will override the method which returns the queryset
    # for ListView by filtering with user.
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-timestamp')


# class PostDetailView(DetailView):
# In the template, elements of models can be accessed by using
# the word 'object'.  Eg: 'object.title' instead of 'post.title'
# But here we are renaming it.
# PostDetailView must be called with either an object pk or a slug in the URLconf.
#     model = Post
#     template_name = 'blog/blogPost.html'
#     context_object_name = 'post'


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    # This requires 'post_confirm_delete.html' template by default
    model = Post
    success_url = '/blog/'
    # Test for UserPassesTestMixin : To check whether logged in
    # user is author of the current post.
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False


class PostCreateView(LoginRequiredMixin, CreateView):
  
    model = Post
    fields = ['title', 'category', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = ['title', 'category', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, 'Your Account Has Been Created! Please Login.')
            return redirect('home:login')

    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account Successfully Updated !')
            return redirect('blog:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'blog/update.html', {'form':form})


@login_required
def new(request):
    if request.method == 'POST':

        author = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')

        if len(title) != 0 and len(content) != 0 and len(category) != 0 :
            post = Post.objects.create(author=author, title=title, category=category, content=content)
            post.save()
            messages.success(request, "New Post Created Successfully !")
            return redirect('blog:blogHome')
        else:
            messages.error(request, "Please Enter Valid Information.")

    return render(request, 'blog/post_form.html')


@login_required
def post_update(request, sno):

    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')

        if len(title) != 0 and len(content) != 0 and len(category) != 0 :
            post = Post.objects.get(sno=sno)    # .get returns single object.
            post.author = author
            post.title = title
            post.content = content
            post.category = category
            post.save()
            messages.success(request, "Post Updated Successfully !")
            # print("POST")
            return HttpResponseRedirect(reverse('blog:blogPost', args=[post.sno]))

    else:   
        # print("GET")
        post = Post.objects.filter(sno=sno).first()     # .filter returns QuerySet.
        return render(request, 'blog/post_update.html', {'post':post})


@login_required
def comment(request, sno):
    if request.method == "POST":
        post = Post.objects.filter(sno=sno).first()
        owner = request.user
        content = request.POST.get('content')
        if len(content) > 0:
            comment = Comment.objects.create(post=post, owner=owner, content=content)
            print("Comment Saved !")
            messages.success(request, "Comment Added Successfully !")
        else:
            messages.error(request, 'Invalid Comment')
        url = f'blog/blogPost/{post.sno}'
        # reverse : generates the url string based on view name and parameters.
        return HttpResponseRedirect(reverse('blog:blogPost', args=[post.sno]))