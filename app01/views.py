from django.shortcuts import render, redirect, HttpResponse
import pymysql
import json
def classes(request):
    # 去請求的cookie中找憑證
    tk = request.COOKIES.get('ticket')
    if not tk:
        return redirect('/login/')


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select cid,cname from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request, 'classes.html', {'class_list': class_list})

def add_class(request):

    if request.method == 'GET':
        return render(request, 'add_class.html')
    else:
        print(request.POST)
        v = request.POST.get('cname')
        if len(v) > 0 :
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into class(cname) values(%s)", [v,])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes/')
        else:
            return render(request, 'add_class.html', {'msg': '班級名稱不得為空'})

def del_class(request):
    nid = request.GET.get('nid')

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where cid =%s", [nid,])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/classes/')

def edit_class(request):

    if request.method == 'GET':
        nid = request.GET.get('nid')

        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select cid,cname from class where cid =%s", [nid,])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(result)
        return render(request, 'edit_class.html', {'result':result})
    else:
        nid = request.GET.get('nid')
        cname = request.POST.get('cname')

        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set cname=%s where cid=%s", [cname, nid,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')

def students(request):

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("SELECT sid, sname, class_id, cname FROM student LEFT JOIN class ON student.`class_id` = class.`cid`")
    student_list = cursor.fetchall()
    # print(student_list)
    cursor.close()
    conn.close()
    class_list = sqlhelper.get_list('select cid, cname from class', [])
    return render(request, 'students.html', {'student_list': student_list, 'class_list': class_list})

def add_student(request):

    if request.method == 'GET':

        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select cid, cname from class")
        class_list = cursor.fetchall()
        print(class_list)
        cursor.close()
        conn.close()
        return render(request, 'add_student.html', {'class_list': class_list})
    else:
        sname = request.POST.get('sname')
        class_id = request.POST.get('class_id')
        print(sname, class_id)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('insert into student(sname, class_id) values(%s, %s)', [sname, class_id,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students/')

from utils import sqlhelper

def edit_student(request):

    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list = sqlhelper.get_list("select cid, cname from class", [])
        current_student_info = sqlhelper.get_one("select sid, sname, class_id from student where sid = %s ", [nid,])
        return render(request, 'edit_student.html', {'class_list': class_list, 'current_student_info': current_student_info})
    else:
        nid = request.GET.get('nid')
        sname = request.POST.get('sname')
        class_id = request.POST.get('class_id')
        sqlhelper.modify('update student set sname = %s, class_id = %s where sid = %s', [sname, class_id, nid, ])
        return redirect('/students/')

def del_student(request):
    nid = request.GET.get('nid')

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from student where sid =%s", [nid,])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/students/')

def teachers(request):
    teacher_list = sqlhelper.get_list('''
        SELECT teacher.tid, tname, cname FROM teacher LEFT JOIN `teacher2class` ON teacher.`tid` = teacher2class.`tid`
        LEFT JOIN class ON teacher2class.`cid`=class.`cid` 
    ''', [])

    result = {}

    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['cname'].append(row['cname'])
        else:
            result[tid] = {'tid': row['tid'], 'tname': row['tname'], 'cname': [row['cname'], ]}

    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list('select cid, cname from class', [])
    obj.close()

    return render(request, 'teachers.html', {'teacher_list': result.values(), 'class_list': class_list})
#############################對話框#############################
def modal_add_class(request):

    title = request.POST.get('title')
    if len(title) > 0:
        sqlhelper.modify('insert into class(cname) value(%s)', [title, ])
        return HttpResponse('ok')
    else:
        #頁面不要刷新, 提示錯誤信息

        return HttpResponse('班級標題不能為空')
    # if len(title) > 0:
    #     sqlhelper.modify('insert into class(cname) value(%s)', [title, ])
    #     return redirect('/classes/')
    # else:
    #     #頁面不要刷新, 提示錯誤信息
    #     return redirect('/classes/')

def modal_delete_class(request):

    nid = request.POST.get('nid')
    print(nid)
    sqlhelper.modify("delete from class where cid =%s", [nid,])
    return redirect('/classes/')

def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sqlhelper.modify('update class set cname = %s where cid = %s', [content, nid,])

    except Exception as e:
        ret['status'] = False
        ret['message'] = '處理異常'
    return HttpResponse(json.dumps(ret))

#####################################################
def s1(request):

    return render(request, 's1.html')
def modal_add_student(request):
    ret = {'status':True, 'message':None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')

        sqlhelper.modify('insert into student(sname, class_id) values(%s, %s)',[name, class_id])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return  HttpResponse(json.dumps(ret))


def modal_edit_student(request):
    ret = {'status':True, 'message':None}
    try:
        id = request.POST.get('id')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        print(id, name, class_id)
        sqlhelper.modify('update student set sname = %s, class_id = %s where sid = %s', [name, class_id, id, ])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return  HttpResponse(json.dumps(ret))


def add_teacher(request):
    if request.method == 'GET':
        class_list = sqlhelper.get_list('select cid, cname from class', [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        tname = request.POST.get('tname')
        # 老師表中添加一條數據
        teacher_id = sqlhelper.create('insert into teacher(tname) values (%s)', [tname, ])

        class_ids = request.POST.getlist('class_ids')
        # 多次連接, 多次提交
        # for cls_id in class_ids:
        #     sqlhelper.modify('insert into teacher2class(tid, cid) values (%s, %s)', [teacher_id, cls_id, ])

        # 連接一次, 多次提交
        # obj = sqlhelper.SqlHelper()
        # for cls_id in class_ids:
        #     sqlhelper.modify('insert into teacher2class(tid, cid) values (%s, %s)', [teacher_id, cls_id, ])
        # obj.close()


        # 一次連接, 一次提交
        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id, cls_id,)
            data_list.append(temp)
        print(data_list)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into teacher2class(tid, cid) values (%s, %s)', data_list)
        obj.close()

        print(tname, class_ids, teacher_id)
        return redirect('/teachers/')

def edit_teacher(request):

    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = sqlhelper.SqlHelper()

        teacher_info = obj.get_one('select tid, tname from teacher where tid = %s', [nid, ])
        class_id_list = obj.get_list('select cid from teacher2class where tid = %s', [nid,])
        row_list = []
        for i in class_id_list:
            row_list.append(i['cid'])

        class_list = obj.get_list('select cid, cname from class', [])

        obj.close()

        return render(request, 'edit_teacher.html',
                      {'class_list': class_list,
                       'teacher_info': teacher_info,
                       'class_id_list': row_list})
    else:
        nid = request.GET.get('nid')
        tname = request.POST.get('tname')
        class_ids = request.POST.getlist('class_ids')
        print('nid', nid)
        # 更新老師表
        obj = sqlhelper.SqlHelper()
        obj.modify('update teacher set tname = %s where tid=%s', [tname, nid,])
        # 更新老師和班級關係表
        obj.modify('delete from teacher2class where tid = %s', [nid,])
        data_list = []
        for cls_id in class_ids:
            temp = (nid, cls_id,)
            data_list.append(temp)
        print(data_list)
        obj.multiple_modify('insert into teacher2class(tid, cid) values (%s, %s)', data_list)
        obj.close()
        return redirect('/teachers/')

def del_teacher(request):
    nid = request.GET.get('nid')

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from teacher where tid =%s", [nid,])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/teachers/')

def modal_add_teacher(request):
    ret = {'status':True, 'message':None}
    try:
        tname = request.POST.get('name')

        teacher_id = sqlhelper.create('insert into teacher(tname) values (%s)', [tname, ])

        class_ids = request.POST.getlist('class_ids')

        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id, cls_id,)
            data_list.append(temp)

        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into teacher2class(tid, cid) values (%s, %s)', data_list)
        obj.close()

    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def layout(request):
    return render(request, 'layout.html')
def classes_backup(request):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select cid,cname from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'classes_backup.html',  {'class_list': class_list})

def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user, pwd)
        if user == 'alex' and pwd == '123':
            obj = redirect('/classes/')
            obj.set_cookie('ticket', 'asdsadasd')
            return obj
        else:
            return render(request, 'login.html')

