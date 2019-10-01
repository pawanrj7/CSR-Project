from django.urls import path, include
from . import views

# app_name = ''

urlpatterns = [
    path('home/', views.post_list, name='post_list'),
    path('new/', views.post_create, name='post_new'),
    path('edit/<int:pk>/', views.post_update, name='post_edit'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('joining/<int:pk>/', views.post_join, name='post_join'),
    path('index/', include(('user_accounts.urls', 'user_accounts'), namespace='index')),
    path("by/join/<int:pk>/",views.SingleGroup.as_view(),name="post_joining"),
    path('list/attendees/<int:pk>/',views.AttendeesList.as_view(),name="name_attendees"),
    path("join/<int:pk>/",views.JoinGroup.as_view(),name="join"),
    path("leave/<int:pk>/",views.LeaveGroup.as_view(),name="leave"),
    path("userpost/",views.UserPosts.as_view(),name="for_user"), 
    path("see_attending/", views.see_attending,name = "see_attending"),
    path("attinfo/<username>/<int:pk>/",views.AttendeesInfo.as_view(),name="attendees_info"),
]