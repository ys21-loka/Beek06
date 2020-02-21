from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from . import forms
from myboard.models import Board
from . import apps


class BoardView(View) :
    def get(self, request, category, pk, mode):
        if  mode == 'add' :
            form = forms.BoardForm()
        elif mode == 'list' :
            username = request.session["username"]
            user = User.objects.get(username=username)
            data = Board.objects.all().filter(category=category)
            
            context = {"data": data, "username": username, "category": category}
            return render(request, "myboard/list.html", context)
        elif mode ==  "detail" :
            p = get_object_or_404(Board, pk=pk)
            p.cnt += 1
            p.save()
            return render(request, "myboard/detail.html", {"d": p,"category":category})
        elif mode == "edit" :
            post = get_object_or_404(Board, pk=pk)
            form = forms.BoardForm(instance=post)
        else :
            return HttpResponse("error page")

        return render(request, "myboard/edit.html", {"form":form})

    def post(self, request, category, pk, mode):

        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0:
            form = forms.BoardForm(request.POST)
        else:
            post = get_object_or_404(Board, pk=pk)
            form = forms.BoardForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
            post.category = category
            post.save()
            return redirect("myboard", category, 0, 'list')
        return render(request, "myboard/edit.html", {"form": form})


def page(request):
    datas = [
        {"id":1, "name":"lee1"},
        {"id":2, "name":"lee2"},
        {"id":3, "name":"lee3"},
        {"id":4, "name":"lee4"},
        {"id":5, "name":"lee5"},
        {"id":6, "name":"lee6"},
        {"id":7, "name":"lee7"},
        ]

    page = request.GET.get("page", 1)
    p = Paginator(datas, 3)
    subs = p.page(page)

    return render(request, "myboard/page.html", {"datas":subs})


def ajaxdel(requst):
    pk = requst.GET.get("pk")
    board = Board.objects.get(pk=pk)
    #board.delete()
    return JsonResponse({'error':'0'})

def ajaxget(request):
    page = request.GET.get("page", 1)
    datas = Board.objects.all().filter(category='common')
    #page = (int)page
    subs = datas[(page-1)*3:(page*3)]
