from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (  # isort:skip
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,  # isort:skip
    SignupAPIView, TitleViewSet, TokenAPIView, UserViewSet,  # isort:skip
)  # isort:skip

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('auth/token/', TokenAPIView.as_view(), name='token')
]
