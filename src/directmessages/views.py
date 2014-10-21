# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render_to_response, RequestContext, Http404, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Q

from matches.models import Match
from .models import DirectMessage
from .forms import ComposeForm, FriendForm, ReplyForm
from profiles.views import user_not_new




''' Gets a message using the dm_id in the url for the logged in user. The 
user is not allowed to view a message sent from themselves (to prevent errors).
If the user has not seen it already, it's read and read_at fields are changed.'''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def view_direct_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	'''
	if not message.sender != request.user or message.receiver != request.user:
	raise Http404
	'''
	if not message.read:
		message.read = True
		message.read_at = datetime.datetime.now()
		message.save()
	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	
	return render_to_response('directmessages/views.html', locals(), 
										context_instance=RequestContext(request))

@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def view_sent_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	
	return render_to_response('directmessages/views_sent.html', locals(), 
										context_instance=RequestContext(request))

@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def delete_messages(request):
	messages_to_delete = request.POST.getlist('delete_messages')
	DirectMessage.objects.filter(id__in=messages_to_delete).delete()
	return HttpResponseRedirect(reverse('inbox'))


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def delete_individual_message(request, dm_id):
	message = DirectMessage.objects.get(id=dm_id)
	print "getting here for some strange reason"
	message.delete()
	return HttpResponseRedirect(reverse('inbox'))


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def delete_sent_messages(request):
	messages_to_delete = request.POST.getlist('delete_messages')
	DirectMessage.objects.filter(id__in=messages_to_delete).delete()
	return HttpResponseRedirect(reverse('sent'))

@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def delete_individual_sent_message(request, dm_id):
	message = DirectMessage.objects.get(id=dm_id)
	print "getting here"
	message.delete()
	return HttpResponseRedirect(reverse('sent'))



''' The logged in user creates a new message using ComposeForm. The logged in
user can only send messages to users that have approved the logged in user for
friendship and that have also been approved by the logged in user. '''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def compose(request):
	title = "<h1>Compose</h1>"

	form = ComposeForm(request.POST or None)
	
	message_users = []
	matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).filter(user1_approved=True, user2_approved=True)
	for match in matches:
		if match.user1 != request.user:
			message_users.append(match.user1)
		else:
			message_users.append(match.user2)
	try: 
		icebreaker_matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user)).filter(Q(currently_in_icebreaker_user1=True) | Q(currently_in_icebreaker_user2=True))
		for match in icebreaker_matches:
			if match.user1 != request.user:
				message_users.append(match.user1)
			else:
				message_users.append(match.user2)
	except: 
		pass
	form.fields['receiver'].queryset = User.objects.filter(username__in=message_users)
	

	if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.sent = datetime.datetime.now()
			send_message.save()
			return HttpResponseRedirect(reverse('inbox'))

	return render_to_response('directmessages/compose.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in user sends a message to the user who's profile they are currently viewing
via the "send message" button. If both users have approved each other for 
friendship, then the logged in user can message the viewed user from their profile. 
Otherwise, the html template renders a response saying that they aren't both 
approved yet. '''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def su_compose(request, single_user):
	su = User.objects.get(username=single_user)
	title = "<h1>Compose</h1>"

	form = FriendForm(request.POST or None)
	
	if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.receiver = su
			send_message.sent = datetime.datetime.now()
			send_message.save()
			return HttpResponseRedirect(reverse('inbox'))

	return render_to_response('directmessages/su_compose.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in user replies to a message that was sent to them, using
the dm_id field to determine what the correct message to reply to is. '''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
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
		#path = reverse('view_direct_message', args=dm_id)
		#return HttpResponseRedirect(path)
		messages_in_inbox = DirectMessage.objects.filter(sender=request.user)
		return render_to_response('directmessages/sent.html', locals(), 
									context_instance=RequestContext(request))
		

	return render_to_response('directmessages/compose.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in user views all messages that they have'''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def inbox(request):

	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user).order_by('-id')
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	number_of_messages = messages_in_inbox.count()
	return render_to_response('directmessages/inbox.html', locals(), 
									context_instance=RequestContext(request))



'''The logged in viewer views all messages that they have sent'''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def sent(request):

	messages_in_inbox = DirectMessage.objects.filter(sender=request.user).order_by('-sent')
	number_of_messages = messages_in_inbox.count()

	return render_to_response('directmessages/sent.html', locals(), 
									context_instance=RequestContext(request))
