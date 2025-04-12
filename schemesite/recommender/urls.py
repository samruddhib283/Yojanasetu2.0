from django.urls import path
from . import views
from recommender.views import chatgpt_scheme_recommender

urlpatterns = [

    path('', views.index, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chatgpt-scheme-recommender', chatgpt_scheme_recommender, name='chatgpt_scheme_recommender'),
    path('schemes/', views.all_schemes, name='all_schemes'),
    path('predict-scheme/',views.predict_scheme, name='predict_scheme'),
     path('recommend-scheme/', views.recommend_scheme_page, name='recommend_scheme_page'),
     
    # recommender/urls.py
    path('summarize_filtered_schemes/', views.summarize_filtered_schemes, name='summarize_filtered_schemes'),
    #path('save-scheme-history', views.save_scheme_history, name='save_scheme_history'),
    path('videos/', views.video_guides, name='video_guides'),

     path('chatbot/', views.chatbot_view, name='chatbot'),


]


