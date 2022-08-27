from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, BlogPostForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Blog_post
from django.contrib.auth.models import Group
from django.core.cache import cache


#Home.html
def home(request):
    posts = Blog_post.objects.all()
    return render(request, 'blog/home.html', {'posts' : posts})

#About.html
def about(request):
    return render(request, 'blog/about.html')

#Contact.html
def contact(request):
    return render(request, 'blog/contact.html')

#Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Blog_post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grps = user.groups.all()
        ip = request.session.get('ip', 0)
        ct = cache.get('count', version=user.pk)
        return render(request, 'blog/dashboard.html', {'posts' : posts, 'full_name' : full_name, 'groups' : grps, 'ip' : ip, 'ct' : ct})
    else:
        return HttpResponseRedirect('/login/')

#Signup
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Signup Successfull!")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:        
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form' : form})

#Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
                form = LoginForm(request=request, data=request.POST)
                if form.is_valid():
                    uname = form.cleaned_data['username']
                    upass = form.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None: 
                            login(request, user)
                            messages.success(request, 'Login Successful!!')
                            return HttpResponseRedirect('/dashboard/')
        else:        
            form = LoginForm()
        return render(request, 'blog/login.html', {'form' : form})
    else:
        return HttpResponseRedirect('/dashboard/')

#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')    #When user clicks on Logout button, he should be directed to Home Page

#Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogPostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                author = form.cleaned_data['author']
                desc = form.cleaned_data['desc']
                pst = Blog_post(title=title, author=author, desc=desc)
                pst.save()
                messages.success(request, "Post successfully added!")
                form = BlogPostForm()
        else:
                form = BlogPostForm()
        return render(request, 'blog/addpost.html', {'form' : form})
    else:
        return HttpResponseRedirect('/login/')

#Update New Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Blog_post.objects.get(pk=id)
            form = BlogPostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, "Post successfully Updated!")
        else:
            pi =  Blog_post.objects.get(pk=id)
            form = BlogPostForm(instance = pi)    
        return render(request, 'blog/updatepost.html', {'form' : form})
    else:
        return HttpResponseRedirect('/login/')

#Delete New Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Blog_post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

