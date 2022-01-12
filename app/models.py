from django.db import models
from extensions.utils import jalali_converter
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save








#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس  ")

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()

  class Meta:
      verbose_name = "شماره کاربر"
      verbose_name_plural = "شماره کاربران"

  def __str__(self):
    return str(self.phone) +"|"+ str(self.user)








#------------------------------------------------------------------------------
class Newsletter(models.Model):
    email = models.EmailField(max_length = 254 , verbose_name="ایمیل")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ درخواست")

    def __str__(self):
        return str(self.email)








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
        return str(self.month) + " ماهه | " + str(self.price) + ' تومان '









#------------------------------------------------------------------------------
class Requests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "کاربر")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name = "بسته")
    domain = models.CharField(max_length=80, unique=True, verbose_name="نام دامنه")
    discount = models.CharField(max_length=80, blank=True, null=True, verbose_name = "کد تخفیف")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ درخواست")
    final_price = models.IntegerField(null=True, blank=True, verbose_name = "قیمت نهایی")
    CHOICES = ( ('فعال','فعال'), ('لغو شده','لغو شده'), ('در انتظار پرداخت','در انتظار پرداخت'), ('در انتظار فعال سازی','در انتظار فعال سازی') )
    status = models.CharField(max_length=40,choices=CHOICES, default='در انتظار پرداخت', verbose_name = "وضعیت")
    paid = models.BooleanField(default = False, verbose_name="پرداخت شده")
    date_launched = jmodels.jDateField(null=True, blank=True, verbose_name = "تاریخ راه اندازی")

    def get_absolute_url(self):
        return reverse('app:checkout',args=[self.id])

    class Meta:
        verbose_name = "درخواست"
        verbose_name_plural = "درخواست ها"

    def __str__(self):
        return str(self.user.first_name) + str(self.user.last_name) + " | " + str(self.package.month) + " ماهه "














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
