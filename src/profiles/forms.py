from django import forms
from .models import Address, Info, Job, UserPicture

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDictKeyError
from PIL import Image

from forfriends.settings.deployment import EMAIL_HOST_USER, DEBUG, MEDIA_ROOT


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('city', 'state', 'zipcode',)


class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = ('bio', 'gender',)


class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		fields = ('position', 'employer',)


class UserPictureForm(forms.ModelForm):
	class Meta:
		model = UserPicture
		fields = ('image', 'caption', 'is_profile_pic')
		labels = {
        	'is_profile_pic': 'Make Profile Pic',
		}

UPLOAD_IMG_ID="image_file"

class JcropWidget(forms.Widget):

	jcrop_options = {
				"onSelect": "storeCoords", 
				"onChange": "storeCoords",
	}

	# HTML template for the widget. 
	#
	# The widget is constructed from the following parts:
	#
	#  * HTML <img> - the actual image used for displaying and cropping
	#  * HTML <label> and <input type="file> - used for uploading a new
	#                                          image
	#  * HTML <input type="hidden"> - to remember image path and filename
	#  * JS code - The JS code makes the image a Jcrop widget and 
	#              registers an event handler for the <input type="file"> 
	#              widget. The event handler submits the form so the new
	#              image is sent to the server without the user having
	#              to press the submit button.
	# 
	markup = """
	<img id="jcrop-img" src="%(MEDIA_URL)s%(img_fn)s"/><br/>
	<label for="new-img-file">Neues Bild hochladen:</label>
	<input type="file" name="%(UPLOAD_IMG_ID)s" id="%(UPLOAD_IMG_ID)s"/>
	<input type="hidden" name="imagefile" id="imagefile" value="%(imagefile)s"/>
	<script type="text/javascript">
	function storeCoords(c)
	{
	jQuery('#id_x1').val(c.x);
	jQuery('#id_x2').val(c.x2);
	jQuery('#id_y1').val(c.y);
	jQuery('#id_y2').val(c.y2);
	}
	jQuery(function() {
		jQuery('#jcrop-img').Jcrop(%(jcrop_options)s);
		jQuery('#%(UPLOAD_IMG_ID)s').change(function(e){
		var form = jQuery('#%(UPLOAD_IMG_ID)s').parents('form:first');
		form.submit();
		});
	});</script>
	"""
  
	
	def __init__(self, attrs=None):
		"""
		__init__ does nothing special for now
    	"""
		super(JcropWidget, self).__init__(attrs)
    
	def add_jcrop_options(self, options):
		"""
		add jcrop options; options is expected to be a dictionary of name/value
		pairs that Jcrop understands; 
		see http://deepliquid.com/content/Jcrop_Manual.html#Setting_Options
		"""
		for k, v in options.items():
			self.jcrop_options[k] = v
    
	def render(self, name, value, attrs=None):
		"""
		render the Jcrop widget in HTML
		"""
		# translate jcrop_options dictionary to JavaScipt
		jcrop_options = "{";
		for k, v in self.jcrop_options.items():
			jcrop_options = jcrop_options + "%s: %s," % (k, v)
		jcrop_options = jcrop_options + "}"
    
		# fill in HTML markup string with actual data
		output = self.markup % {
							"MEDIA_URL": settings.MEDIA_URL, 
							"img_fn": str(value),
							"UPLOAD_IMG_ID": UPLOAD_IMG_ID,
							"jcrop_options": jcrop_options,
							"imagefile": value,
							}
		return mark_safe(output)

    
class JcropForm(forms.Form):
	"""
	Jcrop form class
	"""
	imagefile = forms.Field(widget=JcropWidget(), label="", required=False)
	x1 = forms.DecimalField(widget=forms.HiddenInput)
	y1 = forms.DecimalField(widget=forms.HiddenInput)
	x2 = forms.DecimalField(widget=forms.HiddenInput)
	y2 = forms.DecimalField(widget=forms.HiddenInput)
    
	def __init__(self, *args, **kwargs):
		"""
		overridden init func; check for Jcrop options and remove them
		from kwargs
		"""    
		# remove upload image post data (if present); this would make Django form
		# code hick up (since there is no upload image widget in the control)...
		try:
			post_data = args[0]
			if UPLOAD_IMG_ID in post_data:
				del post_data[UPLOAD_IMG_ID]
		except (IndexError):
			# no POST data passed; nothing todo anyway
			pass
  
		jcrop_options = {}
		if "jcrop_options" in kwargs:
			jcrop_options = kwargs["jcrop_options"]
			del(kwargs["jcrop_options"])
  
    	# call base class __init__
		super(JcropForm, self).__init__(*args, **kwargs)
  
		# set Jcrop options for our crop widget 
		self.fields["imagefile"].widget.add_jcrop_options(jcrop_options)
    
	def clean_imagefile(self):
		"""
		instantiate PIL image; raise ValidationError if field contains no image
		"""
		fn = '/' + self.img
		try:
			self.img = Image.open(MEDIA_ROOT + fn)
		except IOError:
			raise forms.ValidationError("Invalid image file")
		return self.cleaned_data["image_file"]
  
  
	def is_valid(self):
		"""
		checks if self._errors is empty; if so, self._errors is set to None and
		full_clean() is called.
		This is necessary since the base class' is_valid() method does
		not populate cleaned_data if _errors is an empty ErrorDict (but not 'None').
		I just failed to work this out by other means...
		"""
		if self._errors is not None and len(self._errors) == 0:
			self._errors = None
			self.full_clean()
		return super(JcropForm, self).is_valid()

	def crop (self):
		"""
		crop the image to the user supplied coordinates
		"""
		x1=self.cleaned_data['x1']
		x2=self.cleaned_data['x2']
		y1=self.cleaned_data['y1']
		y2=self.cleaned_data['y2']
		self.img = self.img.crop((x1, y1, x2, y2))

	def resize (self, dimensions, maintain_ratio=False):
		"""
		resize image to dimensions passed in
		"""
		if maintain_ratio:
			self.img = self.img.thumbnail(dimensions, Image.ANTIALIAS)
		else:
			self.img = self.img.resize(dimensions, Image.ANTIALIAS)

	def save(self):
		"""
		save image...
		"""
		self.img.save(settings.MEDIA_ROOT + self.cleaned_data['imagefile'])

	@staticmethod
	def prepare_uploaded_img(files, profile, max_display_size=None):
		"""
		stores an uploaded image in the proper destination path and 
		optionally resizes it so it can be displayed properly.
		Returns path and filename of the new image (without MEDIA_ROOT).

		'upload_to' must be a function reference as expected by Django's
		FileField object, i.e. a function that expects a profile instance
		and a file name and that returns the final path and name for the
		file. 
			"""
		
		upload_file = files[UPLOAD_IMG_ID]
		
			# files dict does not contain new image


		# copy image data to final file
		fn = '/' + upload_file.name
		pfn = MEDIA_ROOT + fn
		destination = open(pfn, 'wb+')
		for chunk in upload_file.chunks():
			destination.write(chunk)
		destination.close()

		if max_display_size:
			# resize image if larger than specified
			im = Image.open(pfn)
			if im.size[0] > max_display_size[0]:
				# image is wider than allowed; resize it
				im = im.resize((max_display_size[0], 
					im.size[1] * max_display_size[0] / im.size[0]), Image.ANTIALIAS)
			if im.size[1] > max_display_size[1]:
				# image is taller than allowed; resize it
				im = im.resize((im.size[0] * max_display_size[1] / im.size[1], im.size[1]), Image.ANTIALIAS)
			im.save(pfn)

		return fn
		    
