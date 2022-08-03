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