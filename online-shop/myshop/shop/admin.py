from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin

class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug':('name', )}  # NOTE: 'slug' field is of type 'models.SlugField'

class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']  # fields that are editable in the list display in admin dashboard
    
    # Django-parler does not suport the 'prepopulated_fields' attribute, but it does support
    # get_prepopulated_fields(), which has the same purpose
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)