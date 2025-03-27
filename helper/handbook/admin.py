from django.contrib import admin

from .models import Monster, Spell, MagicItem

# Register your models here.


admin.site.register(Monster)
admin.site.register(Spell)
admin.site.register(MagicItem)