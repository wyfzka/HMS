# 视图配置页

from django.shortcuts import render, render_to_response
from django import forms
from .models import User, Teacher, Student, Teacher_grade
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):  # 返回给模板index.html
    return render(request, 'myApp/preparation/index.html')


class UserForm_regist(forms.Form):  # 注册表单
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')
    gender = forms.BooleanField(required=False, label='性别：男')
    age = forms.IntegerField(label='年龄')
    grade = forms.CharField(required=False, label='班级号（老师不填)', max_length=20)
    isTeacher = forms.CharField(required=False, label='老师密钥（学生不填)')


class UserForm_login(forms.Form):  # 登录表单
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    isTeacher = forms.CharField(required=False, label='老师密钥（学生不填)')


class UserForm_teacher(forms.Form):  # 教师修改信息表单
    sname = forms.CharField(label='姓名', max_length=50)
    sgender = forms.BooleanField(required=False, label='性别：男')
    sage = forms.IntegerField(label='年龄')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')


class UserForm_student(forms.Form):  # 学生修改信息表单
    sname = forms.CharField(label='姓名', max_length=50)
    sgender = forms.BooleanField(required=False, label='性别：男')
    sage = forms.IntegerField(label='年龄')
    sgrade = forms.CharField(label='班级号', max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')


class UserForm_teacher_add_grade(forms.Form):  # 添加老师所教班级表单
    grade1 = forms.CharField(required=False, label='所教班级号1(非必填)', max_length=20)
    grade2 = forms.CharField(required=False, label='所教班级号2(非必填)', max_length=20)
    grade3 = forms.CharField(required=False, label='所教班级号3(非必填)', max_length=20)


class UserForm_teacher_delete_grade(forms.Form):  # 删除老师所教班级表单
    grade1 = forms.CharField(required=False, label='删除所教班级号1(非必填)', max_length=20)
    grade2 = forms.CharField(required=False, label='删除所教班级号2(非必填)', max_length=20)
    grade3 = forms.CharField(required=False, label='删除所教班级号3(非必填)', max_length=20)


TeacherPassword = "12345678"  # 老师身份验证的密码


@csrf_exempt
def regist(request):  # 注册函数
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

            if isTeacher == "":
                user = User.objects.create(username=username, password=password, email=email, gender=gender, age=age,
                                           grade=grade, isTeacher=-1)
                user.save()
                student = Student.objects.create(sname=username, sgender=gender, sage=age, sgrade=grade, semail=email, isDelete=False)
                student.save()
                return HttpResponse('Student registered!!!')

            if isTeacher != TeacherPassword:
                user = User.objects.create(username=username, password=password, email=email, gender=gender, age=age,
                                           grade=grade, isTeacher=-1)
                user.save()
                student = Student.objects.create(sname=username, sgender=gender, sage=age, sgrade=grade, semail=email,
                                                 isDelete=False)
                student.save()
                return HttpResponse('Student registered!!!')

            if isTeacher == TeacherPassword:
                user = User.objects.create(username=username, password=password, email=email, gender=gender, age=age,
                                           grade=-1, isTeacher=isTeacher)
                user.save()
                teacher = Teacher.objects.create(sname=username, sgender=gender, sage=age, semail=email, isDelete=False)
                teacher.save()
                return HttpResponse('Teacher registered!!!')
    else:
        userform = UserForm_regist()
    return render_to_response('myApp/preparation/regist.html', {'userform': userform})  # error


@csrf_exempt
def login(request):  # 登录函数
    if request.method == 'POST':
        userform = UserForm_login(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']
            password = userform.cleaned_data['password']
            isTeacher = userform.cleaned_data['isTeacher']

            user = User.objects.filter(email__exact=email, password__exact=password)
            if user and isTeacher == TeacherPassword:
                teacher = Teacher.objects.get(semail=email)
                return render_to_response('myApp/preparation/info_teacher.html', {'teacher': teacher})

            if user and isTeacher == "":
                student = Student.objects.get(semail=email)
                return render_to_response('myApp/preparation/info_student.html', {'student': student})

            if user and isTeacher != TeacherPassword:
                student = Student.objects.get(semail=email)
                return render_to_response('myApp/preparation/info_student.html', {'student': student})

            if not user:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm_login()
    return render_to_response('myApp/preparation/login.html', {'userform': userform})


def check_teacher_info(request, num):  # 查看老师个人信息
    teacher = Teacher.objects.get(pk=num)
    user = User.objects.get(username=teacher.sname)
    teacher_grade_List = Teacher_grade.objects.filter(teacher_id=teacher.pk)
    return render_to_response('myApp/preparation/check_teacher_info.html',
                              {'teacher': teacher, 'user': user, 'teacher_grade_List': teacher_grade_List})


def check_student_info(request, num):  # 查看学生个人信息
    student = Student.objects.get(pk=num)
    user = User.objects.get(username=student.sname)
    return render_to_response('myApp/preparation/check_student_info.html', {'student': student, 'user': user})


@csrf_exempt
def alter_teacher_info(request, num):  # 修改老师个人信息
    if request.method == 'POST':
        userform = UserForm_teacher(request.POST)
        if userform.is_valid():
            sname = userform.cleaned_data['sname']
            sgender = userform.cleaned_data['sgender']
            sage = userform.cleaned_data['sage']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            teacher = Teacher.objects.get(pk=num)
            User.objects.filter(username=teacher.sname).update(password=password, email=email)
            Teacher.objects.filter(pk=num).update(sname=sname, sgender=sgender, sage=sage)

            return HttpResponse('成功修改老师信息！')
    else:
        userform = UserForm_teacher()
    return render_to_response('myApp/preparation/alter_teacher_info.html', {'userform': userform})


@csrf_exempt
def alter_student_info(request, num):  # 修改学生个人信息
    if request.method == 'POST':
        userform = UserForm_student(request.POST)
        if userform.is_valid():
            sname = userform.cleaned_data['sname']
            sgender = userform.cleaned_data['sgender']
            sage = userform.cleaned_data['sage']
            sgrade = userform.cleaned_data['sgrade']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            student = Student.objects.get(pk=num)
            User.objects.filter(username=student.sname).update(password=password, email=email)
            Student.objects.filter(pk=num).update(sname=sname, sgender=sgender, sage=sage, sgrade=sgrade)

            return HttpResponse('成功修改学生信息！')
    else:
        userform = UserForm_student()
    return render_to_response('myApp/preparation/alter_student_info.html', {'userform': userform})


@csrf_exempt
def add_teacher_grade(request, num):  # 添加老师所教班级
    if request.method == 'POST':
        userform = UserForm_teacher_add_grade(request.POST)
        if userform.is_valid():
            grade1 = userform.cleaned_data['grade1']
            grade2 = userform.cleaned_data['grade2']
            grade3 = userform.cleaned_data['grade3']

            teacher = Teacher.objects.get(pk=num)

            flag = False

            if grade1 != "":
                teacher_grade1 = Teacher_grade.objects.create(teacher_id=teacher.pk, teacher_name=teacher.sname,
                                                              grade=grade1)
                teacher_grade1.save()
                flag = True

            if grade2 != "":
                teacher_grade2 = Teacher_grade.objects.create(teacher_id=teacher.pk, teacher_name=teacher.sname,
                                                              grade=grade2)
                teacher_grade2.save()
                flag = True

            if grade3 != "":
                teacher_grade3 = Teacher_grade.objects.create(teacher_id=teacher.pk, teacher_name=teacher.sname,
                                                              grade=grade3)
                teacher_grade3.save()
                flag = True

            if flag:
                return HttpResponse('成功添加所教班级！')
    else:
        userform = UserForm_teacher_add_grade()
    return render_to_response('myApp/preparation/add_teacher_grade.html', {'userform': userform})


@csrf_exempt
def delete_teacher_grade(request, num):  # 删除老师所教班级
    if request.method == 'POST':
        userform = UserForm_teacher_delete_grade(request.POST)
        if userform.is_valid():
            grade1 = userform.cleaned_data['grade1']
            grade2 = userform.cleaned_data['grade2']
            grade3 = userform.cleaned_data['grade3']

            teacher = Teacher.objects.get(pk=num)

            flag = False

            if grade1 != "":
                Teacher_grade.objects.filter(grade=grade1, teacher_id=teacher.pk).delete()
                flag = True

            if grade2 != "":
                Teacher_grade.objects.filter(grade=grade2, teacher_id=teacher.pk).delete()
                flag = True

            if grade3 != "":
                Teacher_grade.objects.filter(grade=grade3, teacher_id=teacher.pk).delete()
                flag = True

            if flag:
                return HttpResponse('成功删除所教班级！')
    else:
        userform = UserForm_teacher_delete_grade()
    return render_to_response('myApp/preparation/delete_teacher_grade.html', {'userform': userform})
