from django.contrib import admin
from .models import Interest, InterestPicture,  UserInterestAnswer

class InterestAdmin(admin.ModelAdmin):
	class Meta:
		model = Interest

admin.site.register(Interest, InterestAdmin)

class InterestPictureAdmin(admin.ModelAdmin):
	class Meta:
		model = InterestPicture

admin.site.register(InterestPicture, InterestPictureAdmin)


class UserInterestAnswerAdmin(admin.ModelAdmin):
	class Meta:
		model = UserInterestAnswer

admin.site.register(UserInterestAnswer, UserInterestAnswerAdmin)
