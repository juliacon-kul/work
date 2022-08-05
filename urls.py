# from app.views import ElementDetail
# from app.views import ElementList
from app.views import ElementView
from django.urls import path

app_name = 'app'
urlpatterns = [
    path('<slug:slug>/elements/',ElementView.as_view()),
    path('<slug:slug>/elements/<int:pk>/',ElementView.as_view()),

]