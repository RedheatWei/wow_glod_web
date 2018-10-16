from django.db import models

# Create your models here.

class WowGlodPrice(models.Model):
    # id = models.IntegerField(verbose_name='id')
    glod = models.FloatField(verbose_name='金币')
    price = models.FloatField(verbose_name='价格')
    unit_price = models.FloatField(verbose_name='单价')
    area = models.CharField(verbose_name='大区',max_length=60)
    server = models.CharField(verbose_name='服务器',max_length=60)
    camp = models.CharField(verbose_name='阵营',max_length=60)
    order_id = models.CharField(verbose_name='订单ID',max_length=60)
    push_timestrap = models.IntegerField(verbose_name='提交时间',max_length=60)
    url = models.CharField(verbose_name='url',max_length=200)

    class Meta:
        managed = False
        db_table = 'wow_glod_price'