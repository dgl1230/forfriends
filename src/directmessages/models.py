from django.db import models

from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.core.urlresolvers import reverse



class DirectMessage(models.Model):
	subject = models.CharField(max_length=150)
	body = models.CharField(max_length=3000)
	sender = models.ForeignKey(User, related_name='sent_direct_messages', null=True, blank=True)
	receiver = models.ForeignKey(User, related_name='recieved_direct_messages', null=True, blank=True)
	sent = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	read = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

	def __unicode__(self):
		return self.subject

	def get_absolute_url(self):
		return (reverse('view_direct_message', kwargs={'dm_id': self.id}))

def set_messages_in_session(sender, user, request, **kwargs):
	direct_messages = DirectMessage.objects.filter(receiver=user)
	request.session['num_of_messages'] = len(direct_messages)



user_logged_in.connect(set_messages_in_session)
