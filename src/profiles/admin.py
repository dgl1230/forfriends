from django.contrib import admin
from .models import Address, Job, Info, UserPicture


class AddressAdmin(admin.ModelAdmin):
	class Meta:
		model = Address

admin.site.register(Address, AddressAdmin)


class InfoAdmin(admin.ModelAdmin):
	class Meta:
		model = Info

admin.site.register(Info, InfoAdmin)


class JobAdmin(admin.ModelAdmin):
	class Meta:
		model = Job

admin.site.register(Job, JobAdmin)


class UserPictureAdmin(admin.ModelAdmin):
	class Meta:
		model = UserPicture

admin.site.register(UserPicture, UserPictureAdmin)
