from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

import datetime

from .models import Article

# Create your views here.

def home(request):
	'''#return HttpResponse("hello world,django.")
	post_list = Article.objects.all()
	return render(request,'home.html',{'post_list' : post_list})'''
	posts = Article.objects.all()
	paginator = Paginator(posts,2)  #each page show 2 passages
	page = request.GET.get('page')
	try:
		post_list = paginator.page(page)
	except PageNotAnInteger:
		post_list = paginator.page(1)
	except EmptyPage:
		post_list = paginator.paginator(paginator.num_pages)
	return render(request,'home.html',{'post_list':post_list})

def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)
def test_time(request):
	return render(request,'test.html',{'current_time':datetime.datetime.now()})

def detail1(request, my_args):
	#return HttpResponse("You're looking at my_args %s." % my_args)
	post = Article.objects.all()[int(my_args)]
	str = ("title = %s, category = %s, date_time = %s, content = %s" % (post.title, post.category, post.date_time, post.content))
	return HttpResponse(str)

def detail(request,id):
	try:
		post = Article.objects.get(id=int(id))  #id:unicode -> int
	except Article.DoesNotExist:
		raise Http404
	return render(request,'post.html',{'post':post})

def archives(request):## simple list
	try:
		post_list = Article.objects.all()
	except Article.DoesNotExist:
		raise Http404
	return render(request,'archives.html',{'post_list' : post_list,'error':False})

def about_me(request):
	return render(request,'aboutme.html')

def search_tag(request,tag):
	try:
		post_list = Article.objects.filter(category__icontains = tag)
	except Article.DoesNotExist:
		raise Http404
	return render(request, 'tag.html', {'post_list' : post_list})

def blog_search(request):
	if 's' in request.GET:
		s = request.GET['s']
		if not s:
			return render(request,'home.html')
		else:
			post_list = Article.objects.filter(title__icontains = s)
			if len(post_list) == 0:
				return render(request,'archives.html', {'post_list' : post_list,'error' : True})
			else:
				return render(request,'archives.html', {'post_list' : post_list,'error' : False})

class RSSFeed(Feed):
	title = "RSS feed - article"
	link = "feeds/posts"
	description = "RSS feed - blog posts"

	def items(self):
		return Article.objects.order_by('-date_time')

	def item_title(self,item):
		return item.title
	def item_pubdate(self,item):
		return item.date_time
	def item_description(self,item):
		return item.content
