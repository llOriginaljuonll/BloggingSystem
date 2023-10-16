from django.shortcuts import render, redirect
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required(login_url='member')
def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum('views'))
    return render(request, 'backend/index.html', {'blogs':blogs, 'writer':writer, 'blogCount':blogCount, 'total':total})

def displayForm(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum('views'))
    categories = Category.objects.all()
    return render(request, 'backend/blogForm.html', {'blogs':blogs, 'writer':writer, 'blogCount':blogCount, 'total':total, 'categories':categories})
    
def insertData(request):
	if request.method == 'POST' and request.FILES['image']:
          image = request.FILES['image']
          fs = FileSystemStorage()
          #อัพโหลด
          img_url = 'blogImages/' + image.name
          filename = fs.save(img_url + image.name, image)
          return redirect('displayForm')