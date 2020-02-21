from django.urls import path
from . import views

app_name = 'loka'
 
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('<int:pk>/<mode>/', views.PostEditView.as_view(), name="edit"),
]


# get 요청
# 0/list : 리스트 출력
# 5/detail : 5번 post 출력
# 0/add : 신규 데이터 작성 -> post 발생
# 5/edit : 5번 post  수정 -> post 발생