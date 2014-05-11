from django.contrib import admin

from .models import Interest, InterestPicture,  UserInterestAnswer


class InterestPictureInline(admin.TabularInline):
	max_num = 1	
	model = InterestPicture




class InterestAdmin(admin.ModelAdmin):
	inlines = [InterestPictureInline]
	class Meta:
		model = Interest

admin.site.register(Interest, InterestAdmin)


