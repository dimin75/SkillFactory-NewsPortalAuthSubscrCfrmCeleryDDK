from django.urls import path
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
   path('', PostList.as_view()),
   path('search', SearchList.as_view()),
   path('<int:pk>', PostView.as_view()),
   path('add', PostCreateView.as_view(), name='post_create'),
   path('edit/<int:pk>', PostUpdateView.as_view(), name='post_edit'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
   path('subscriptions', SubscriptionView.as_view()),
   path('subscribe', add_subscribe),
]
