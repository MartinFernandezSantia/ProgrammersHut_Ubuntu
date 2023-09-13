from django.urls import path
from . import views
urlpatterns = [
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/update_profile", views.update_profile, name="update_profile"),
    path("profile/<str:username>/add_link", views.add_link, name="add_link"),
    path("profile/delete_link/<str:username>/<int:link_id>/", views.delete_link, name="delete_link"),
    path("profile/<str:username>/update_avatar", views.update_avatar, name="update_avatar"),

]
