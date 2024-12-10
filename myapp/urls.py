from django.urls import path,include
from .import views

app_name = "myapp"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('create/', views.create_question, name='create_question'),  
    path('<int:question_id>/add_choices/', views.add_choices, name='add_choices'), 
]