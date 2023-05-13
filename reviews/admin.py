from django.contrib import admin
from .models import Book, BookContributor, Review, Contributor, Publisher, Category


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publication_date', 'publisher', 'price', 'hasSale')
    search_fields = ('id', 'title', 'publisher')
    list_editable = ('hasSale',)
    list_filter = ('hasSale', 'publication_date')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    search_fields = ('category',)
    # prepopulated_fields = {"slug": ("category",)}


admin.site.register(Publisher)
admin.site.register(Contributor)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review)
admin.site.register(Category, CategoryAdmin)
