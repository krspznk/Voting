from django.urls import path
from . import views

urlpatterns = [
    path('', views.voting_view, name='voting'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),     # ← оцей рядок важливий!
    path('logout/', views.logout_view, name='logout'),
    path('vote_success/', views.vote_success_view, name='vote_success'),  # <- додали
    path('voting-heuristics/', views.voting_heuristics, name='voting_heuristics'),  # нова сторінка евристик
    path('vote-heuristics-success/', views.vote_heuristics_success, name='vote_heuristics_success'),

]
