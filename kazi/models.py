
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

GENDER = (
            ("Male","Male"),
            ("Female","Female")
         )


class BaseContent(models.Model):
  
    publish  = models.DateTimeField(default=timezone.now)            
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    class Meta:
        abstract = True


class Employee(BaseContent):
 
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE)
    id_no = models.IntegerField()
    residence = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=50,choices=GENDER, null=False, blank=False)
    kin_name = models.CharField(max_length=50)
    kin_relation = models.CharField(max_length=50)
    kin_contact = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name


class Customer(BaseContent):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE)
    id_no = models.IntegerField()
    residence = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=50,choices=GENDER, null=False, blank=False)
    id_number = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.user.first_name

class Task(BaseContent):
    title = models.CharField(max_length=50)
    description = RichTextUploadingField()
    due_date = models.DateField()
    done = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    amount = models.IntegerField()
    comments = RichTextUploadingField()
    owner = models.ForeignKey("Customer", on_delete=models.CASCADE)
    employees = models.ManyToManyField("Employee", through="Assignment")

    def __str__(self):
        return self.title

class Assignment(BaseContent):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    assignee = models.ForeignKey("Employee", on_delete=models.CASCADE)

    class Meta:
        unique_together = [["task","assignee"]]

    def __str__(self):
        return self.task.title


class Leave(BaseContent):
    from_date = models.DateField()
    to_date = models.DateField()
    reason = RichTextUploadingField()
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)

    class Meta:
        ordering = ('from_date',)
        verbose_name = 'Leave'
        verbose_name_plural = 'Leavies'
        

    def __str__(self):
        return self.employee.user.first_name
