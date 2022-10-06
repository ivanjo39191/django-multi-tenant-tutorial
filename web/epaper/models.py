from django.db import models

# Create your models here.

class EPaperEmail(models.Model):
    '''
    電子報訂閱信箱
    '''
    email = models.EmailField('E-mail', max_length=255)
    
    class Meta:
        verbose_name = '電子報訂閱信箱'
        verbose_name_plural = '電子報訂閱信箱'

    def __str__(self):
        return f'{self.email}'