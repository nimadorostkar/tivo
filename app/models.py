from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from extensions.utils import jalali_converter
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels








#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس  ")
  additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
  user_photo = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True, verbose_name = "تصویر")
  CHOICES = ( ('کاربر','کاربر'), ('کاربر ویژه','کاربر ویژه'), ('کارشناس','کارشناس'), ('مدیر','مدیر') )
  user_type = models.CharField(max_length=30,choices=CHOICES, default='کاربر', verbose_name = "نوع کاربر")
  sales_expert = models.ForeignKey("Profile", null=True, blank=True, on_delete=models.CASCADE,verbose_name = "کارشناس مربوطه")
  date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")


  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()

  def get_absolute_url(self):
      return reverse('customer_detail',args=[self.id])

  def get_absolute_edit_url(self):
      return reverse('customer_edit',args=[self.id])


  def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.user_photo.url))

  @property
  def short_description(self):
      return truncatechars(self.additional_information, 50)


  def user_name(self):
        return str(self.user)

  class Meta:
      verbose_name = "کاربر"
      verbose_name_plural = "کاربران"

  def __str__(self):
    return self.user_type +"|"+ str(self.user)





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

    def get_absolute_url(self):
        return reverse('contact_detail',args=[self.id])

    class Meta:
      verbose_name = "تماس"
      verbose_name_plural = "تماس ها"

    def __str__(self):
        return str(self.name)





# End
