# 模型的定义，在这里定义的模型类可以通过迁移同步到Mysql，每个模型类对应Mysql中的一张表
from __future__ import unicode_literals
from django.db import models


class User(models.Model):  # 用户类定义
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.BooleanField(default=True)
    age = models.IntegerField()
    grade = models.CharField(max_length=20)
    isTeacher = models.CharField(max_length=50)  # 老师密钥


class Student(models.Model):  # 学生类定义
    sname = models.CharField(max_length=20)  # 姓名
    sgender = models.BooleanField(default=True)  # 性别
    sage = models.IntegerField()  # 年龄
    isDelete = models.BooleanField(default=False)  # 是否删除
    sgrade = models.CharField(max_length=20)  # 班级
    semail = models.EmailField()  # 学生email（修改1）

    def __str__(self):  # 显示学生时显示其姓名
        return self.sname


class Teacher(models.Model):  # 老师类定义同上
    sname = models.CharField(max_length=20)
    sgender = models.BooleanField(default=True)
    sage = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    semail = models.EmailField()  # 老师email（修改2）

    def __str__(self):
        return self.sname


class Teacher_grade(models.Model):  # 老师-班级，教授关系类
    teacher_id = models.IntegerField()
    teacher_name = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)


class Homework(models.Model):  # 作业类
    homework_create_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    teacher_name = models.CharField(max_length=20)
    student_name = models.CharField(max_length=20)
    student_id = models.IntegerField()
    teacher_id = models.IntegerField()
    homework_id = models.IntegerField()
    homework_content = models.CharField(max_length=50)
    homework_deadline = models.DateTimeField(max_length=20)
    handIn_homework = models.FileField(null=True, upload_to='avatar')
    handIn_time = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    isLate = models.BooleanField(default=False)
    isComplete = models.BooleanField(default=False)


class Notice_student(models.Model):  # 学生通知类
    notice_create_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    teacher_email = models.EmailField()
    student_id = models.IntegerField()
    notice_content = models.CharField(max_length=50)


class Teacher_homework(models.Model):  # 老师作业类
    teacher_id = models.IntegerField()
    homework_content = models.CharField(max_length=50, default='1')
    homework_deadline = models.DateTimeField(max_length=20)
    homework_create_time = models.DateTimeField(auto_now=False, auto_now_add=False)


class Homework1(models.Model):  # 为避免上面的Homework类冗余数据过多，新建一个作业类，与上面的Homework类一一对应
    student_id = models.IntegerField()
    teacher_id = models.IntegerField()
    homework_id = models.IntegerField()
    iscorrect = models.NullBooleanField()
    tcomment = models.CharField(max_length=200, default='待评论！')
    iscommented = models.BooleanField(default=False)
    isComplete = models.BooleanField(default=False)
    feedback_homework = models.FileField(null=True, upload_to='media')
    feedback_comment = models.CharField(max_length=200, default='待评论！')
    isright = models.BooleanField(default=False)
    isfeedback = models.BooleanField(default=False)
    homework_content = models.CharField(max_length=50, default='1')


class objective_item(models.Model):  # 客观题
    student_id = models.IntegerField()
    teacher_id = models.IntegerField()
    teacher_name = models.CharField(max_length=20)
    student_name = models.CharField(max_length=20)
    item_content = models.CharField(max_length=200)  # 题目具体内容（后期可修改为文件）
    item_num = models.IntegerField()  # 题目个数
    answer = models.CharField(max_length=200)  # 标准答案
    student_answer = models.CharField(null=True, max_length=200)
    isComplete = models.BooleanField(default=False)
    homework_create_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    homework_deadline = models.DateTimeField(max_length=20)
    item_id = models.IntegerField(null=True)
    handIn_time = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    isLate = models.BooleanField(default=False)
    accuracy = models.FloatField(null=True)


class objective_id(models.Model):  # 每道客观题和老师
    teacher_id = models.IntegerField()
    homework_create_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    homework_deadline = models.DateTimeField(max_length=20)
    item_content = models.CharField(max_length=200)
    mean = models.FloatField(null=True)
