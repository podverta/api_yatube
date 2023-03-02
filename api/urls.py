from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from .views import PostViewSet, APIComment, APIFollow, APIGroup

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('posts/(?P<post_id>[0-9]+)/comments', APIComment,
                basename='comments')
router.register('follow', APIFollow)


urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('group/', APIGroup.as_view()),

]

urlpatterns += router.urls