from django import forms

from .models import DirectMessage
from matches.models import Match
from visitors.models import Visitor

class ComposeForm(forms.ModelForm):
	class Meta:
		model = DirectMessage
		fields = ('receiver', 'body',)
		widgets = {
			'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
		}
		labels = {
        	'receiver': 'To',
		}

class FriendForm(forms.ModelForm):
	class Meta:
		model = DirectMessage
		fields = ('subject', 'body', )
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