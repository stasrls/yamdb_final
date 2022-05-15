from django.contrib import admin

from .models import Categories, Genres, Title, Review, Comments


class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('name',)
    search_fields = ('name', 'slug')


class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('name',)
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year',
        'description',
    )
    list_editable = ('name', 'year')
    search_fields = ('name', 'year')


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'author',
        'text', 'score', 'pub_date',
    )
    list_editable = ('title', 'author', 'score')
    search_fields = ('title', 'author', 'pub_date')


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'review', 'author',
        'text', 'pub_date',
    )
    list_editable = ('review', 'author')
    search_fields = ('review', 'author', 'pub_date')


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
