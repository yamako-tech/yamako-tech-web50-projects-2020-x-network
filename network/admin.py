from django.contrib import admin


from .models import User, Post, Like, Profile

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Profile)

