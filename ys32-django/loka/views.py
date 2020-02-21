from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from loka.models import Post
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import Form
from django.forms import CharField, Textarea, ValidationError
from . import forms

def index(request):
    return HttpResponse("Hello loka!")

class LoginView(View) :
    def get(self, request):
        return render(request, "loka/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        
        if user == None :
            return redirect("/loka/login")        
        else:
            request.session["username"] = username
            return redirect("/loka/0/list")


class PostEditView(View):
    def get(self, request, pk, mode):
        if mode == 'list': # mode가 list일 때. pk 값은 상관이 없다.
            username = request.session.get('username', 'home')
            user = User.objects.get(username=username)
            data = Post.objects.all().filter(author=user) # author field로 검색 후 반환
            context = {'username':user, 'data':data} # html에서 읽기 위해 json화(=딕셔너리화) 시킴.
            return render(request, 'loka/list.html', context)
        elif mode == 'detail':
            post = get_object_or_404(Post, pk=pk) # DB내 Post table에서 요청된 pk 값과 일치하는 포스트 반환
            form = forms.PostForm(instance=post) # instance=post는 무엇을 위한 것인지 모르겠음. 아마 초기 값(원래 작성된 제목 및 본문)을 위한 것 같음.
            return render(request, 'loka/detail.html', {'form':form, 'pk':pk}) # detail.html에서 수정을 위해 pk 값을 넘겨주어야함. 따라서 pk 값을 전달인자에 포함시킴
        elif mode == 'add':
            form = forms.PostForm()
            return render(request, 'loka/edit.html', {'form':form})
        elif mode == 'edit': # 여기서 return이 없는데 이는 맨 밑에 return이 존재하기 때문이다. 즉 아래 edit으로 처음 접속하면(GET 방식으로) 아래 두 줄 수행 후 맨 밑의 return 코드가 실행된다.
            post = get_object_or_404(Post, pk=pk)
            form = forms.PostForm(instance=post)
        else: return HttpResponse('error') # mode에서 정의되지 않은 주소로 접속하면 보여줄 메세지.
        
        return render(request, 'loka/edit.html', {'form':form})
        
    def post(self, request, pk, mode):
        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0: # POST 방식으로 접근했을 때 pk가 0인 경우는 add 밖에 없다(?)
            form = forms.PostForm(request.POST)
        else:
            post = get_object_or_404(Post, pk=pk)
            form = forms.PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
                post.save()
            else:
                post.publish()
            return redirect("edit",0,"list")
        return render(request, "loka/edit.html", {"form": form})

def validator(value) :
    if len(value) < 5 :
        raise  ValidationError("길이가 너무 짧아요")

class PostForm(Form):
    title = CharField(label='제목', max_length=20, validators=[validator])
    text = CharField(label="내용", widget=Textarea)

