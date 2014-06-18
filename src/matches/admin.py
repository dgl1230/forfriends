from django.contrib import admin

from .models import Match

class MatchAdmin(admin.ModelAdmin):
	list_display = ['user', 'matched', 'percent']
	class Meta:
		model = Match
admin.site.register(Match, MatchAdmin)


