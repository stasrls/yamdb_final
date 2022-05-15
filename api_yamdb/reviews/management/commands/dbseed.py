import copy
import csv
import os
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Categories, Comments, Genres, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = (
        'Команда для заполнения таблиц базы данных.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'tables',
            nargs='+',
            type=str,
            help=(
                'Названия CSV-файлов. Допустимые аргументы: '
                'category, comments, genre, genre_title, '
                'review, titles, users. При единственном '
                'аргументе "__all__" применяются все файлы'
            )
        )

    def handle(self, *args, **options):
        tables_len = len(options['tables'])
        csv_filenames = self.get_filenames()

        tables = []
        if tables_len == 1 and options['tables'][0] == '__all__':
            tables = [
                'users', 'category', 'genre', 'titles', 'review', 'comments'
            ]
        else:
            tables = copy.deepcopy(options['tables'])

        for table in tables:
            if table not in csv_filenames:
                self.stdout.write(
                    self.style.ERROR(
                        'В директории с csv файлами сидов '
                        f'нет файла "{table}.csv"'
                    )
                )
                continue

            seed_method = f'seed_{table}'
            if not hasattr(self, seed_method):
                self.stdout.write(
                    self.style.ERROR(
                        'Для команды dbseed не определен '
                        f'метод seed_{table}'
                    )
                )
                continue

            self.stdout.write(
                self.style.MIGRATE_LABEL(
                    f'Выполнение сида {table}'
                )
            )
            getattr(self, seed_method)(self.get_csv_file(table))

    def seed_users(self, users):
        for user in users:
            try:
                if User.objects.filter(pk=user['id']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            (
                                'Не удалось создать пользователя %s "%s". '
                                'Пользователь с таким id уже существует.'
                            ) % (user['id'], user['username'])
                        )
                    )
                    continue

                new_user = User.objects.create(
                    id=user['id'],
                    username=user['username'],
                    email=user['email'],
                    role=user['role'],
                    bio=user['bio'],
                    first_name=user['first_name'],
                    last_name=user['last_name']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Пользователь "{new_user.username}" успешно создан'
                    )
                )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Не удалось создать пользователя %s "%s"'
                        % (user['id'], user['username'])
                    )
                )

    def seed_category(self, categories):
        for category in categories:
            try:
                if Categories.objects.filter(pk=category['id']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            (
                                'Не удалось создать запись category %s "%s". '
                                'Запись с таким id уже существует.'
                            ) % (category['id'], category['name'])
                        )
                    )
                    continue

                new_category = Categories.objects.create(
                    id=category['id'],
                    name=category['name'],
                    slug=category['slug']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Запись category "%s" успешно создана'
                        % new_category.name
                    )
                )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Не удалось создать запись category %s "%s"'
                        % (category['id'], category['name'])
                    )
                )

    def seed_genre(self, genres):
        for genre in genres:
            try:
                if Genres.objects.filter(pk=genre['id']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            (
                                'Не удалось создать запись genre %s "%s". '
                                'Запись с таким id уже существует.'
                            ) % (genre['id'], genre['name'])
                        )
                    )
                    continue

                new_genre = Genres.objects.create(
                    id=genre['id'],
                    name=genre['name'],
                    slug=genre['slug']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Запись genre "%s" успешно создана'
                        % new_genre.name
                    )
                )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Не удалось создать запись genre %s "%s"'
                        % (genre['id'], genre['name'])
                    )
                )

    def seed_titles(self, titles):
        for title in titles:
            try:
                if Title.objects.filter(pk=title['id']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            (
                                'Не удалось создать запись title %s "%s". '
                                'Запись с таким id уже существует.'
                            ) % (title['id'], title['name'])
                        )
                    )
                    continue

                new_title = Title.objects.create(
                    id=title['id'],
                    name=title['name'],
                    year=title['year'],
                    category=Categories.objects.get(pk=title['category'])
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Запись title "%s" успешно создана'
                        % new_title.name
                    )
                )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Не удалось создать запись title %s "%s"'
                        % (title['id'], title['name'])
                    )
                )

    def seed_genre_title(self, titles):
        pass

    def seed_review(self, reviews):
        for review in reviews:
            try:
                if Review.objects.filter(pk=review['id']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            (
                                'Не удалось создать запись review %s "%s". '
                                'Запись с таким id уже существует.'
                            ) % (review['id'], review['text'])
                        )
                    )
                    continue

                new_review = Review.objects.create(
                    id=review['id'],
                    author_id=review['author'],
                    title_id=review['title_id'],
                    text=review['text'],
                    score=review['score'],
                    pub_date=review['pub_date']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Запись review "%s" успешно создана'
                        % new_review.text
                    )
                )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Не удалось создать запись review %s "%s"'
                        % (review['id'], review['text'])
                    )
                )

    def seed_comments(self, comments):
        for comment in comments:
            try:
                if Comments.objects.filter(pk=comment['id']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            (
                                'Не удалось создать запись comment %s "%s". '
                                'Запись с таким id уже существует.'
                            ) % (comment['id'], comment['text'])
                        )
                    )
                    continue

                new_comment = Comments.objects.create(
                    id=comment['id'],
                    author_id=comment['author'],
                    review_id=comment['review_id'],
                    text=comment['text'],
                    pub_date=comment['pub_date']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Запись comment "%s" успешно создана'
                        % new_comment.text
                    )
                )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Не удалось создать запись comment %s "%s"'
                        % (comment['id'], comment['text'])
                    )
                )

    def get_filenames(self):
        '''Возвращает названия csv-файлов'''
        tables = []
        with os.scandir(settings.SEED_DIR) as entries:
            for entry in entries:
                match = re.search(r'^(?P<filename>.*)\.csv$', entry.name)

                if match is None:
                    self.stdout.write(
                        self.style.ERROR(
                            f'файл "{entry.name}" не является csv файлом'
                        )
                    )
                    continue

                tables.append(match['filename'])

        return tables

    def get_csv_file(self, filename):
        '''Получение содержимого CSV файла'''
        if filename is None:
            raise CommandError('Не указано название CSV-файла сида')

        file = f'{settings.SEED_DIR}/{filename}.csv'
        table = []
        with open(file, newline='') as f:
            reader = csv.reader(f)
            coll = 0
            fields = {}
            for row in reader:
                if coll == 0:
                    for i in range(len(row)):
                        fields[i] = row[i]
                else:
                    row_data = {}
                    for i in range(len(row)):
                        if i not in fields:
                            continue
                        row_data[fields[i]] = row[i]
                    table.append(row_data)

                coll += 1

        return table
