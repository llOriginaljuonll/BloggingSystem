from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'backend/login_register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if username == '' or email == '' or password == '' or repassword == '':
            messages.info(request, 'กรุณาป้อนป้อนข้อมูลให้ครบ')
            return redirect('member')
        else:
            if password == repassword :
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password
                )
                user.save()
                messages.info(request, 'สร้างบัญชีเรียบร้อย')
                return redirect('member')
            else:
                messages.info(request, 'ไม่สามารถลงทะเบียนได้รหัสผ่านไม่ตรงกัน')
                return redirect('member')