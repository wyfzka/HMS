# myApp里面的urls路由配置
from django.conf.urls import url, include
from django.contrib import admin
from . import view_firstWeek, view_secondWeek
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),  # 仅主页直接转到views中的index函数

    url(r'^regist/$', views.regist),  # regist需求转至views中的regist函数,下同
    url(r'^login/$', views.login),
    url(r'^index/$', views.index),
    url(r'^login/(\d+)$', views.check_teacher_info),
    url(r'^login/0/(\d+)$', views.alter_teacher_info),
    url(r'^login/1/(\d+)$', views.check_student_info),
    url(r'^login/2/(\d+)$', views.alter_student_info),
    url(r'^login/3/(\d+)$', views.add_teacher_grade),
    url(r'^login/4/(\d+)$', views.delete_teacher_grade),  # preparation的模板及views的视图

    url(r'^login/5/(\d+)$', view_firstWeek.launch_homework),  # firstWeek的模板及view_firstWeek的视图
    url(r'^login/6/(\d+)$', view_firstWeek.check_student_finished_homework_html2),  # 学生查看已提交作业html2
    url(r'^login/7/(\d+)$', view_firstWeek.submit_student_homework),  # 提交作业
    url(r'^login/8/(\d+)/(\d+)$', view_firstWeek.check_teacher_homework),  # 老师查看作业完成情况
    url(r'^login/8/1/1/(\d+)$', view_firstWeek.teacher_alter_homework),  # 老师修改对应作业
    url(r'^login/8/1/2/(\d+)$', view_firstWeek.delete_teacher_homework),  # 老师删除对应作业
    url(r'^login/9/2/(\d+)/(\d+)$', view_firstWeek.check_submission_homework),  # 老师批改学生列表
    url(r'^login/9/2/2/(\d+)/(\d+)$', view_firstWeek.check_common_student_the_homework),  # 老师查看正确或订正正确且未迟交的学生名单
    url(r'^login/9/(\d+)/(\d+)$', view_firstWeek.check_feedback_homework),  # 老师查看反馈学生列表
    url(r'^login/9/1/1/(\d+)/(\d+)$', view_firstWeek.check_redo_homework),  # 老师查看未订正学生列表
    url(r'^login/9/1/2/(\d+)/(\d+)$', view_firstWeek.check_not_submitted_homework),  # 老师查看未提交学生列表
    url(r'^login/10/(\d+)$', view_firstWeek.correct_homework),  # 老师批改学生作业
    url(r'^login/10/1/(\d+)$', view_firstWeek.correct_feedback_homework),  # 老师批改反馈内容
    url(r'^login/11/(\d+)$', views.check_gradelist),  # 老师查看所属班级
    url(r'^login/12/(\d+)$', views.check_studentlist),  # 老师查看所属班级学生情况
    url(r'^login/14/(\d+)/(\d+)/(\d+)$', view_firstWeek.check_student_finished_homework_html3_handInTime),  # 学生查看已提交作业html3（默认提交日期排序）
    url(r'^login/14/1/(\d+)/(\d+)/(\d+)$', view_firstWeek.check_student_finished_homework_html3_createtime),  # 学生查看已提交作业html3（改为发布日期排序）
    url(r'^login/13/(\d+)$', view_firstWeek.check_student_unfinished_homework_html2),  # 学生查看未提交作业html2
    url(r'^login/15/(\d+)/(\d+)/(\d+)$', view_firstWeek.check_student_unfinished_homework_html3_sorted_by_deadline),  # 学生查看未提交作业html3（默认截止日期排序）
    url(r'^login/15/1/(\d+)/(\d+)/(\d+)$', view_firstWeek.check_student_unfinished_homework_html3_sorted_by_createtime),  # 学生查看未提交作业html3（改为发布日期排序）
    url(r'^login/14/1/1/(\d+)/(\d+)/(\d+)$', view_firstWeek.feedback_homework),  # 学生反馈作业

    url(r'^login/16/(\d+)$', view_secondWeek.launch_objective_item),  # 发布客观题
    url(r'^login/17/(\d+)/(\d+)$', view_secondWeek.teacher_check_objective_item),  # 老师查看客观题
    url(r'^login/18/(\d+)/(\d+)$', view_secondWeek.teacher_check_student_submission),  # 老师查看学生客观题提交情况
    url(r'^login/18/1/(\d+)/(\d+)$', view_secondWeek.teacher_check_not_submitted_objective),  # 老师查看客观题未提交或迟交学生名单
    url(r'^login/19/(\d+)$', view_secondWeek.check_unfinished_objective_item_html2),  # 学生查看未提交客观题html2
    url(r'^login/20/(\d+)$', view_secondWeek.submit_objective_item),  # 学生提交客观题作业
    url(r'^login/21/(\d+)$', view_secondWeek.check_finished_objective_item_html2),  # 学生查看已提交客观题html2
    url(r'^login/22/(\d+)/(\d+)/(\d+)$', view_secondWeek.check_unfinished_objective_item_html3_sorted_by_deadline),  # 学生查看未提交客观题html3（默认截止日期排序）
    url(r'^login/22/1/(\d+)/(\d+)/(\d+)$', view_secondWeek.check_unfinished_objective_item_html3_sorted_by_createtime),  # 学生查看未提交客观题html3（改为发布日期排序）
    url(r'^login/23/(\d+)/(\d+)/(\d+)$', view_secondWeek.check_finished_objective_item_html3_handInTime),  # 学生查看已提交客观题html3（默认提交日期排序）
    url(r'^login/23/1/(\d+)/(\d+)/(\d+)$', view_secondWeek.check_finished_objective_item_html3_createtime),  # 学生查看已提交客观题html3（改为发布日期排序）

    url(r'^login/download/(?P<file_name>.*)/$', view_firstWeek.download),  # 下载作业
]
