from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_file, name="upload"),
    path("myfiles/", views.my_files, name="myfiles"),

    path(
        "download/<int:file_id>/",
        views.download_file,
        name="download_file"
    ),

    path(
        "delete/<int:file_id>/",
        views.delete_file,
        name="delete_file"
    ),

    path(
    "share/<uuid:token>/",
    views.share_file,
    name="share_file"
    ),
]