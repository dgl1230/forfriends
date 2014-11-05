from django.contrib import admin

from .models import Interest,  UserInterestAnswer


class InterestAdmin(admin.ModelAdmin):
	inlines = [InterestPictureInline]
	class Meta:
		model = Interest

admin.site.register(Interest, InterestAdmin)


