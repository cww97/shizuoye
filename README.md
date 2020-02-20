
# 拾作业

## feature

- 老师可以定义文件名，避免学生自己上传的文件名混乱
- 学生之间无法看见其他人的作业

## Class

用户：账号、姓名、密码；学校；学号/工号

- User(default stu) - SubClass(teacher)
- 课程Course(joiners) - 作业Assignment() - 提交Submit

一个课程对应多个作业，每人对于每次作业允许有一个submission(与oj系统不同)，
就是在提交作业的时候，如果该用户对于该assignment的submission已经存在则update, else create
提交完后跳转至submit_detail页面，状态更新为 submitted

## 功能

注册登录

### 老师端 

- 发布课程与作业(支持编辑)，导入带编号的学生list，生成邀请码，有ddl
- 一键下载一次作页所有学生交上来的pdf(后台可以 "%s..." 来定义文件名)
- pdf用手写笔批注后（这个part老师先自己搞定，web pdf editor后续工程）
- 老师再再打包上传，(默认文件名"xxx_feedback.pdf"，也可"%s...")，学生的submit更新judge status
- 作业打分的功能以后再做（预留接口），还有后续统计，目前ranklist先做成统计学生是否提交的表

### 学生端

- 找到对应的课程并加入（使用老师提供的邀请码）
- 点进去每次的作业提交
- 待老师批完后下载feedback pdf

## rua

其实教师/学生可以不加区分，也就是任何人都可以发布作业并批改，只是扮演角色不一样。
这么说我只是没想好如何快捷的教师资格验证，or 默认学生然后注册后在个人中心注册老师权限？

## 按照优先级future work

- 域名备案
- 短信注册
- 一个是密码错了不会给提示
- pdf加载 验证
- fork course, assignment
- django-hashid-field
- id 从BIGN开始

## 头像：

- 更新头像后 from django.contrib.auth import login
- 手动写CACHE函数(user)
- login
