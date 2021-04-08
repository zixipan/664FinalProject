from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class Kind(models.Model):
    kind = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(1, "Kind must be greater than 1 character")]
    )
    breed = models.TextField()


class Pet(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    age = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')

    contacts = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Contact', related_name='contacts_owned')

    locations = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Location', related_name='locations_owned')
    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_pets')

    kind = models.ForeignKey(Kind, on_delete=models.CASCADE)

    # Shows up in the admin list
    def __str__(self):
        return self.title

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


class Contact(models.Model):
    email = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(2, "Email must be greater than 2 characters")]
    )
    phone = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Location(models.Model):
    state = models.CharField(
            max_length=2,
            validators=[MinLengthValidator(1, "State must be greater than 1 character")]
    )
    zipcode = models.TextField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Fav(models.Model) :
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('pet', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.pet.title[:10])
