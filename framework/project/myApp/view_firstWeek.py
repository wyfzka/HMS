from datetime import datetime
from datetime import timedelta
from django.shortcuts import render, render_to_response
from django import forms
from .models import User, Teacher, Student, Teacher_grade, Homework, Notice_student
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


class UserForm_launch_homework(forms.Form):  # 发布作业信息表单
    homework_content = forms.CharField(label='作业内容', max_length=50)
    deadline_days = forms.IntegerField(label='截止日期为多少天后')


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

            for teacher_grade in teacher_gradeList:
                studentList = Student.objects.filter(sgrade=teacher_grade.grade)
                create_time = timezone.now()
                create_time = datetime.strptime(create_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                homework_deadline = create_time + timedelta(days=deadline_days)
                homework_deadline = datetime.strptime(homework_deadline.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

                for student in studentList:
                    homework = Homework.objects.create(homework_create_time=create_time,
                                                       teacher_email=user.email,
                                                       student_id=student.pk,
                                                       homework_content=homework_content,
                                                       homework_deadline=homework_deadline)
                    homework.save()

                    notice_content = "作业发布：" + homework_content
                    notice_student = Notice_student.objects.create(notice_create_time=create_time,
                                                                   teacher_email=user.email,
                                                                   student_id=student.pk,
                                                                   notice_content=notice_content)
                    notice_student.save()

            return HttpResponse('成功发布作业！')
    else:
        userform = UserForm_launch_homework()
    return render_to_response('myApp/firstWeek/launch_homework.html', {'userform': userform})
