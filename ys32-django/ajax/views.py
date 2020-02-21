from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import sys
from io import StringIO
from ajax.models import User
from django.db import connection


def dictfetchall(fetchall):
    datas=[]
    for f in fetchall:
        datas.append(dict(zip(['filename'], f)))
    data = {'datas':datas}
    return data

def index(request) :
    return HttpResponse("Hello AJAX")    

def uploadimage(request):
    file = request.FILES['filename']
    filename = file._name
    username = "beek06"
    fp = open(settings.BASE_DIR + "/static/face/" + username + "/" + filename, "wb")
    for chunk in file.chunks() :
        fp.write(chunk)
    fp.close()
    author_id = 1
    sql =f"""
    INSERT INTO ajax_image("filename", "author_id")
    VALUES('{filename}', '{author_id}');
    """
    cursor = connection.cursor()
    cursor.execute(sql)

    return redirect('/ajax/uploadimageForm')

def uploadimageForm(request) :
    # username = request.session["username"]
    username = "beek06"
    sql = f"""
    select filename
    from ajax_image
    where author_id=(select id from auth_user 
    where username='{username}')
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    context = dictfetchall(result)

    return render(request, "ajax/photolist.html", context)

def calcForm(request) :
    return render(request, "ajax/calc.html")

def calc(request) :
    op1 = int(request.GET["op1"])
    op2 = int(request.GET["op2"])
    result = op1 + op2
    return JsonResponse({'error':0, 'result':result})

def login(request):
    id = request.GET["id"]
    pwd = request.GET["pwd"]

    if id == pwd :
        request.session["user"] = id
        return JsonResponse({'error': 0})

    return JsonResponse({'error': -1, 'message': 'id/pwd를 확인해 주세요.'})

def loginForm(request):
    return render(request, "ajax/login.html")

# def uploadForm(request) :
#     return render(request, "ajax/uploadajax.html")

# def upload(request) :
#     file = request.POST.get('file1')
#     filename = file._name
#     fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
#     for chunk in file.chunks() :
#         fp.write(chunk)
#     fp.close()
#     return HttpResponse("upload")

def runpythonForm(request):
    return render(request, "ajax/runpython.html")

def runpython(request):
    code = request.GET["code"]
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    exec(code)
    contents = sys.stdout.getvalue()
    sys.stdout = original_stdout
    contents = contents.replace("\n", "<br>")

    return HttpResponse(contents)

def listUser(request):
    if request.method == 'GET':
        userid = request.GET.get("userid", "")
        if userid != "":
            User.objects.all().get(userid=userid).delete()
            return redirect("/ajax/listuser")
        q = request.GET.get("q", "")
        data = User.objects.all()
        if q != "":
            data = data.filter(name__contains=q)
        return render(request, 'template2.html', {"data":data})
    else:
        userid = request.POST["userid"]
        name = request.POST["name"]
        age = request.POST["age"]
        hobby = request.POST["hobby"]
        User.objects.create(userid=userid, name=name, age=age, hobby=hobby)
        return redirect("/ajax/listuser")