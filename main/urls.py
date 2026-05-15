from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("info1/", views.info1, name="info1"),
    path("info2/", views.info2, name="info2"),

    path("task13/", views.task13, name="task13"),

    path("education/", views.education, name="education"),
    path("requirements/", views.requirements, name="requirements"),
]
