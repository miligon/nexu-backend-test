from django.db import models

class Brands(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True) 
    name = models.CharField(max_length=50, null=True, blank=False)

class ModelInfo(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    brand_name = models.ForeignKey(Brands, related_name='models', on_delete=models.PROTECT, verbose_name="Marca")
    name = models.CharField(max_length=50, null=True, blank=False)
    average_price = models.PositiveBigIntegerField(default=0, blank=True)
