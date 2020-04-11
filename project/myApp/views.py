#视图配置页

from django.shortcuts import render, render_to_response
from django import forms
from .models import User, Teacher, Student
from django.db import models
# Create your views here.
from django.http import HttpResponse

def index(request):  #返回给模板index.html
    return render(request, 'myApp/index.html')


class UserForm_regist(forms.Form):   #注册表单
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')
    gender = forms.BooleanField(required=False,label='性别：男')
    age = forms.IntegerField(label='年龄')
    grade = forms.IntegerField(label='班级')
    isTeacher = forms.CharField(required=False, label='老师密钥（可不填)')

class UserForm_login(forms.Form):   #登录表单
    #username = forms.CharField(label='用户名',max_length=50)
    email = forms.EmailField(label='邮箱')#修改
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    isTeacher = forms.CharField(required=False, label='老师密钥（可不填)')


TeacherPassword = "12345678"#老师身份验证的密码


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def regist(request):   #注册函数
    if request.method == 'POST':
        userform = UserForm_regist(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']
            gender = userform.cleaned_data['gender']
            age = userform.cleaned_data['age']
            grade = userform.cleaned_data['grade']
            isTeacher = userform.cleaned_data['isTeacher']

            user = User.objects.create(username=username,password=password,email=email,gender=gender,age=age,grade=grade,isTeacher=isTeacher)
            user.save()

            if (isTeacher == ""):
                student = Student.objects.create(sname=username,sgender=gender,sage=age,sgrade=grade,semail=email,isDelete=False)
                student.save()
                return HttpResponse('Student registered!!!')

            if (isTeacher != TeacherPassword):
                student = Student.objects.create(sname=username,sgender=gender,sage=age,sgrade=grade,semail=email,isDelete=False)
                student.save()
                return HttpResponse('Student registered!!!')

            if (isTeacher == TeacherPassword):
                teacher = Teacher.objects.create(sname=username,sgender=gender,sage=age,sgrade=grade,semail=email,isDelete=False)
                teacher.save()
                return HttpResponse('Teacher registered!!!')
    else:
        userform = UserForm_regist()
    return render_to_response('myApp/regist.html',{'userform':userform})#error



from django.views.decorators.csrf import csrf_exempt
from .models import Teacher
@csrf_exempt
def login(request):   #登录函数
    if request.method == 'POST':
        userform = UserForm_login(request.POST)
        if userform.is_valid():
            #username = userform.cleaned_data['username']
            email = userform.cleaned_data['email']#修改3
            password = userform.cleaned_data['password']
            isTeacher = userform.cleaned_data['isTeacher']

            user = User.objects.filter(email__exact=email, password__exact=password)#修改4
            if user and isTeacher == TeacherPassword:
                teacher = Teacher.objects.get(semail=email)#修改5
                return render_to_response('myApp/info_teacher.html',{'teacher':teacher})

            if user and isTeacher == "":
                student = Student.objects.get(semail=email)#修改6
                return render_to_response('myApp/info_student.html',{'student':student})

            if user and isTeacher != TeacherPassword:
                student = Student.objects.get(semail=email)
                return render_to_response('myApp/info_student.html',{'student':student})

            if user == False:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm_login()
    return render_to_response('myApp/login.html',{'userform':userform})

