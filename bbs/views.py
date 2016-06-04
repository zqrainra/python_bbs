from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
import  utility
import json
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.



def account_login(request):

    if request.method == 'GET':
        return  render(request,'login.html')

    else:
        print request.POST
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        user = authenticate(username=username,password=passwd)
        if user is not None:
            login(request,user)
            user.userprofile.online = True
            user.userprofile.save()
            return  HttpResponseRedirect("/")
        else:
            return  render(request,'login.html',{
                'login_err': "Wrong username or password!"
            })

def account_logout(request):
    logout(request)
    return render(request,'login.html')

def index(request):
    article_list = models.Article.objects.all().order_by("-id")
    paginator = Paginator(article_list, 2)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request,'index.html',{
        'articles': articles
    })


def create_article(request):
    if request.method == 'POST':
        # print request.POST
        article = utility.Bbs_generater(request)
        bbs = article.create()
        html_res = '''Article <a href="/detail/%s/">%s</a> is created successful! ''' % (bbs.id,bbs.title)
        return HttpResponse(html_res)
    elif request.method == 'GET':
        category = models.Category.objects.all()
        return render(request,'create_article.html',{'category':category})

def life(request):

    return  render(request,'life.html')

def tech(request):

    return  render(request,'tech.html')
def category1024(request):
    aaa = 'aaa'
    return  render(request,'1024.html',{'aaa':aaa})

def detail(request,article_id):
    try:
        article = models.Article.objects.get(id=article_id)
        comment = utility.create_comment_tree(request,article_id)
    except ObjectDoesNotExist,e:
        err_msg = str(e)

    return render(request,'article.html',{'article':article,'comment':comment})

def thumb_up(request,article_id):
    try:
        article = models.Article.objects.get(id=article_id)
    except ObjectDoesNotExist,e:
        err_msg = str(e)

    user = request.user.userprofile
    data_list = {
    'user' : user,
    'article' : article,
    }
    thumb = models.ThumbUp(**data_list)
    thumb.save()
    return HttpResponseRedirect('/')
