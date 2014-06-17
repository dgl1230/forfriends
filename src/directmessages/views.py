# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render_to_response, RequestContext, Http404, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from matches.models import Match
from .models import DirectMessage
from .forms import ComposeForm, FriendForm, ReplyForm
from visitors.models import Visitor


''' Gets a message using the dm_id in the url for the logged in user. The 
user is not allowed to view a message sent from themselves (to prevent errors).
If the user has not seen it already, it's read and read_at fields are changed.'''
def view_direct_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	if not message.sender != request.user or message.receiver != request.user:
		raise Http404
	if not message.read:
		message.read = True
		message.read_at = datetime.datetime.now()
		message.save()
	
	return render_to_response('directmessages/views.html', locals(), 
										context_instance=RequestContext(request))



''' The logged in user creates a new message using ComposeForm. The logged in
user can only send messages to users that have approved the logged in user for
 friendship and that have also been approved by the logged in user. '''
def compose(request):
	title = "<h1>Compose</h1>"

	form = ComposeForm(request.POST or None)
	
	message_users = []
	matches = Match.objects.filter(user=request.user, approved=True)
	for match in matches:
		try:
			match2 = Match.objects.get(user=match.matched, matched=request.user)
			if match2.approved == True:
				message_users.append(match.matched.username)
		except:
			pass
	form.fields['receiver'].queryset = User.objects.filter(username__in=message_users)
	

	if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.sent = datetime.datetime.now()
			send_message.save()
			messages.success(request, "Message sent!")
			return HttpResponseRedirect(reverse('inbox'))

	return render_to_response('directmessages/compose.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in user sends a message to the user who's profile they are currently viewing
via the "send message" button. If both users have approved each other for 
friendship, then the logged in user can message the viewed user from their profile. 
Otherwise, the html template renders a response saying that they aren't both 
approved yet. '''
def su_compose(request, single_user):
	user_match, created = Match.objects.get_or_create(user=request.user, 
								matched__username=single_user)
	visited_match, created = Match.objects.get_or_create(user__username=single_user, 
											matched=request.user)
	title = "<h1>Compose</h1>"

	form = FriendForm(request.POST or None)
	if user_match.approved == True:
		true1 = True
	else:
		true1 = False
	if visited_match.approved == True:
		true2 = True
	else:
		true2 = False

	if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			form.receiver = single_user
			send_message.sent = datetime.datetime.now()
			send_message.save()
			messages.success(request, "Message sent!")
			return HttpResponseRedirect(reverse('inbox'))

	return render_to_response('directmessages/su_compose.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in user replies to a message that was sent to them, using
the dm_id field to determine what the correct message to reply to is. '''
def reply(request, dm_id):

	parent_id = dm_id
	parent = get_object_or_404(DirectMessage, id=parent_id)
	title = "<h1>Reply<small> %s from %s</small></h1>" %(parent.subject, parent.sender)
	form = ReplyForm(request.POST or None)

	if form.is_valid():
		send_message = form.save(commit=False)
		send_message.sender = request.user
		send_message.receiver = parent.sender
		send_message.subject = "RE: " + parent.subject
		send_message.sent = datetime.datetime.now()
		send_message.parent = parent
		send_message.save()
		parent.replied = True
		parent.save()
		messages.success(request, "Reply sent!")
		path = reverse('view_direct_message', args=dm_id)
		return HttpResponseRedirect(path)

	return render_to_response('directmessages/compose.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in user views all messages that they have'''
def inbox(request):

	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	return render_to_response('directmessages/inbox.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in viewer views all messages that they have sent'''
def sent(request):

	messages_in_inbox = DirectMessage.objects.filter(sender=request.user)

	return render_to_response('directmessages/sent.html', locals(), 
									context_instance=RequestContext(request))
