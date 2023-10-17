from django.shortcuts import render, redirect
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

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
          datafile = request.FILES['image']
          #รับค่าจากฟอร์ม
          name = request.POST['name']
          category = request.POST['category']
          description = request.POST['description']
          content = request.POST['content']
          writer = auth.get_user(request)

          if str(datafile.content_type).startswith('image'):
            #อัพโหลด
            fs = FileSystemStorage()
            img_url = 'blogsImages/' + datafile.name
            filename = fs.save(img_url, datafile)
            #บันทึกข้อมูลบทความ
            blog = Blogs(name=name, category_id=category, description=description, content=content, writer=writer, image=img_url)
            blog.save()
            messages.info(request, 'บันทึกข้อมูลเรียบร้อย')
            return redirect('displayForm')
          else:
              messages.info(request, 'ไฟล์ที่อัพโหลดไม่รองรับ กรุณาอัพโหลดไฟล์รูปภาพอีกครั้ง')
              return redirect('displayForm')