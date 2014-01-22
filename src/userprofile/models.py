from django.db import models
from django.utils.encoding import smart_unicode

GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female')
)


class UserProfile(models.Model):
	birthday = models.DateTimeField()
	city = models.CharField(max_length=20)
	country = models.CharField(max_length=40)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	email = models.EmailField()
	first_name = models.CharField(max_length=20)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	last_name = models.CharField(max_length =20)
	modified = models.DateTimeField(auto_now=True)
	state = models.CharField(max_length=2, blank=True)
	summary = models.CharField(max_length=420)
	username = models.CharField(max_length=20)

	def __unicode__(self):
		return smart_unicode(self.email)


