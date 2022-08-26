from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import APIPost, APIComment, APIFollow, APIGroup

router = DefaultRouter()
router.register('posts', APIPost, basename='posts')
router.register('posts/(?P<post_id>[0-9]+)/comments', APIComment,
                basename='comments')


urlpatterns = [

    path('follow/', APIFollow.as_view()),

    path('group/', APIGroup.as_view()),
]

urlpatterns += router.urls