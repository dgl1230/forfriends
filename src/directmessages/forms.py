from django import forms

from .models import DirectMessage


class ComposeForm(forms.ModelForm):
	class Meta:
		model = DirectMessage
		fields = ('receiver', 'subject', 'body',)
		widgets = {
			'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
		}

class ReplyForm(forms.ModelForm):
	class Meta:
		model = DirectMessage
		fields = ('body',)
		widgets = {
			'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
		}