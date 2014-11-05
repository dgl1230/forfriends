from django.contrib import admin

from .models import Interest,  UserInterestAnswer, Category


class InterestAdmin(admin.ModelAdmin):
	class Meta:
		model = Interest

admin.site.register(Interest, InterestAdmin)



class InterestCategoryAdmin(admin.ModelAdmin):
	class Meta:
		model = Category

admin.site.register(Category, InterestCategoryAdmin)


