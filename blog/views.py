from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import Post, marketing, comment, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import postForm, commentForm

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



def home(request):

    postShow = Post.objects.filter(featured=True)[0:3]
    post = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST['email']
        mark = marketing()
        mark.email = email
        mark.save()
        messages.success(request, 'Thanks For Subscribe')

    context = {'post': postShow, 'latest': post, 'title':"Home Page"}
    return render(request, 'index.html', context)


def blog(request):
    latest = Post.objects.order_by('timestamp')[:3]
    cat = Category.objects.all()
    post = Post.objects.all()
    p = Paginator(post, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    # print(p.num_pages)
    try:
        paginated_queryset = p.page(page)

    except PageNotAnInteger:
        paginated_queryset = p.page(1)

    except EmptyPage:
        paginated_queryset = p.page(p.num_pages)

    context = {'post': post, 'paginated_queryset': paginated_queryset,
               'page_request_var': page_request_var, 'cat': cat, 'latest':latest, 'title':"Blog"}
    return render(request, 'blog.html', context)





def postpage(request, id):
    cat = Category.objects.all()
    comm = comment.objects.filter(postby = id).order_by('-timestamp')
    com = commentForm()
    post = Post.objects.get(pk=id)
    post.views += 1
    post.save()
    # print(post.views)
    if request.method == "POST":
        com = commentForm(request.POST)
        com.instance.user = request.user
        com.instance.postby = post

        if com.is_valid():
            com.save()
            messages.success(request, 'successfull Post Your Comment')
            context={'com':com}
        return redirect(reverse("postpage", kwargs={
                'id': post.pk
            }))
            

    context = {'post': post, 'com':com, 'comment':comm, 'cat':cat, 'title':"Post" }
    
    return render(request, 'post.html', context)


def search(request):
    val = request.GET['sea']
    searchTitle = Post.objects.filter(title__icontains=val)
    searchOverview = Post.objects.filter(overview__icontains=val)
    searchPost = searchTitle.union(searchOverview)
    # print(searchPost)
    context = {'searchPost': searchPost, 'title':"Search"}
    return render(request, 'search.html', context)


def createPost(request):
    form = postForm()
    if request.method == "POST":
        form = postForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()

        return redirect('postpage', id=form.instance.id)
    context = {'form': form , 'title':"Create Post"}
    return render(request, 'createPost.html', context)


def updatePost(request, id):
    ids = Post.objects.get(pk=id)
    form = postForm(instance=ids)
    if request.method == "POST":
        form = postForm(request.POST or None,
                        request.FILES or None, instance=ids)
        if form.is_valid():
            form.save()

        return redirect('postpage', id=form.instance.id)

    context = {'form': form, 'title':"Update"}
    return render(request, 'createPost.html', context)


def deletePost(request, id):
    post = Post.objects.filter(id=id)
    post.delete()
    return redirect('blog')


def handleSignup(request):

    username = request.POST['username']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']

    # if len(username) < 10:
    #     messages.error(request, "username must contain 10 character")
    #     return redirect('home')

    # if not username.isalnum():
    #     messages.error(request, "username must be alphanumeric")
    #     return redirect('home')

    # if pass1 != pass2:
    #     messages.error(request, "password must be same")
    #     return redirect('home')

    if request.method == "POST":
        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = firstname
        myUser.last_name = lastname
        myUser.save()
        messages.success(request, 'successfull Sign up Click " Log in "  ')
        return redirect('home')
    else:
        return HttpResponse('ok')

def handleLogin(request):

    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully')
            return redirect('home')
        else:
            messages.error(request, 'try again Later')
            return redirect('home')

    return HttpResponse('404 -page Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'successfull log out')
    return redirect('home')
    # return HttpResponse('404 -page Not Found')
