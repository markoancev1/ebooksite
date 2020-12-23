from django.contrib import admin
from .models import Profile, Ebook, Comment

admin.site.register(Profile)
admin.site.register(Ebook)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_date', 'active')
    list_filter = ('active', 'created_date')
    search_fields = ('email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
