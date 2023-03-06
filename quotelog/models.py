from django.db import models
from accounts.models import Profile
from django_countries.fields import CountryField
import datetime
year = datetime.date.today().year



# Create your models here.

# --------------- FORM FILL FIELDS
OFFCIE_CHOICE  = (
    ('FIT KENYA','FIT KENYA'),
    ('FIT UGANDA','FIT UGANDA'),
    ('FIT TANZANIA','FIT TANZANIA'),
    ('FIT RWANDA','FIT RWANDA'),
    ('FIT ETHIOPIA','FIT ETHIOPIA'),
    ('FIT SUDAN','FIT SUDAN'),
    ('FIT DJIBOUTI','FIT DJIBOUTI'),
)

QUOTER_CHOICE = (
    ('Q1', 'Q1'),
    ('Q2', 'Q2'),
    ('Q3', 'Q3'),
    ('Q4', 'Q4'),
)

WEEK_CHOICE = (
    ('1', '1'),('2', '2'),('3', '3'),
    ('4', '4'),('5', '5'),('6', '6'),
    ('7', '7'),('8', '8'),('9', '9'),
    ('10', '10'),('11', '11'),('12', '12'),
    ('13', '13'),('14', '14'),('15', '15'),
    ('16', '16'),('17', '17'),('18', '18'),
    ('19', '19'),('20', '20'),('21', '21'),
    ('22', '22'),('23', '23'),('24', '24'),
    ('25', '25'),('26', '26'),('27', '27'),
    ('28', '28'),('29', '29'),('30', '30'),
    ('31', '31'),('32', '32'),('33', '33'),
    ('34', '34'),('35', '35'),('36', '36'),
    ('37', '37'),('38', '38'),('39', '39'),('40', '40'),
    ('41', '41'),('42', '42'),('43', '43'),('44', '44'),
    ('45', '45'),('46', '46'),('47', '47'),('48', '48'),
    ('49', '49'),('50', '50'),('51', '51'),('52', '52'),
)

BUSINESS_TYPE_CHOICE = (
    ('AGENT', 'AGENT'),
    ('EXISTING CUSTOMER', 'EXISTING CUSTOMER'),
    ('NEW CUSTOMER', 'NEW CUSTOMER'),
)

FREIGHT_MODE_TYPE_CHOICE = (
    ('Air freight', 'Air freight'),
    ('Sea freight', 'Sea freight'),
    ('Road freight', 'Road freight'),
    ('Warehousing', 'Warehousing'),
)

REQ_TYPE_CHOICE = (
    ('Import', 'Import'),
    ('Export', 'Export'),
    ('TRANSIT', 'TRANSIT'),
    ('TRANS SHIPMENT', 'TRANS SHIPMENT'),
    ('WAREHOUSING', 'WAREHOUSING'),
    ('LOCAL', 'LOCAL'),
)

NATURE_OF_SERVICE_CHOICE = (
    ('EXW', 'EXW'),('FCA', 'FCA'),('CPT', 'CPT'),
    ('CIP', 'CIP'),('DAP', 'DAP'),('DPU', 'DPU'),
    ('DDP', 'DDP'),('FAS', 'FAS'),('FOB', 'FOB'),
    ('CFR', 'CFR'),('CIF', 'CIF')
)

CARGO_DESCRIPTION_CHOICE = (
    ('General cargo', 'General cargo'), ('Cold Chain', 'Cold Chain'),
    ('Pharma', 'Pharma'), ('Perishables', 'Perishables'),
    ('Harzadous', 'Harzadous')
)

VOLUME_UNIT_CHOICE = (
    ('KGS', 'KGS'),('FT', 'FT'),
    ('RH', 'RH'),('CBM', 'CBM'),
)

QUOTATION_STATUS_CHOICE = (
    ('SENT', 'SENT'),
    ('WON', 'WON'),
    ('LOST', 'LOST',),
    ('PENDING', 'Pending'),
)


# --------------------------------
class QuoteLogdb(models.Model):
    """
        # Model for quotelogs summary
    """
    
    office = models.CharField(max_length=100)
    created_by = models.CharField(max_length=200,blank=True)
    
    # ------------ QUOTELOG Columns
    # 1.  quarter
    quarter = models.CharField(max_length=200,choices=QUOTER_CHOICE)

    # 2. quote_ref_no FIT own number i.e(UG1001/22)
    quote_ref_no = models.CharField(max_length=100,unique = True)

    # 3. week (from 1 to 52)
    week = models.CharField(max_length=200,choices=WEEK_CHOICE)

    # 4. business_type
    business_type = models.CharField(max_length=200, choices=BUSINESS_TYPE_CHOICE)

    # 5. freight_mode
    freight_mode = models.CharField(max_length=200, choices=FREIGHT_MODE_TYPE_CHOICE)

    # 6.request_type
    request_type = models.CharField(max_length=200, choices=REQ_TYPE_CHOICE)

    # 7.nature_of_service_requested
    nature_of_service_requested = models.CharField(max_length=200, choices=NATURE_OF_SERVICE_CHOICE)

    # 8. origin_country
    origin_country = CountryField()

    # 9. origin_port_aiport
    origin_port_airpot = models.CharField(max_length=200)

    # 10. destination_country
    destination_country = CountryField()

    # 11. destination_port_airport
    destination_port_aiport = models.CharField(max_length=200)

    # 12. cargo_description
    cargo_description = models.CharField(max_length=200, choices=CARGO_DESCRIPTION_CHOICE)

    # 13. volume_unit
    volume_unit = models.CharField(max_length=200, choices=VOLUME_UNIT_CHOICE)

    # 14. volume_amount (C.W of no.)
    volume_amount = models.CharField(max_length=50)

    # 15. carrier (if_known)
    carrier = models.CharField(max_length=200,default="", blank = True, null=True)

    # 16. total_buy_rate
    total_buy_rate = models.FloatField()

    # 17. client_quote_sell_rate
    client_quote_sell_rate = models.FloatField()

    # 18. absolute_profit
    absolute_profit = models.FloatField()

    # 19. percentage_profit
    percentage_profit = models.CharField(max_length=6)

    # 20. email_subject (if RFO/RFQ was recieved by mail)
    email_subject = models.TextField(null=True, blank=True)

    # 21. date_of_reciept_of_request (date pick)
    # [https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html]
    date_of_reciept_of_request = models.DateField()

    # 22. date_of_reply_to_client (date pick)
    date_of_reply_to_client = models.DateField()

    # 23. date_of_quote_won_loss
    date_of_quote_won_loss = models.DateField(blank=True)

    # 24. name_of_sales_person (if request from sales team)
    name_of_sales_person = models.CharField(max_length=200,default="", blank = True, null=True)

    # 25. quote_sent_by
    quote_sent_by = models.CharField(max_length=100)

    # 26. quotation status
    quotation_status = models.CharField(max_length=20,choices=QUOTATION_STATUS_CHOICE)

    # 27. feedback_remarks (include reasons why business was lost)
    feedback_remarks = models.TextField()

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        '''
            to set table name in database
        '''
        db_table = "FITQuoteLog"
        ordering = ('quote_ref_no', )
        



    def __str__(self) -> str:
        return f"{self.office}"
