# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from matches.models import Match 
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile





GENDER_CHOICES = (
	('Male', 'Male'),
	('Female', 'Female')
)

class Address(models.Model):
	user = models.ForeignKey(User)
	country = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	zipcode = models.IntegerField(max_length=5, null=True, blank=True)
	
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.city


class Gamification(models.Model):
	user = models.ForeignKey(User, related_name="logged_in_user")
	circle = models.ManyToManyField(Match)
	friends_list = models.ManyToManyField(User, related_name="friends_list", null=True, blank=True)

	circle_time_until_reset = models.DateTimeField(null=True, blank=True)


	icebreaker_until_reset = models.DateTimeField(null=True, blank=True)

	

	def __unicode__(self):
		return self.user.username

	



class Info(models.Model):
	user = models.ForeignKey(User)
	bio = models.CharField(max_length=420, null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
	is_new_user = models.BooleanField(default=True)
	signed_up_with_fb_or_goog = models.BooleanField(default=True)

	def __unicode__(self):
		return self.user.username


class Job(models.Model):
	user = models.ForeignKey(User)
	position = models.CharField(max_length=200)
	employer = models.CharField(max_length=200)

	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.position


def save_path(instance, filename):
	number = instance.get_num_user_pics() + 1
	#number = number + 1
	return 'profiles/' + str(instance.user.username) + "/picture_number-" + str(number) + '/' + filename 


class UserPicture(models.Model):
	user = models.ForeignKey(User)
	caption = models.CharField(max_length=100, null=True, blank=True)
	image = models.ImageField(upload_to=save_path, max_length=200)
	#image = ImageCropField(null=True, blank=True, upload_to='profiles/')
	is_profile_pic = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	cropped_image = models.ImageField(blank=True, null=True, upload_to='profiles/')

	
	active = models.BooleanField(default=True)


	def __unicode__(self):
		return str(self.image)



	def save(self, *args, **kwargs):
		if self.is_profile_pic:
			try:
				temp = UserPicture.objects.filter(user=self.user).filter(is_profile_pic=True)
				for pic in temp:
					if self != pic:
						pic.is_profile_pic = False
						pic.save()
			except:
				pass
		super(UserPicture, self).save(*args, **kwargs)


	def get_num_user_pics(self):
		num_of_pics = UserPicture.objects.filter(user=self.user).count()
		'''
		try: 
			num_of_pics = UserPicture.objects.filter(user=self.user).count()
		except:
			num_of_pics = 0
		return num_of_pics
		'''
		return num_of_pics


	@receiver(pre_delete, sender=ContentFile)
	def remove_file_from_s3(sender, instance, using):
	    instance.content.delete(save=False)










