from django.contrib import admin
from .models import Post, Category, marketing, comment, Author
from django.contrib import admin

# Register your models here.

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(marketing)
admin.site.register(comment)


admin.site.site_title = "SdBLog"
admin.site.site_header = "SdBlog"
admin.site.index_title = "SdBlog"