from django.contrib import admin

from .models import Interest,  UserInterestAnswer, Category



'''
class InterestAdmin(admin.ModelAdmin):
	class Meta:
		model = Interest

admin.site.register(Interest, InterestAdmin)
'''

class InterestAdmin(admin.ModelAdmin):
	class Meta:
		model = Interest

admin.site.register(Interest, InterestAdmin)



class InterestInline(admin.TabularInline):	
	model = Interest




class InterestCategoryAdmin(admin.ModelAdmin):
	inlines = [InterestInline]
	class Meta:
		model = Category

admin.site.register(Category, InterestCategoryAdmin)


