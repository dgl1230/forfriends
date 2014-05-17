from django.contrib import admin
from django.contrib.auth.models import User


from .models import Address, Job, Info, UserPicture
from interests.models import UserInterestAnswer
from matches.models import Match
from questions.models import UserAnswer, MatchAnswer


class AddressInline(admin.TabularInline):
	max_num = 1	
	model = Address


class InfoInline(admin.TabularInline):
	max_num = 1	
	model = Info


class JobInline(admin.TabularInline):
	max_num = 1	
	model = Job


class MatchAnswerInline(admin.TabularInline):
	extra = 0
	model = MatchAnswer

class UserAnswerInline(admin.TabularInline):
	extra = 0
	model = UserAnswer


class UserInterestAnswerInline(admin.TabularInline):
	extra = 0
	model = UserInterestAnswer


class UserPictureInline(admin.TabularInline):
	extra = 0
	model = UserPicture


class UserAdmin(admin.ModelAdmin):
    inlines = [AddressInline, InfoInline, JobInline, 
    		UserPictureInline, UserInterestAnswerInline, UserAnswerInline, 
    		MatchAnswerInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
