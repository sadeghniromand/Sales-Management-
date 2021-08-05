from django.db import models
from django.utils.translation import ugettext_lazy as _


class StatusFollowUp(models.TextChoices):
    start = 'st', _('پیگیری در دست اقدام است')
    in_process = 'in', _('پیگیری در حال جریان است')
    canceled = 'ca', _('پیگیری منقضی شد')
    finished = 'fi', _('پیگیری تمام شد')
