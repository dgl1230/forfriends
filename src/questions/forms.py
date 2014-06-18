from django import forms

from .models import Question, Answer, UserAnswer


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('question',)

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ('answer', )
