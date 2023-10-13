from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
def index(request):
	categories = Category.objects.all()
	blogs = Blogs.objects.all()
	latest = Blogs.objects.all().order_by('-pk')[:4]

	# บทความยอดนิยม
	popular = Blogs.objects.all().order_by('-views')[:3]
	
	#บทความแนะนำ
	suggestion = Blogs.objects.all().order_by('views')[:3]
	
	# pagination
	paginator = Paginator(blogs, 2)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	
	try:
		blogPerpage = paginator.page(page)
	except (EmptyPage, InvalidPage):
		blogPerpage = paginator.page(paginator.num_pages)


	return render(request, 'frontend/index.html', {'categories': categories, 'blogs': blogPerpage, 'latest': latest, 'popular':popular, 'suggestion':suggestion})

def blogDetail(request,id):
	categories = Category.objects.all()
	# บทความยอดนิยม
	popular = Blogs.objects.all().order_by('-views')[:3]

	#บทความแนะนำ
	suggestion = Blogs.objects.all().order_by('views')[:3]
	
	singleblog = Blogs.objects.get(id=id)
	singleblog.views = singleblog.views+1
	singleblog.save()
	return render(request,'frontend/blogDetail.html',{'blog':singleblog, 'categories': categories, 'popular':popular, 'suggestion':suggestion})

def searchCategory(request, cat_id):
	categories = Category.objects.all()
	# บทความยอดนิยม
	popular = Blogs.objects.all().order_by('-views')[:3]

	#บทความแนะนำ
	suggestion = Blogs.objects.all().order_by('views')[:3]

	#ชื่อหมวดหมู่
	categoryName = Category.objects.get(id=cat_id)
	
	blogs = Blogs.objects.filter(category_id=cat_id)
	return render(request, 'frontend/searchCategory.html', {'blogs':blogs, 'categories': categories, 'popular':popular, 'suggestion':suggestion, 'categoryName':categoryName})

def searchWriter(request, writer):
	categories = Category.objects.all()
	# บทความยอดนิยม
	popular = Blogs.objects.all().order_by('-views')[:3]

	#บทความแนะนำ
	suggestion = Blogs.objects.all().order_by('views')[:3]
	
	blogs = Blogs.objects.filter(writer=writer)
	writerName = Blogs.objects.get(id=writer) 
	return render(request, 'frontend/writer.html', {'blogs':blogs, 'categories': categories, 'popular':popular, 'suggestion':suggestion, 'writerName':writerName})