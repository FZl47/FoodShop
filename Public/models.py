from django.db import models
from django.conf import settings
from Config import tools
from Config import exceptions
from Config.tools import domain_url, static_url


def upload_image_gallery_site_src(instance, path):
    path = str(path).split('.')[-1]
    if path in settings.IMAGES_FORMAT:
        src = f"images/gallery/site/{tools.RandomString(40)}.{path}"
        return src
    raise exceptions.FormatIsWrong()


class ImageSite(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_image_gallery_site_src)

    def __str__(self):
        return tools.TextToShortText(self.title)

    def get_url(self):
        return domain_url(self.image.url)


class GallerySite(models.Model):
    images = models.ManyToManyField(ImageSite)

    def get_images(self):
        return self.images.all()

    def __str__(self):
        return 'Gallery Site'


class AboutUs(models.Model):
    story_aboutus = models.TextField()
    why_chooseus = models.TextField()


    def __str__(self):
        return 'Pizzle - AboutUs'


class ContactUs(models.Model):
    emails = models.CharField(max_length=300,help_text='You can split with "," for muliple value')
    phones = models.CharField(max_length=300,help_text='You can split with "," for muliple value')
    location = models.CharField(max_length=400,help_text='You can split with "," for muliple value')
    location_image = models.ImageField(upload_to=upload_image_gallery_site_src)

    def __str__(self):
        return 'Pizzle - ContactUs'

    def get_location_image(self):
        return domain_url(self.location_image.url)


class FeedBack(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject[:30]


class SubscribeNews(models.Model):
    email = models.EmailField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):return self.email