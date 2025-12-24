from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("suggestions/", views.chat_suggestions, name="chat_suggestions"),
    path(
        "bank-search/",
        views.search_bank_with_location,
        name="search_bank_with_location",
    ),
]
