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

class UserForm_teacher(forms.Form):   #教师修改信息表单
    sname = forms.CharField(label='姓名',max_length=50)
    sgender = forms.BooleanField(required=False,label='性别：男')
    sage = forms.IntegerField(label='年龄')
    sgrade = forms.IntegerField(label='班级')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

class UserForm_student(forms.Form):   #学生修改信息表单
    sname = forms.CharField(label='姓名',max_length=50)
    sgender = forms.BooleanField(required=False,label='性别：男')
    sage = forms.IntegerField(label='年龄')
    sgrade = forms.IntegerField(label='班级')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')


class UserForm_login(forms.Form):   #登录表单
    username = forms.CharField(label='用户名',max_length=50)
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
                student = Student.objects.create(sname=username,sgender=gender,sage=age,sgrade=grade,isDelete=False)
                student.save()
                return HttpResponse('Student registered!!!')

            if (isTeacher != TeacherPassword):
                student = Student.objects.create(sname=username,sgender=gender,sage=age,sgrade=grade,isDelete=False)
                student.save()
                return HttpResponse('Student registered!!!')

            if (isTeacher == TeacherPassword):
                teacher = Teacher.objects.create(sname=username,sgender=gender,sage=age,sgrade=grade,isDelete=False)
                teacher.save()
                return HttpResponse('Teacher registered!!!')
    else:
        userform = UserForm_regist()
    return render_to_response('myApp/regist.html',{'userform':userform})#error



from .models import Teacher
@csrf_exempt
def login(request):   #登录函数
    if request.method == 'POST':
        userform = UserForm_login(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            isTeacher = userform.cleaned_data['isTeacher']

            user = User.objects.filter(username__exact=username,password__exact=password)
            if user and isTeacher == TeacherPassword:
                teacher = Teacher.objects.get(sname=username)
                return render_to_response('myApp/info_teacher.html',{'teacher':teacher})

            if user and isTeacher == "":
                student = Student.objects.get(sname=username)
                return render_to_response('myApp/info_student.html',{'student':student})

            if user and isTeacher != TeacherPassword:
                student = Student.objects.get(sname=username)
                return render_to_response('myApp/info_student.html',{'student':student})

            if user == False:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm_login()
    return render_to_response('myApp/login.html',{'userform':userform})



def check_teacher_info(request,num):   #查看老师个人信息
    teacher = Teacher.objects.get(pk=num)
    user = User.objects.get(username=teacher.sname)
    return render_to_response('myApp/check_teacher_info.html', {'teacher': teacher,'user': user})


def check_student_info(request,num):   #查看学生个人信息
    student = Student.objects.get(pk=num)
    user = User.objects.get(username=student.sname)
    return render_to_response('myApp/check_student_info.html', {'student': student,'user': user})



@csrf_exempt
def alter_teacher_info(request,num):   #修改老师个人信息
    if request.method == 'POST':
        userform = UserForm_teacher(request.POST)
        if userform.is_valid():
            sname = userform.cleaned_data['sname']
            sgender = userform.cleaned_data['sgender']
            sage = userform.cleaned_data['sage']
            sgrade = userform.cleaned_data['sgrade']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            teacher=Teacher.objects.get(pk=num)
            User.objects.filter(username=teacher.sname).update(password=password,email=email)
            Teacher.objects.filter(pk=num).update(sname=sname,sgender=sgender,sage=sage,sgrade=sgrade)

            return HttpResponse('成功修改老师信息！')
    else:
        userform = UserForm_teacher()
    return render_to_response('myApp/alter_teacher_info.html',{'userform':userform})


@csrf_exempt
def alter_student_info(request,num):   #修改学生个人信息
    if request.method == 'POST':
        userform = UserForm_student(request.POST)
        if userform.is_valid():
            sname = userform.cleaned_data['sname']
            sgender = userform.cleaned_data['sgender']
            sage = userform.cleaned_data['sage']
            sgrade = userform.cleaned_data['sgrade']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            student=Student.objects.get(pk=num)
            User.objects.filter(username=student.sname).update(password=password,email=email)
            Student.objects.filter(pk=num).update(sname=sname,sgender=sgender,sage=sage,sgrade=sgrade)

            return HttpResponse('成功修改学生信息！')
    else:
        userform = UserForm_student()
    return render_to_response('myApp/alter_student_info.html',{'userform':userform})