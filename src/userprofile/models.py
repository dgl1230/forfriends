from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.db.models.signals import post_save



GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female')
)


class Interest(models.Model):
	content = models.CharField(max_length=30)
	user = models.ForeignKey(User)

class UserProfile(models.Model):
	birthday = models.DateTimeField()
	city = models.CharField(max_length=20)
	country = models.CharField(max_length=40)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	last_name = models.CharField(max_length =20)
	modified = models.DateTimeField(auto_now=True)
	#picture
	summary = models.CharField(max_length=420)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return smart_unicode(self.user.email)


