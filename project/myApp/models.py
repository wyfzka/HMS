#模型的定义，在这里定义的模型类可以通过迁移同步到Mysql，每个模型类对应Mysql中的一张表
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class Student(models.Model):    #学生类定义
    sname = models.CharField(max_length=20)  #姓名
    sgender = models.BooleanField(default = True)  #性别
    sage = models.IntegerField()  #年龄
    isDelete = models.BooleanField(default = False)  #是否删除
    sgrade = models.IntegerField()  #班级
    semail = models.EmailField()   #学生email（修改1）
    def __str__(self):   #显示学生时显示其姓名
        return self.sname

class Teacher(models.Model):   #老师类定义同上
    sname = models.CharField(max_length=20)
    sgender = models.BooleanField(default=True)
    sage = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    sgrade = models.IntegerField()
    semail = models.EmailField()    #老师email（修改2）
    def __str__(self):
        return self.sname


class User(models.Model):  #用户类定义
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.BooleanField(default=True)
    age = models.IntegerField()
    grade = models.IntegerField()
    isTeacher = models.CharField(max_length=50)   #老师密钥

