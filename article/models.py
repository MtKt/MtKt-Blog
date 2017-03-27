import os
from datetime import datetime
from django.db import models
from django.conf import settings
#from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import markdown2
from unidecode import *

# Create your models here.

upload_dir = 'content/Article/%s/%s'

class Category(models.Model):
    name = models.CharField('类别', max_length=20, default='Default Value')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    
    ARTICLE_STATUS = {
        0:u'发布',
        1:u'草稿',
    }

    COMMENT_STATUS = {
        0:u'开启',
        1:u'禁用', 
    }
    
    def get_upload_md_name(self, filename):
        if self.pub_date:
            year = self.pub_date.year   # always store in pub_year folder
        else:
            year = datetime.now().year
        upload_to = upload_dir % (year, self.title + '.md')
        return upload_to
    
    def get_html_name(self, filename):
        if self.pub_date:
            year = self.pub_date.year
        else:
            year = datetime.now().year
        upload_to = upload_dir % (year, filename)
        return upload_to

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'作者')
    title = models.CharField('标题', max_length=200)
    body = models.TextField('正文', blank=True)
    md_file = models.FileField('上传MD文件', upload_to=get_upload_md_name, blank=True)
    html_file = models.FileField(upload_to=get_html_name, blank=True)
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)
    last_edit_date = models.DateTimeField('最后修改', auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)
    category = models.ForeignKey(Category,verbose_name=u'类别')
    article_status = models.IntegerField('文章状态', default=0, choices=ARTICLE_STATUS.items())
    #comment_status = models.IntegerField('评论状态', default=0, choices=COMMENT_STATUS.items())
    #s = TaggableManager()

    def __str__(self):
        return self.title 

    class Meta:
        ordering = ['-last_edit_date']

    @property
    def filename(self):
        if self.md_file:
            return os.path.basename(self.title)
        else:
            return 'no md_file'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        if not self.body and self.md_file:
            self.body = self.md_file.read()
        html = markdown2.markdown(self.body,extras=["fenced-code-blocks", "tables"])
        self.html_file.save(self.title + '.html',ContentFile(html.encode('utf-8')), save=False)
        self.html_file.close()
        super().save(*args, **kwargs)

    def display_html(self):
        with open(self.html_file.path, encoding='utf-8') as f:
            return f.read()

    def get_absolute_url(self):
        return reverse('article:article',
                       kwargs={'slug': self.slug, 'article_id': self.id})

@receiver(pre_delete, sender=Article)
def article_delete(instance, **kwargs):
    if instance.md_file:
        instance.md_file.delete(save=False)
    if instance.html_file:
        instance.html_file.delete(save=False)

class Image(models.Model):
    def get_upload_img_name(self, filename):
        upload_to = upload_dir % ('images', filename)  # filename involves extension
        return upload_to
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_img_name)