from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    # set fields of the model to be displayed in the admin object list page
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author') # appears in "Filter", on the right
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' # adds a date hierachy, which can be used to navigate (at the top)
    ordering = ['status', 'publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


# register Post model into the admin site using a custom class, which inherits form admin.ModelAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)