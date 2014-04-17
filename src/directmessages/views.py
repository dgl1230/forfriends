import datetime
from django.shortcuts import render_to_response, RequestContext, Http404, get_object_or_404

from .models import DirectMessage
from .forms import ComposeForm



def view_direct_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	if not message.sender != request.user or message.receiver != request.user:
		raise Http404
	if not message.read:
		message.read = datetime.datetime.now()
		message.save()
	
	return render_to_response('directmessages/view.html', locals(), 
					context_instance=RequestContext(request))



def compose(request):

	form = ComposeForm(request.POST or None)

	if form.is_valid():
		send_message = form.save(commit=False)
		send_message.sender = request.user
		send_message.sent = datetime.datetime.now()
		send_message.save()

	return render_to_response('directmessages/compose.html', locals(), 
									context_instance=RequestContext(request))

def inbox(request):

	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	request.session['num_of_message'] = len(messages_in_inbox)

	return render_to_response('directmessages/inbox.html', locals(), 
									context_instance=RequestContext(request))


def sent(request):

	messages_in_inbox = DirectMessage.objects.filter(sender=request.user)

	return render_to_response('directmessages/sent.html', locals(), 
									context_instance=RequestContext(request))
