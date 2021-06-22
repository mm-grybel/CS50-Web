from django.contrib import admin

from .models import Auction, Bid, Comment, Category, Image, User

# Register your models here.

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(User)
