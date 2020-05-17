from datetime import datetime
from datetime import timedelta
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response
from django import forms
from .models import User, Teacher, Student, Teacher_grade, Homework, Notice_student, Teacher_homework, Homework1, \
    objective_item, objective_id
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from itertools import chain


class UserForm_launch_objective_item(forms.Form):  # 发布客观题表单
    item_content = forms.CharField(label='作业内容', max_length=200)
    item_num = forms.IntegerField(label='题目个数')  # 可用统计字符串长度代替
    answer = forms.CharField(label='标准答案', max_length=200)
    deadline_days = forms.IntegerField(label='截止日期为多少天后')


class UserForm_submit_objective_item(forms.Form):  # 提交客观题表单
    student_answer = forms.CharField(label='提交客观题答案')


class UserForm_search_teacher_objective(forms.Form):  # 搜索老师发布客观题表单
    search_message = forms.CharField(label='客观题相关信息')


@csrf_exempt
def launch_objective_item(request, num):  # 发布作业
    if request.method == 'POST':
        userform = UserForm_launch_objective_item(request.POST)
        if userform.is_valid():
            item_content = userform.cleaned_data['item_content']
            item_num = userform.cleaned_data['item_num']
            answer = userform.cleaned_data['answer']
            deadline_days = userform.cleaned_data['deadline_days']

            teacher = Teacher.objects.get(pk=num)
            # user = User.objects.get(email=teacher.semail)
            teacher_gradeList = Teacher_grade.objects.filter(teacher_id=teacher.pk)

            create_time = timezone.now()
            create_time = datetime.strptime(create_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            homework_deadline = create_time + timedelta(days=deadline_days)
            homework_deadline = datetime.strptime(homework_deadline.strftime("%Y-%m-%d %H:%M:%S"),
                                                  "%Y-%m-%d %H:%M:%S")

            item_t = objective_id.objects.create(teacher_id=num, homework_create_time=create_time,
                                                 homework_deadline=homework_deadline,
                                                 item_content=item_content)
            item_t.save()

            for teacher_grade in teacher_gradeList:
                studentList = Student.objects.filter(sgrade=teacher_grade.grade)

                for student in studentList:
                    item = objective_item.objects.create(homework_create_time=create_time,
                                                         teacher_name=teacher.sname,
                                                         student_name=student.sname,
                                                         student_id=student.pk,
                                                         item_num=item_num,
                                                         answer=answer,
                                                         item_content=item_content,
                                                         homework_deadline=homework_deadline,
                                                         teacher_id=teacher.pk,
                                                         item_id=item_t.pk,
                                                         )
                    item.save()

            return HttpResponse('成功发布客观题作业！')
    else:
        userform = UserForm_launch_objective_item()
    return render_to_response('myApp/secondWeek/launch_objective_item.html', {'userform': userform, 'teacher_id': num})


@csrf_exempt
def teacher_check_objective_item(request, num, pindex):  # 老师查看客观题
    homeworkList_search = objective_id.objects.filter(teacher_id=num).order_by('-id')
    searchList = []
    flag = False
    if request.method == 'POST':
        userform = UserForm_search_teacher_objective(request.POST)
        if userform.is_valid():
            search_message = userform.cleaned_data['search_message']
            for homework in homeworkList_search:
                if search_message in str(homework.homework_create_time):
                    flag = True
                if search_message in homework.item_content:
                    flag = True
                if search_message in str(homework.homework_deadline):
                    flag = True
                if search_message in str(homework.pk):
                    flag = True
                homeworkList_tmp = objective_id.objects.filter(id=homework.pk)

                if flag is True:
                    searchList = chain(searchList, homeworkList_tmp)

    else:
        userform = UserForm_search_teacher_objective()

    homeworkList = objective_id.objects.filter(teacher_id=num).order_by('-id')
    objectList = objective_item.objects.all()
    paginator = Paginator(homeworkList, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)

    pindex1 = 1

    for homework in homeworkList:
        sum0 = 0.0
        i = 0
        for object0 in objectList:
            if object0.accuracy is not None and object0.item_content == homework.item_content:
                sum0 += object0.accuracy
                i = i + 1
                if i is 0:
                    mean = -1
                else:
                    mean = sum0 / i
                objective_id.objects.filter(pk=homework.pk).update(mean=mean)

    homeworkList = objective_id.objects.filter(teacher_id=num).order_by('-id')

    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/teacher_check_objective_item.html', {'homeworkList': homeworkList,
                                                                                     'searchList': searchList,
                                                                                     'flag': flag,
                                                                                     'userform': userform,
                                                                                     'teacher_id': num,
                                                                                     "page": page,
                                                                                     'pindex1': pindex1})


def teacher_check_student_submission(request, num, pindex):  # 老师查看学生提交情况
    studentList = objective_item.objects.filter(item_id=num).order_by('-id')
    paginator = Paginator(studentList, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/teacher_check_student_submission.html',
                              {'studentList': studentList, "page": page, 'item_id': num})


def teacher_check_not_submitted_objective(request, num, pindex):  # 老师查看客观题未提交或迟交学生名单
    objectiveList = objective_item.objects.filter(item_id=num).order_by('-id')
    studentList = Student.objects.all().order_by('-id')
    paginator = Paginator(objectiveList, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/teacher_check_not_submitted_objective.html',
                              {'objectiveList': objectiveList, "page": page, 'item_id': num, 'studentList': studentList})


@csrf_exempt
def submit_objective_item(request, num):  # 学生提交客观题作业
    if request.method == 'POST':
        userform = UserForm_submit_objective_item(request.POST)
        if userform.is_valid():
            student_answer = userform.cleaned_data['student_answer']

            objective = objective_item.objects.get(pk=num)

            handIn_time = timezone.now()
            handIn_time = datetime.strptime(handIn_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

            deadline = objective.homework_deadline
            deadline = datetime.strptime(deadline.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            isLate = handIn_time > deadline

            student_real_answer_calc1 = ''.join([x for x in student_answer if x.isalpha()])
            real_answer_calc1 = ''.join([x for x in objective.answer if x.isalpha()])
            student_real_answer_calc = student_real_answer_calc1.lower()
            real_answer_calc = real_answer_calc1.lower()

            calc = 0
            for j in range(len(real_answer_calc)):
                if real_answer_calc[j] == student_real_answer_calc[j]:
                    calc = calc + 1
                j = j + 1

            accuracy = calc / len(real_answer_calc)

            objective_item.objects.filter(pk=num).update(student_answer=student_answer, isComplete=True,
                                                         isLate=isLate, handIn_time=handIn_time, accuracy=accuracy)

            return HttpResponse('成功提交客观题作业！查询成绩请前往查看已提交作业~')
    else:
        userform = UserForm_submit_objective_item()
    return render_to_response('myApp/secondWeek/submit_objective_item.html', {'userform': userform})


def check_unfinished_objective_item_html2(request, num):  # 学生查看待提交客观题html2

    student = Student.objects.get(id=num)
    teacher_gradeList = Teacher_grade.objects.filter(grade=student.sgrade)
    teacherList = []
    for teacher_grade in teacher_gradeList:
        teacher = Teacher.objects.filter(id=teacher_grade.teacher_id)
        teacherList = chain(teacherList, teacher)

    pindex = 1

    return render_to_response('myApp/secondWeek/check_unfinished_objective_item.html',
                              {'teacherList': teacherList, 'studentId': student.id, 'pindex': pindex})


def check_unfinished_objective_item_html3_sorted_by_deadline(request, num1, num2, pindex):  # 学生查看未提交作业html3（默认截止日期排序）
    objectiveList = objective_item.objects.filter(student_id=num1, teacher_id=num2, isComplete=False).order_by('-id')
    objectiveList_sorted_by_ddl = objective_item.objects.filter(student_id=num1, teacher_id=num2,
                                                                isComplete=False).order_by(
        '-homework_deadline')
    paginator = Paginator(objectiveList_sorted_by_ddl, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/check_unfinished_objective_item_html3.html',
                              {'objectiveList': objectiveList, 'student_id': num1, 'teacher_id': num2, "page": page,
                               "objectiveList_sorted_by_ddl": objectiveList_sorted_by_ddl})


def check_unfinished_objective_item_html3_sorted_by_createtime(request, num1, num2, pindex):  # 学生查看未提交作业html3（改为发布日期排序）
    objectiveList = objective_item.objects.filter(student_id=num1, teacher_id=num2, isComplete=False).order_by('-id')
    objectiveList_sorted_by_ddl = objective_item.objects.filter(student_id=num1, teacher_id=num2,
                                                                isComplete=False).order_by(
        '-homework_deadline')
    paginator = Paginator(objectiveList_sorted_by_ddl, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/check_unfinished_objective_item_html3_sorted_by_createtime.html',
                              {'objectiveList': objectiveList, 'student_id': num1, 'teacher_id': num2, "page": page,
                               "objectiveList_sorted_by_ddl": objectiveList_sorted_by_ddl})


def check_finished_objective_item_html2(request, num):  # 学生查看已提交客观题html2
    student = Student.objects.get(id=num)
    teacher_gradeList = Teacher_grade.objects.filter(grade=student.sgrade)
    teacherList = []
    for teacher_grade in teacher_gradeList:
        teacher = Teacher.objects.filter(id=teacher_grade.teacher_id)
        teacherList = chain(teacherList, teacher)

    pindex = 1

    return render_to_response('myApp/secondWeek/check_finished_objective_item.html',
                              {'teacherList': teacherList, 'studentId': student.id, 'pindex': pindex})


def check_finished_objective_item_html3_handInTime(request, num1, num2, pindex):  # 学生查看已提交客观题html3（默认提交日期排序）

    objectiveList = objective_item.objects.filter(student_id=num1, teacher_id=num2, isComplete=True).order_by('-id')
    objectiveList_sorted_by_handInTime = objective_item.objects.filter(student_id=num1, teacher_id=num2,
                                                                       isComplete=True).order_by(
        '-handIn_time')
    paginator = Paginator(objectiveList_sorted_by_handInTime, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/check_finished_objective_item_html3.html',
                              {'objectiveList': objectiveList, 'student_id': num1,
                               'objectiveList_sorted_by_handInTime': objectiveList_sorted_by_handInTime,
                               'teacher_id': num2, "page": page})


def check_finished_objective_item_html3_createtime(request, num1, num2, pindex):  # 学生查看已提交客观题html3（改为发布日期排序）

    objectiveList = objective_item.objects.filter(student_id=num1, teacher_id=num2, isComplete=True).order_by('-id')
    objectiveList_sorted_by_handInTime = objective_item.objects.filter(student_id=num1, teacher_id=num2,
                                                                       isComplete=True).order_by(
        '-handIn_time')
    paginator = Paginator(objectiveList_sorted_by_handInTime, 5)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    return render_to_response('myApp/secondWeek/check_finished_objective_item_html3_sorted_by_createtime.html',
                              {'objectiveList': objectiveList, 'student_id': num1,
                               'objectiveList_sorted_by_handInTime': objectiveList_sorted_by_handInTime,
                               'teacher_id': num2, "page": page})
