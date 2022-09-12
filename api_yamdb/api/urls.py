from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    APISignUp, APIToken, CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet, UserViewSet
)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments', CommentViewSet, basename='comments'
)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('auth/signup/', APISignUp.as_view(),
         name='get_confirmation_code'),
    path('auth/token/', APIToken.as_view(), name='get_jwt_token'),
    path('', include(router_v1.urls))
]
