from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор')
)

LIMIT_SIMBOLS = 30


class User(AbstractUser):
    email = models.EmailField(
        'Почта', max_length=254, unique=True
    )
    first_name = models.CharField(
        'Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True
    )
    bio = models.TextField(
        'Биография', blank=True, null=True
    )
    role = models.CharField(
        'Роль', max_length=50, choices=ROLES, default='user'
    )
    confirmation_code = models.CharField(
        'Код подтвержения', max_length=100, blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username[:LIMIT_SIMBOLS]


class Category(models.Model):
    name = models.CharField(
        'Название', max_length=256
    )
    slug = models.SlugField(
        'Слаг', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LIMIT_SIMBOLS]


class Genre(models.Model):
    name = models.CharField(
        'Название', max_length=256
    )
    slug = models.SlugField(
        'Слаг', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LIMIT_SIMBOLS]


class Title(models.Model):
    name = models.CharField(
        'Название', max_length=256
    )
    year = models.IntegerField(
        'Год выпуска'
    )
    description = models.TextField(
        'Описание', blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория'
    )
    rating = models.IntegerField(
        null=True, default=None, verbose_name='Рейтинг'
    )

    class Meta:
        verbose_name = 'Произедение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LIMIT_SIMBOLS]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'[:LIMIT_SIMBOLS]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимые значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимые значения от 1 до 10'),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self) -> str:
        return self.title[:LIMIT_SIMBOLS]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self) -> str:
        return self.review[:LIMIT_SIMBOLS]
