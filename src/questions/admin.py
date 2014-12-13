from django.contrib import admin

from .models import Question, Answer, UserAnswer

class AnswerInline(admin.TabularInline):
	extra = 0
	model = Answer
	

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]
	class Meta:
		model = Question
admin.site.register(Question, QuestionAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
	class Meta:
		model = UserAnswer
admin.site.register(UserAnswer, UserAnswerAdmin)
