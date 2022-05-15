import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Categories, Comments, Genres, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256
    )
    slug = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=Categories.objects.all())]
    )

    class Meta:
        exclude = ['id']
        model = Categories
        # extra_kwargs = {
        #     'slug': { не работает т.к. поле явно объявлено в классе
        #         'validators': [
        #             UniqueValidator(
        #                 queryset=Categories.objects.all()
        #             )
        #         ]
        #     }
        # }


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField(
        validators=[UniqueValidator(queryset=Genres.objects.all())]
    )

    class Meta:
        exclude = ['id']
        model = Genres


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(
        read_only=True,
        min_value=0,
        max_value=10,
        default=0
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleWriteSerializer(TitleReadSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year'],
                message='Произведение с таким именем и годом уже существует!'
            )
        ]

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError(
                'Год произведение может быть от 0 до текущего года'
            )
        return value

    def to_representation(self, instance):
        '''Вместо слага возвращает десериализованный объект'''
        ret = super().to_representation(instance)

        if 'category' in ret and isinstance(ret['category'], str):
            category_slug = ret.pop('category')
            category = Categories.objects.get(slug=category_slug)
            categorySerializer = CategorySerializer(category)
            ret['category'] = categorySerializer.data

        if 'genre' in ret and isinstance(ret['genre'], list):
            genre_slugs = ret.pop('genre')
            genres = []
            for genre_slug in genre_slugs:
                genre = Genres.objects.get(slug=genre_slug)
                genreSerializer = GenreSerializer(genre)
                genres.append(genreSerializer.data)
            ret['genre'] = genres

        return ret


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Этот login уже используется'
        )]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Этот email уже используется'
        )]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio',
        )


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        read_only=True,
        validators=[
            UniqueValidator(
                queryset=Categories.objects.all(),
                message='Этот логин уже используется'
            )
        ]
    )
    email = serializers.EmailField(
        read_only=True,
        validators=[
            UniqueValidator(
                queryset=Categories.objects.all(),
                message='Этот email уже используется'
            )
        ]
    )
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio',
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Этот email уже используется'
        )
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Этот login уже используется'
        )
        ]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать такой логин'
            )
        return value

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio',
        )


class ConfirmationCodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=150)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method == "POST":
            reviews = Review.objects.filter(
                author=request.user.id,
                title=request.parser_context.get('kwargs').get('title_id'),
            )

            if reviews.exists():
                raise serializers.ValidationError(
                    'Автор может оставлять только один отзыв '
                    'на определённое произведение'
                )

        return data

    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Значение score должно быть больше либо равно 0!'
            )

        if value > 10:
            raise serializers.ValidationError(
                'Значение score должно быть меньше либо равно 10!'
            )

        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
