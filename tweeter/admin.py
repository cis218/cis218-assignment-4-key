from django.contrib import admin

from .models import Twit, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class TwitAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Twit, TwitAdmin)
admin.site.register(Comment)
