from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       get_confirmation_code, get_user_token)

router = DefaultRouter()
router.register('v1/users', UserViewSet, basename='users')
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)
router.register('v1/titles', TitleViewSet)
router.register(r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)

urlpatterns = [
    path('', include(router.urls), name='api'),
    path('v1/auth/token/', get_user_token, name='signup'),
    path('v1/auth/signup/', get_confirmation_code, name='token'),
]
