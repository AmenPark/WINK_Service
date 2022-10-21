from django.urls import path
from . import views

# 기능- 단건조회, 단건삭제, 생성, 특정일자 목록 조회,
urlpatterns = [
    path('<int:id>/',views.RoutineAPI.as_view()),  #단건조회, 단건삭제.
    path('', views.RoutineSubmit.as_view()),       #생성, 수정
    path('getlist/',views.GetRoutineList.as_view()), #목록조회
]