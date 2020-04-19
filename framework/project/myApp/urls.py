#myApp里面的urls路由配置
from django.conf.urls import url,include
from django.contrib import admin
from . import views, view_firstWeek

from django.urls import path
from . import  views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index), #仅主页直接转到views中的index函数

    url(r'^regist/$',views.regist),  #regist需求转至views中的regist函数,下同
    url(r'^login/$',views.login),
    url(r'^index/$',views.index),
    url(r'^login/(\d+)$',views.check_teacher_info),
    url(r'^login/0/(\d+)$',views.alter_teacher_info),
    url(r'^login/1/(\d+)$',views.check_student_info),
    url(r'^login/2/(\d+)$',views.alter_student_info),
    url(r'^login/3/(\d+)$',views.add_teacher_grade),
    url(r'^login/4/(\d+)$',views.delete_teacher_grade),   #preparation的模板及views的视图

    url(r'^login/5/(\d+)$',view_firstWeek.launch_homework),
    #firstWeek的模板及view_firstWeek的视图


    url(r'^login/6/(\d+)$',view_firstWeek.check_student_homework),  #查看作业

    url(r'^login/7/(\d+)$',view_firstWeek.submit_student_homework) #提交作业

]