import os
from datetime import datetime
from datetime import timedelta

from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response
from django import forms
from .models import User, Teacher, Student, Teacher_grade, Homework, Notice_student, Teacher_homework, Homework1
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from itertools import chain
from django.utils.encoding import escape_uri_path


class UserForm_launch_homework(forms.Form):  # 发布作业信息表单
    homework_content = forms.CharField(label='作业内容', max_length=50)
    deadline_days = forms.IntegerField(label='截止日期为多少天后')


class UserForm_alter_homework(forms.Form):  # 修改已发布的主观题
    homework_content = forms.CharField(label='作业内容', max_length=50)
    deadline_days = forms.IntegerField(label='截止日期为多少天后')


class UserForm_submit_homework(forms.Form):  # 提交作业信息表单
    handIn_homework = forms.FileField(label='提交作业内容')


class UserForm_correct_homework(forms.Form):  # 批改作业表单
    teacher_comment = forms.CharField(required=False, label='批改作业', max_length=200)
    isCorrect = forms.BooleanField(required=False, label='作业是否正确')


class UserForm_feedback_homework(forms.Form):  # 反馈作业表单
    feedback_homework = forms.FileField(label='提交反馈作业内容')
    feedback_comment = forms.CharField(required=False, label='反馈作业', max_length=200)


class UserForm_check_feedback_homework(forms.Form):  # 查看反馈作业表单
    isright = forms.BooleanField(required=False, label='反馈是否正确')


class UserForm_search_teacher_homework(forms.Form):  # 搜索老师发布作业表单
    search_message = forms.CharField(label='作业相关信息')


@csrf_exempt
def launch_homework(request, num):  # 发布作业
    if request.method == 'POST':
        userform = UserForm_launch_homework(request.POST)
        if userform.is_valid():
            homework_content = userform.cleaned_data['homework_content']
            deadline_days = userform.cleaned_data['deadline_days']

            teacher = Teacher.objects.get(pk=num)
            user = User.objects.get(email=teacher.semail)
            teacher_gradeList = Teacher_grade.objects.filter(teacher_id=teacher.pk)

            create_time = timezone.now()
            create_time = datetime.strptime(create_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            homework_deadline = create_time + timedelta(days=deadline_days)
            homework_deadline = datetime.strptime(homework_deadline.strftime("%Y-%m-%d %H:%M:%S"),
                                                  "%Y-%m-%d %H:%M:%S")

            ht = Teacher_homework.objects.create(teacher_id=num, homework_content=homework_content,
                                                 homework_create_time=create_time, homework_deadline=homework_deadline)
            ht.save()

            for teacher_grade in teacher_gradeList:
                studentList = Student.objects.filter(sgrade=teacher_grade.grade)

                for student in studentList:
                    homework = Homework.objects.create(homework_create_time=create_time,
                                                       teacher_name=teacher.sname,
                                                       student_name=student.sname,
                                                       student_id=student.pk,
                                                       homework_content=homework_content,
                                                       homework_deadline=homework_deadline,
                                                       teacher_id=teacher.pk,
                                                       homework_id=ht.pk)
                    homework.save()
                    homework1 = Homework1.objects.create(student_id=student.pk, teacher_id=teacher.pk,
                                                         homework_id=ht.pk, homework_content=homework_content)

                    homework1.save()

                    notice_content = "作业显示" + homework_content
                    notice_student = Notice_student.objects.create(notice_create_time=create_time,
                                                                   teacher_email=user.email,
                                                                   student_id=student.pk,
                                                                   notice_content=notice_content)
                    notice_student.save()

            return HttpResponse('成功发布作业！')
    else:
        userform = UserForm_launch_homework()
    return render_to_response('myApp/firstWeek/launch_homework.html', {'userform': userform, 'teacher_id': num})


@csrf_exempt
def teacher_alter_homework(request, num):  # 修改已发布的主观题

    if request.method == 'POST':
        userform = UserForm_alter_homework(request.POST)
        if userform.is_valid():
            homework1 = Teacher_homework.objects.get(pk=num)
            homework_content_origin = homework1.homework_content

            homework = Homework.objects.get(homework_content=homework_content_origin)
            homework_content = userform.cleaned_data['homework_content']
            deadline_days = userform.cleaned_data['deadline_days']

            create_time = homework.homework_create_time
            create_time = datetime.strptime(create_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            homework_deadline = create_time + timedelta(days=deadline_days)
            homework_deadline = datetime.strptime(homework_deadline.strftime("%Y-%m-%d %H:%M:%S"),
                                                  "%Y-%m-%d %H:%M:%S")

            Homework.objects.filter(homework_content=homework_content_origin).update(homework_content=homework_content,
                                                                                     homework_deadline=homework_deadline)
            Teacher_homework.objects.filter(homework_content=homework_content_origin).update(
                homework_content=homework_content)

            return HttpResponse('成功修改主观题内容！')
    else:
        userform = UserForm_alter_homework()
    return render_to_response('myApp/secondWeek/alter_shomework.html', {'userform': userform})


def check_student_finished_homework_html2(request, num):  # 学生查看已提交作业html2

    student = Student.objects.get(id=num)
    teacher_gradeList = Teacher_grade.objects.filter(grade=student.sgrade)
    teacherList = []
    for teacher_grade in teacher_gradeList:
        teacher = Teacher.objects.filter(id=teacher_grade.teacher_id)
        teacherList = chain(teacherList, teacher)

    pindex = 1

    return render_to_response('myApp/firstWeek/student_paging_finished_html2.html',
                              {'teacherList': teacherList, 'studentId': student.id, 'pindex': pindex})


def check_student_finished_homework_html3_handInTime(request, num1, num2, pindex):  # 学生查看已提交作业html3（默认提交日期排序）

    homeworkList = Homework.objects.filter(student_id=num1, teacher_id=num2, isComplete=True).order_by('-id')
    homework1List = Homework1.objects.filter(student_id=num1, teacher_id=num2, isComplete=True).order_by('-id')
    homeworkList_sorted_by_handInTime = Homework.objects.filter(student_id=num1, teacher_id=num2,
                                                                isComplete=True).order_by('-handIn_time')
    homework1List_sorted_by_handInTime = Homework1.objects.filter(student_id=num1, teacher_id=num2,
                                                                  isComplete=True).order_by('-handIn_time')

    paginator = Paginator(homeworkList_sorted_by_handInTime, 3)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/student_paging_finished_html3.html',
                              {'homeworkList': homeworkList, 'homework1List': homework1List, 'student_id': num1,
                               'homeworkList_sorted_by_handInTime': homeworkList_sorted_by_handInTime,
                               'homework1List_sorted_by_handInTime': homework1List_sorted_by_handInTime,
                               'teacher_id': num2, "page": page})


def check_student_finished_homework_html3_createtime(request, num1, num2, pindex):  # 学生查看已提交作业html3（改为发布日期排序）

    homeworkList = Homework.objects.filter(student_id=num1, teacher_id=num2, isComplete=True).order_by('-id')
    homework1List = Homework1.objects.filter(student_id=num1, teacher_id=num2, isComplete=True).order_by('-id')
    homeworkList_sorted_by_handInTime = Homework.objects.filter(student_id=num1, teacher_id=num2,
                                                                isComplete=True).order_by('-handIn_time')
    homework1List_sorted_by_handInTime = Homework1.objects.filter(student_id=num1, teacher_id=num2,
                                                                  isComplete=True).order_by('-handIn_time')

    paginator = Paginator(homeworkList, 3)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/student_paging_finished_html3_sorted_by_createtime.html',
                              {'homeworkList': homeworkList, 'homework1List': homework1List, 'student_id': num1,
                               'homeworkList_sorted_by_handInTime': homeworkList_sorted_by_handInTime,
                               'homework1List_sorted_by_handInTime': homework1List_sorted_by_handInTime,
                               'teacher_id': num2, "page": page})


def check_student_unfinished_homework_html2(request, num):  # 学生查看未提交作业html2

    student = Student.objects.get(id=num)
    teacher_gradeList = Teacher_grade.objects.filter(grade=student.sgrade)
    teacherList = []
    for teacher_grade in teacher_gradeList:
        teacher = Teacher.objects.filter(id=teacher_grade.teacher_id)
        teacherList = chain(teacherList, teacher)

    pindex = 1

    return render_to_response('myApp/firstWeek/student_paging_unfinished_html2.html',
                              {'teacherList': teacherList, 'studentId': student.id, 'pindex': pindex})


def check_student_unfinished_homework_html3_sorted_by_deadline(request, num1, num2, pindex):  # 学生查看未提交作业html3（默认截止日期排序）
    homeworkList = Homework.objects.filter(student_id=num1, teacher_id=num2, isComplete=False).order_by('-id')
    homeworkList_sorted_by_ddl = Homework.objects.filter(student_id=num1, teacher_id=num2, isComplete=False).order_by(
        '-homework_deadline')
    paginator = Paginator(homeworkList_sorted_by_ddl, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/student_paging_unfinished_html3.html',
                              {'homeworkList': homeworkList, 'student_id': num1, 'teacher_id': num2, "page": page,
                               "homeworkList_sorted_by_ddl": homeworkList_sorted_by_ddl})


def check_student_unfinished_homework_html3_sorted_by_createtime(request, num1, num2,
                                                                 pindex):  # 学生查看未提交作业html3（改为发布日期排序）
    homeworkList = Homework.objects.filter(student_id=num1, teacher_id=num2, isComplete=False).order_by('-id')
    homeworkList_sorted_by_ddl = Homework.objects.filter(student_id=num1, teacher_id=num2, isComplete=False).order_by(
        '-homework_deadline')
    paginator = Paginator(homeworkList, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/student_paging_unfinished_html3_sorted_by_createtime.html',
                              {'homeworkList': homeworkList, 'student_id': num1, 'teacher_id': num2, "page": page,
                               "homeworkList_sorted_by_ddl": homeworkList_sorted_by_ddl})


@csrf_exempt
def submit_student_homework(request, num):  # 学生提交作业
    if request.method == 'POST':
        userform = UserForm_submit_homework(request.POST or None, request.FILES or None)
        if userform.is_valid():
            myFile = request.FILES.get("handIn_homework")
            if not myFile:
                return HttpResponse("没有文件对应上传")

            homework = Homework.objects.get(pk=num)

            handIn_time = timezone.now()
            handIn_time = datetime.strptime(handIn_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

            deadline = homework.homework_deadline
            deadline = datetime.strptime(deadline.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            isLate = handIn_time > deadline

            Homework.objects.filter(pk=num).update(isLate=isLate, handIn_time=handIn_time,
                                                   handIn_homework=myFile, isComplete=True)
            Homework1.objects.filter(pk=num).update(isComplete=True)

            destination = open(os.path.join("./static/media", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            return HttpResponse('成功提交作业！')
    else:
        userform = UserForm_submit_homework()
    return render_to_response('myApp/firstWeek/submit_student_homework.html', {'userform': userform})


@csrf_exempt
def check_teacher_homework(request, num, pindex):  # 老师查看作业
    homeworkList_search = Teacher_homework.objects.filter(teacher_id=num).order_by('-id')
    searchList = []
    flag = False
    if request.method == 'POST':
        userform = UserForm_search_teacher_homework(request.POST)
        if userform.is_valid():
            search_message = userform.cleaned_data['search_message']
            for homework in homeworkList_search:
                if search_message in str(homework.homework_create_time):
                    flag = True
                if search_message in homework.homework_content:
                    flag = True
                if search_message in str(homework.homework_deadline):
                    flag = True
                if search_message in str(homework.pk):
                    flag = True
                homeworkList_tmp = Teacher_homework.objects.filter(id=homework.pk)

                if flag is True:
                    searchList = chain(searchList, homeworkList_tmp)

    else:
        userform = UserForm_search_teacher_homework()

    homeworkList = Teacher_homework.objects.filter(teacher_id=num).order_by('-id')
    paginator = Paginator(homeworkList, 5)
    if pindex == "":
        pindex = 1
    else:
        int(pindex)
    pindex1 = 1
    page = paginator.page(pindex)

    return render_to_response('myApp/firstWeek/check_teacher_homework.html', {'pindex0': pindex, 'homeworkList': homeworkList,
                                                                              'searchList': searchList,
                                                                              'flag': flag,
                                                                              'teacher_id': num, "page": page,
                                                                              'pindex1': pindex1, 'userform': userform})


def delete_teacher_homework(request, num):  # 教师删除对应作业

    thomework = Teacher_homework.objects.get(id=num)
    homeworkList = Homework.objects.filter(homework_content=thomework.homework_content)
    homeworkList1 = Homework1.objects.filter(homework_content=thomework.homework_content)
    thomework.delete()

    for homework in homeworkList:
        homework.delete()

    for homework1 in homeworkList1:
        homework1.delete()

    return render_to_response('myApp/secondWeek/teacher_delete_shomework.html')


def check_submission_homework(request, num, pindex):  # 老师查看作业提交情况

    studentnamelist = Homework.objects.filter(homework_id=num).order_by('-id')
    homework1List = Homework1.objects.all()
    paginator = Paginator(studentnamelist, 1)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/check_submission_homework.html', {'studentnamelist': studentnamelist,
                                                                                 'homework_id': num, "page": page,
                                                                                 'homework1List': homework1List})


def check_common_student_the_homework(request, num, pindex):  # 老师查看正确或订正正确且未迟交的学生名单

    studentnamelist = Homework.objects.filter(homework_id=num).order_by('-id')
    homework1List = Homework1.objects.all()
    paginator = Paginator(studentnamelist, 1)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/check_common_student_the_homework.html',
                              {'studentnamelist': studentnamelist,
                               'homework_id': num, "page": page,
                               'homework1List': homework1List})


@csrf_exempt
def correct_homework(request, num):  # 老师批改作业
    s_homework = Homework.objects.get(pk=num)
    if s_homework.isComplete == False:
        return HttpResponse('这位学生还未完成作业哟！')

    else:
        file_name = s_homework.handIn_homework
        if request.method == 'POST':
            userform = UserForm_correct_homework(request.POST)
            if userform.is_valid():
                teacher_comment = userform.cleaned_data['teacher_comment']
                isCorrect = userform.cleaned_data['isCorrect']

                if teacher_comment == "":
                    return HttpResponse('您未添加评论！')

                else:
                    Homework1.objects.filter(pk=num).update(tcomment=teacher_comment, iscorrect=isCorrect,
                                                            iscommented=True)
                    return HttpResponse('成功添加评论！')

        else:
            userform = UserForm_correct_homework()
        return render_to_response('myApp/firstWeek/correct_homework.html',
                                  {'file_name': file_name, 'userform': userform})


@csrf_exempt
def feedback_homework(request, num1, num2, num3):  # 学生反馈作业
    if request.method == 'POST':
        userform = UserForm_feedback_homework(request.POST or None, request.FILES or None)
        if userform.is_valid():

            myFile = request.FILES.get("feedback_homework")
            if not myFile:
                return HttpResponse("没有文件对应上传")

            feedback_comment = userform.cleaned_data['feedback_comment']

            isfeedback = False

            if feedback_comment != "":
                isfeedback = True

            Homework1.objects.filter(pk=num3, student_id=num1, teacher_id=num2).update(
                feedback_homework=myFile, feedback_comment=feedback_comment, isfeedback=isfeedback)

            destination = open(os.path.join("./static/media", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            return HttpResponse('成功反馈作业！')
    else:
        userform = UserForm_feedback_homework()
    return render_to_response('myApp/firstWeek/feedback_student_finishedhomework_html3.html', {'userform': userform})


def check_feedback_homework(request, num, pindex):  # 老师查看反馈作业
    studentnamelist = Homework1.objects.filter(homework_id=num).order_by('-id')
    studentList = Student.objects.all().order_by('-id')
    paginator = Paginator(studentnamelist, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/check_feedback_homework.html', {'studentnamelist': studentnamelist,
                                                                               'homework_id': num,
                                                                               'studentList': studentList,
                                                                               "page": page})  # 'file_url':studentnamelist.feedback_homework.url})


def check_redo_homework(request, num, pindex):  # 老师查看未订正学生名单
    studentnamelist = Homework1.objects.filter(homework_id=num).order_by('-id')
    studentList = Student.objects.all().order_by('-id')
    paginator = Paginator(studentnamelist, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/check_redo_homework.html', {'studentnamelist': studentnamelist,
                                                                           'homework_id': num,
                                                                           'studentList': studentList,
                                                                           "page": page})  # 'file_url':studentnamelist.feedback_homework.url})


def check_not_submitted_homework(request, num, pindex):  # 老师查看未提交学生名单
    studentnamelist = Homework.objects.filter(homework_id=num).order_by('-id')
    studentList = Student.objects.all().order_by('-id')
    paginator = Paginator(studentnamelist, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/firstWeek/check_not_submitted_homework.html', {'studentnamelist': studentnamelist,
                                                                                    'homework_id': num,
                                                                                    'studentList': studentList,
                                                                                    "page": page})  # 'file_url':studentnamelist.feedback_homework.url})


@csrf_exempt
def correct_feedback_homework(request, num1):  # 老师批改学生反馈内容
    homework1 = Homework1.objects.filter(pk=num1).first()
    file_name = homework1.feedback_homework
    if request.method == 'POST':
        userform = UserForm_check_feedback_homework(request.POST or None, request.FILES or None)
        if userform.is_valid():
            isright = userform.cleaned_data['isright']

            if homework1.iscorrect:
                homework1.iscorrect = homework1.iscorrect
            else:
                homework1.iscorrect = homework1.isright

            Homework1.objects.filter(pk=num1).update(isright=isright, iscorrect=homework1.iscorrect)

            return HttpResponse('成功批改反馈作业！')
    else:
        userform = UserForm_check_feedback_homework()
    return render_to_response('myApp/firstWeek/correct_feedback_homework.html',
                              {'file_name': file_name, 'userform': userform,
                               'feedback_comment': homework1.feedback_comment})


def download(request, file_name):  # 下载作业
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
    file_path = os.path.join(base_dir, 'static', 'media', file_name)  # 下载文件的绝对路径

    if not os.path.isfile(file_path):  # 判断下载文件是否存在
        return HttpResponse("Sorry but Not Found the File")

    def file_iterator(file_name, chunk_size=512):
        print(file_name)
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        the_file_name = './static/media/' + file_name
        print(the_file_name)
        response = StreamingHttpResponse(file_iterator(the_file_name))

        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))

    except:
        return HttpResponse("Sorry but Not Found the File")
    return response
