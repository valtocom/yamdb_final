from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Genres, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, OwnerOrReadOnly

from .serializers import (  # isort:skip
    CategorySerializer, CommentSerializer, GenreSerializer,  # isort:skip
    ReviewSerializer, SignupSerializer, TitleSerializerCreate,  # isort:skip
    TitleSerializerRead, TokenSerializer, UserSerializer  # isort:skip
)  # isort:skip
from rest_framework import filters, status, mixins, viewsets  # isort:skip
from rest_framework.permissions import (  # isort:skip
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly  # isort:skip
)  # isort:skip


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения пользователей."""
    queryset = User.objects.all()
    http_method_names = ['patch', 'get', 'post', 'delete', 'head']
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['patch', 'get'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated, ],
        serializer_class=UserSerializer,
    )
    def users_own_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignupAPIView(APIView):
    """Вьюсет для регистрации и отправки на email."""
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(
                username=username,
                email=email
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            user, created = User.objects.get_or_create(serializer.data)
        except IntegrityError:
            raise ValidationError('Неверные данные для входа')

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb registration',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    """Вьюсет для подтверждения доступа."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User)
        if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateRetrieveDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для передачи и получения информации о
    модели Title. Создает и удаляет админ.
    Нет методов retrieve и update."""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    )
    serializer_class = TitleSerializerRead
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('name', 'year', 'description', 'genre')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateRetrieveDeleteViewSet):
    """Вьюсет для передачи и получения информации о
    модели Categories. Создает и удаляет админ.
    Нет методов retrieve и update."""
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateRetrieveDeleteViewSet):
    """Вьюсет для передачи и получения информации о
    модели Genres. Изменения вносит админ."""
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def _get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def _get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self._get_review().comments.select_related('title', 'author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self._get_title(),
            review=self._get_review(),
        )
