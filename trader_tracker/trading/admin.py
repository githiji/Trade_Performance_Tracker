from django.contrib import admin
from trading.models import Trade,UserProfile,Tag

admin.site.register(UserProfile)
admin.site.register(Trade)
admin.site.register(Tag)


# Register your models here.
