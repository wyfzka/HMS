

from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from .models import  Student, User, Teacher


class StudentsInfo(admin.TabularInline):
    model = Student
    extra = 2

class StudentAdmin(admin.ModelAdmin):
    def gender(self):
        if self.sgender:
            return "男"
        else:
            return "女"
    gender.short_description = "性别"
    list_display = ['pk','sname','sage',gender,'sgrade','isDelete']
    list_per_page = 10

    actions_on_bottom = True
    actions_on_top = False
admin.site.register(Student,StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    def gender(self):
        if self.sgender:
            return "男"
        else:
            return "女"
    gender.short_description = "性别"
    list_display = ['pk','sname','sage',gender,'sgrade','isDelete']
    list_per_page = 10

    actions_on_bottom = True
    actions_on_top = False
admin.site.register(Teacher,TeacherAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','email')

admin.site.register(User,UserAdmin)