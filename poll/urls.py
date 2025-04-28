from django.urls import path
from . import views

urlpatterns = [
    path('', views.voting_view, name='voting'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),     # ← оцей рядок важливий!
    path('logout/', views.logout_view, name='logout'),
    path('vote_success/', views.vote_success_view, name='vote_success'),  # <- додали
    path('vote_results/', views.vote_results_view, name='vote_results'),  # <- додали
    path('voting_heuristics/', views.voting_heuristics, name='voting_heuristics'),  # нова сторінка евристик
    path('heuristic_success/', views.heuristic_application_result, name='heuristic-application-result'),
    path('heuristic_results/', views.heuristic_check, name='heuristic_check'),

]
