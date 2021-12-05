from django.db import models
from django_jalali.db import models as jmodels

from .validators import validate_cell_number, validate_phone_number

class Exhibition(models.Model):
    title = models.TextField(help_text="exhibition title")
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    address = models.TextField(help_text="exihibition address")
    form_header = models.TextField(default="با تشکر از حضور جنابعالی در غرفه شرکت فنی مهندسی فناور پویا سپاهان. خواهشمند است نسبت به تکمیل فرم و اعلام درخواست اقدام فرمایید")


    def __str__(self):
        return f'{self.title} - {self.start_date}'


class Visitor(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name='visitors')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    cellphone_number = models.CharField(max_length=11, validators=[validate_cell_number])
    phone_nunmber = models.CharField(max_length=11, default="03100000000", blank=True, validators=[validate_phone_number])
    expertise = models.CharField(max_length=50, default="Blank", blank=True)
    state = models.CharField(max_length=30, default="Isfahan", blank=True)
    workplace = models.CharField(max_length=50, blank=True, default="Blank")
    work_position = models.CharField(max_length=50, blank=True, default="Blank")
    email = models.EmailField(null=True, blank=True)

    class CoopRequest(models.TextChoices):
        BUY_PRODUCTS = 'buy products'
        SALES_BRANCH = 'sales branch'
        AFTER_SALE_BRANCH = 'after sales branch'
        GET_CATALAOUGUE = ' get catalougue'
        PRESENTATION = 'presentation'
        NOTSET = 'not mentioned'

    coop_request = models.CharField(max_length=60, choices=CoopRequest.choices, blank=True, default=CoopRequest.NOTSET)

    class Products(models.TextChoices):
        VACUUM_THERAPY = 'vaccumed vac'
        HYPER = 'vacumed vac Hyper'
        HYPERMID = 'vacumed vac Hypermid'
        CANISTER = 'canister'
        DRESSING_KIT = 'dressing kit'
        MICRODERM = 'microderm abrasion'
        MICROPIGMENTATION = 'micro pigmentation'
        MICRONEEDLING = 'miconeedling'
        PROBE = 'microderm probes'
        LIFTING_PROBE = 'microderm lifting probes'
        P1_CARTRIDGES = 'Micropigmentation cartridges'
        P2_CARTRIDGES = 'Microneddling cartridges'
        NOTSET = 'not mentioned'

    product_request = models.CharField(max_length=70, choices=Products.choices, blank=True, default=Products.NOTSET)
    slaes_opinion = models.TextField(blank=True, default="None")