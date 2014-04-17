from django.contrib import admin

from .models import DirectMessage

class DirectMessageAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "id"]
	class Meta:
		model = DirectMessage
admin.site.register(DirectMessage, DirectMessageAdmin)