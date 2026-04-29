from django.db import models


class Lion(models.Model):
    TRACK_CHOICES = [
        ('Django', 'Django'),
        ('SpringBoot', 'SpringBoot'),
        ('Frontend', 'Frontend'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]
    name = models.CharField(max_length=100, verbose_name='이름')
    track = models.CharField(max_length=50, choices=TRACK_CHOICES, verbose_name='트랙')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    def __str__(self):
        return f"{self.name} ({self.track})"

    class Meta:
        verbose_name = '아기사자'
        verbose_name_plural = '아기사자 목록'


class Task(models.Model):
    lion = models.ForeignKey(
        Lion,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='아기사자'
    )
    title = models.CharField(max_length=200, verbose_name='과제 제목')
    completed = models.BooleanField(default=False, verbose_name='완료 여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    def __str__(self):
        return f"{self.lion.name} - {self.title}"

    class Meta:
        verbose_name = '과제'
        verbose_name_plural = '과제 목록'


class LionProfile(models.Model):
    lion = models.OneToOneField(
        Lion,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='아기사자'
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub 주소')
    bio = models.TextField(blank=True, verbose_name='자기소개')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    def __str__(self):
        return f"{self.lion.name}의 프로필"

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필 목록'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='태그명')
    lions = models.ManyToManyField(
        Lion,
        related_name='tags',
        blank=True,
        verbose_name='아기사자'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '태그'
        verbose_name_plural = '태그 목록'
