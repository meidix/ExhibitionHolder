from django.db import models
from django.db.models.signals import ModelSignal
from django_jalali.db import models as jmodels

from .validators import validate_cell_number, validate_phone_number

class Exhibition(models.Model):
    title = models.TextField(help_text="exhibition title")
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    address = models.TextField(help_text="exihibition address")
    form_header = models.TextField(default="با تشکر از حضور جنابعالی در غرفه شرکت فنی مهندسی فناور پویا سپاهان. خواهشمند است نسبت به تکمیل فرم و اعلام درخواست اقدام فرمایید", blank=True)
    active = models.BooleanField(default=False, blank=True)


    def __str__(self):
        return f'{self.title} - {self.start_date}'


class Visitor(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name='visitors')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    cellphone_number = models.CharField(max_length=11, validators=[validate_cell_number])
    phone_number = models.CharField(max_length=11, default="03100000000", blank=True, validators=[validate_phone_number])
    expertise = models.CharField(max_length=50, default="Blank", blank=True)
    state = models.CharField(max_length=30, default="Isfahan", blank=True)
    workplace = models.CharField(max_length=50, blank=True, default="Blank")
    work_position = models.CharField(max_length=50, blank=True, default="Blank")
    email = models.EmailField(null=True, blank=True)

    slaes_opinion = models.TextField(blank=True, default="None")

    def __str__(self):
        return f'{self.exhibition} - {self.first_name} {self.last_name} - {self.cellphone_number}'


class CoopRequest(models.Model):
    visitor = models.ManyToManyField(Visitor, related_name="coop_request")
    label = models.CharField(max_length=40)
    value = models.CharField(max_length=40)

class Products(models.Model):
    visitor = models.ManyToManyField(Visitor, related_name="products_request")
    label = models.CharField(max_length=40)
    value = models.CharField(max_length=40)

post_visitor_request_save = ModelSignal(providing_args=['instance', 'raw', 'created', 'using', 'update_fields'], use_caching=True)