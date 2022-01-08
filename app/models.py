from django.db import models
from extensions.utils import jalali_converter
from django_jalali.db import models as jmodels










#------------------------------------------------------------------------------
class Discounts(models.Model):
    code = models.CharField(max_length=80, unique=True, verbose_name="کد تخفیف")
    discount_percentage = models.IntegerField(verbose_name = "درصد تخفیف")
    active = models.BooleanField(default = True)

    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف ها"

    def __str__(self):
        return str(self.code)






#------------------------------------------------------------------------------
class Package(models.Model):
    month = models.IntegerField(verbose_name = "ماه")
    price = models.IntegerField(verbose_name= "قیمت (تومان)")

    class Meta:
        verbose_name = "بسته"
        verbose_name_plural = "بسته ها"

    def __str__(self):
        return str(self.month) + " ماهه | " + str(self.price) + 'تومان'









#------------------------------------------------------------------------------
class Requests(models.Model):
    fname = models.CharField(max_length=80, verbose_name="aaaa")
    lname = models.CharField(max_length=80, verbose_name="aaaa")
    phone = models.CharField(max_length=80, verbose_name="aaaa")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name = "بسته")
    discount = models.ForeignKey(Discounts, on_delete=models.CASCADE, verbose_name = "تخفیف")

    class Meta:
        verbose_name = "درخواست"
        verbose_name_plural = "درخواست ها"

    def __str__(self):
        return str(self.fname) + str(self.lname) + " | " + str(self.package.month)














#------------------------------------------------------------------------------
class Contact(models.Model):
    name = models.CharField(max_length=80, verbose_name="نام")
    phone = models.CharField(max_length=50,verbose_name = " شماره تماس  ")
    body = models.TextField(verbose_name="متن پیام")
    CHOICES = ( ('جدید','جدید'), ('برسی شده','برسی شده') )
    status = models.CharField(max_length=30,choices=CHOICES, default='جدید', verbose_name = "وضعیت")
    created_on = models.DateTimeField(auto_now_add=True)

    def j_created_on(self):
        return jalali_converter(self.created_on)


    class Meta:
        verbose_name = "تماس"
        verbose_name_plural = "تماس ها"

    def __str__(self):
        return str(self.name)





# End
