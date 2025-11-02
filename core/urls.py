from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register/counselor/', views.register_counselor_view, name='register_counselor'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/v1/predict/', views.predict_emotion_api, name='predict_emotion'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments/manage/', views.appointments_manage, name='appointments_manage'),
    path('api/appointments/<int:appointment_id>/update/', views.appointment_update, name='appointment_update'),
    path('resources/', views.resources_view, name='resources'),
    path('forum/', views.forum_view, name='forum'),
    path('forum/post/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('api/forum/posts/', views.forum_post_create, name='forum_post_create'),
<<<<<<< HEAD
    path('api/forum/posts/<int:post_id>/like/', views.forum_post_like, name='forum_post_like'),
    path('api/forum/posts/<int:post_id>/share/', views.forum_post_share, name='forum_post_share'),
=======
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
    path('api/forum/posts/<int:post_id>/replies/', views.forum_reply_create, name='forum_reply_create'),
    path('forum/moderate/', views.forum_moderate, name='forum_moderate'),
    path('api/forum/<str:item_type>/<int:item_id>/approve/', views.forum_approve, name='forum_approve'),
    path('api/forum/<str:item_type>/<int:item_id>/delete/', views.forum_delete, name='forum_delete'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/dashboard/stats/', views.dashboard_stats_api, name='dashboard_stats'),
<<<<<<< HEAD
    path('checkin/', views.checkin_view, name='checkin'),
    path('api/checkin/', views.checkin_api, name='checkin_api'),
    path('checkin/results/', views.checkin_results_view, name='checkin_results'),
=======
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
    # Token-based API endpoints
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
]

