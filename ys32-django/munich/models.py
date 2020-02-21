from django.db import models
from django.urls import reverse # url패턴을 만들어주는 장고의 내장 함수

# Create your models here.

class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias')
    # slug : 페이지나 포스트를 설명하는 핵심 단어의 집합. 콘텐츠의 고유 주소. 콘텐츠가 어떤 내용인지 쉽게 이해하도록 도움.
    # slugField :  제목의 단어들을 -으로 연결. url에서 pk대신 사용되는 경우가 많음. default length = 50
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text')
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'munich_posts'
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('munich:post_detail', args=(self.slug,))

    def get_previous(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()
