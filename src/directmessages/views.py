import datetime

from django.shortcuts import render_to_response, RequestContext, Http404, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from .models import DirectMessage
from .forms import ComposeForm, ReplyForm



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



def compose(request):
	title = "<h1>Compose</h1>"

	form = ComposeForm(request.POST or None)

	if form.is_valid():
		send_message = form.save(commit=False)
		send_message.sender = request.user
		send_message.sent = datetime.datetime.now()
		send_message.save()
		messages.success(request, "Message sent!")
		return HttpResponseRedirect(reverse('inbox'))

	return render_to_response('directmessages/compose.html', locals(), 
									context_instance=RequestContext(request))

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

def inbox(request):

	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	return render_to_response('directmessages/inbox.html', locals(), 
									context_instance=RequestContext(request))


def sent(request):

	messages_in_inbox = DirectMessage.objects.filter(sender=request.user)

	return render_to_response('directmessages/sent.html', locals(), 
									context_instance=RequestContext(request))
