from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File


class Document(models.Model):

    file = models.FileField(upload_to = 'files/')
    uploaded_at = models.DateTimeField(auto_now_add = True)
    extension = models.CharField(max_length = 30, blank = True)
    thumbnail = models.ImageField(blank = True, null = True)
    is_public = models.BooleanField(default = False)

    uploaded_by = models.ForeignKey(User,
                                related_name='uploadedByAsUser')

    allowed_users = models.ManyToManyField(User,
                                related_name='allowedUsersAsUser')

    def clean(self):
        self.file.seek(0)
        self.extension = self.file.name.split('/')[-1].split('.')[-1]
        if self.extension == 'xlsx' or self.extension == 'xls':
            self.thumbnail = 'xlsx.png'
        elif self.extension == 'pptx' or self.extension == 'ppt':
            self.thumbnail = 'pptx.png'
        elif self.extension == 'docx' or self.extension == 'doc':
            self.thumbnail = 'docx.png'


    def delete(self, *args, **kwargs):
        #delete file from /media/files
        self.file.delete(save = False)
        #call parent delete method.
        super().delete(*args, **kwargs)

    #Redirect to file list page.
    def get_absolute_url(self):
        return reverse('dashby-files:files')

    def __str__(self):
        return self.file.name.split('/')[-1]

    class Meta():
        #order by upload_date descending
        #for bootstrap grid system. (start left side)
        ordering = ['-uploaded_at']
        #add custom permissions
        #permissions = (('public_access', 'Everyone can see the file'),)


