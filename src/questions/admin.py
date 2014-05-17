from django.contrib import admin

from .models import Question, Answer, UserAnswer, MatchAnswer

class AnswerInline(admin.TabularInline):
	extra = 0
	model = Answer
	

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]
	class Meta:
		model = Question
admin.site.register(Question, QuestionAdmin)
