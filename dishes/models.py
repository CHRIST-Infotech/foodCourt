from django.db import models

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}/{1}'.format("food",filename)


class dishes(models.Model):
    dish_Id = models.AutoField(primary_key=True)
    d_Name = models.CharField(max_length=100, blank=False, null=False)
    d_Description = models.CharField(max_length=1000, blank=False, null=False)
    d_Ingredients = models.CharField(max_length=500, blank=False, null=False)
    d_Photo = models.FileField(upload_to=user_directory_path, null=True, verbose_name="")
    d_Type = models.CharField(max_length=10, blank=False, null=False)
    d_Add_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dishes'


class dish_votes(models.Model):
    dish_Id = models.AutoField(primary_key=True)
    d_Name = models.CharField(max_length=100, blank=False, null=False)
    v_Date = models.DateField()

    class Meta:
        db_table = 'dish_votes'