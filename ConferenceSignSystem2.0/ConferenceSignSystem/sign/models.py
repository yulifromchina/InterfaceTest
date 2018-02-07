from django.db import models

# Create your models here.


# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)             # 发布会标题
    limit = models.IntegerField()                       # 参加人数限制
    status = models.BooleanField()                      # 状态，是否激活
    address = models.CharField(max_length=100)          # 召开地址
    start_time = models.DateTimeField()                 # 发布会时间
    create_time = models.DateTimeField(auto_now=True)   # 创建时间

    def __str__(self):
        return self.name


# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)     # 关联发布会id,可以为空，不设置为级联删除
    realname = models.CharField(max_length=64)              # 姓名
    phone = models.CharField(max_length=16)                 # 手机号
    email = models.EmailField()                             # 邮箱
    sign = models.BooleanField()                            # 签到状态
    create_time = models.DateTimeField(auto_now=True)       # 创建时间

    class Meta:  # Meta是内部类，表示不是一个字段的任何数据，unique_together通过两个字段表示唯一性
        unique_together = ("event","phone")

    def __str__(self):
        return self.realname

