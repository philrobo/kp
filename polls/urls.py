from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.chatindex, name='index'),
    # path('', views.mongoIndex, name='mongoIndex'),

    path('mongo/', views.mongoIndex, name='mongoIndex'),

    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('chatbot/', views.chatbot, name='chatbot'),


]
