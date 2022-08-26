from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import APIPost, APIComment, APIFollow

router = DefaultRouter()
router.register('posts', APIPost, basename='posts')
router.register('posts/(?P<post_id>[0-9]+)/comments', APIComment,
                basename='comments')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('follow/', APIFollow.as_view()),
]

urlpatterns += router.urls