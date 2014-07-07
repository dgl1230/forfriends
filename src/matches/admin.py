from django.contrib import admin

from .models import Match

class MatchAdmin(admin.ModelAdmin):
	list_display = ['user1', 'user2', 'percent']
	class Meta:
		model = Match
admin.site.register(Match, MatchAdmin)


