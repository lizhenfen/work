from django.db import models
from  django.contrib.auth.models import User

class Idc(models.Model):
    name                = models.CharField('机房名', max_length=50)
    region              = models.CharField('区域', max_length=50,default=None)
    isp                 = models.CharField('运营商', max_length=128, default=None)
    address             = models.CharField('地址', max_length=50, null=True, blank=True)
    phone               = models.CharField('电话', max_length=25, null=True, blank=True)
    email               = models.EmailField('邮箱',null=True, blank=True)
    user_interface      = models.CharField("联系人",max_length=50, null=True, blank=True)
    user_phone          = models.CharField("联系电话",max_length=50, null=True, blank=True)
    status              = models.CharField("状态", max_length=50, null=True, blank=True)
    commet              = models.TextField("备注")
    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = "机房"
        verbose_name_plural = verbose_name

class Manufactures(models.Model):
    name          = models.CharField("厂商名称", max_length=50, unique=True)
    support_phone = models.CharField('支持电话', max_length=50, blank=True)
    comment       = models.TextField('备注')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "厂商"
        verbose_name_plural = verbose_name

class Mem(models.Model):
    sn          = models.CharField('SN', max_length=50, blank=True)
    model       = models.CharField('型号', max_length=50, blank=True)
    manufactory = models.CharField('制造商', max_length=50, null=True,
                                    blank=True)
    slot        = models.CharField('插槽', max_length=32, blank=True)
    capacity    = models.FloatField('容量')
    comment     = models.TextField('备注')
    create_at    = models.DateTimeField(blank=True, auto_now_add=True)
    update_at   = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        if self.capacity != 0:
            return '%s: %sGB' % (self.slot, self.capacity)
        else:
            return  self.slot

    class Meta:
        unique_together = ("sn", "slot")
        verbose_name = "内存"
        verbose_name_plural = verbose_name

class CPU(models.Model):
    sn          = models.CharField('SN', max_length=50, blank=True)
    manufactory = models.CharField('制造商', max_length=50, default=None,
                                   blank=True)
    model       = models.CharField('型号', max_length=50, blank=True)
    comment     = models.TextField('备注')

    def __str__(self):
        return  self.model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = verbose_name

class Disk(models.Model):
    sn = models.CharField('SN', max_length=64,  blank=True)
    slot = models.CharField('插槽', max_length=64, blank=True)
    manufactory = models.CharField('制造商', max_length=64, blank=True)
    capacity = models.FloatField('容量')
    disk_iface_type = (
        ('SSD','SSD'),
        ('SATA','SATA'),
        ('SCSI', 'SCSI'),
        ('SAS', 'SAS')
    )
    iface_type = models.CharField('接口类型',max_length=64, choices=disk_iface_type, blank=True)
    comment = models.TextField('备注')
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('更新时间', auto_now=True)
    def __str__(self):
        return 'slot: %s capacity:%f' %(self.slot, self.capacity)

    class Meta:
        unique_together = ('sn','slot')
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name

class NIC(models.Model):
    sn = models.CharField('SN', max_length=128, blank=True)
    name = models.CharField('插口', max_length=64, blank=True)
    model = models.CharField('网卡型号', max_length=64, blank=True)
    manufactory = models.CharField('制造商', max_length=64, blank=True)
    ip = models.GenericIPAddressField("IP地址", null=True,blank=True)
    mac = models.CharField('MAC地址', max_length=128, blank=True)
    comment = models.TextField('备注')
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('更新时间', auto_now=True)
    def __str__(self):
        return '%s: %s' %(self.name, self.ip)
    class Meta:
        unique_together = ('name', 'mac')
        verbose_name = '网卡'
        verbose_name_plural = verbose_name

class Monitor(models.Model):
    asset = models.OneToOneField('Assets')
    sn    = models.CharField('SN', max_length=64, blank=True)
    manufactory = models.CharField('制造商', max_length=128, blank=True)
    model  = models.CharField('型号', max_length=128, blank=True)
    comment = models.TextField('备注')
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('更新时间', auto_now=True)
    def __str__(self):
        return  self.model
    class Meta:
        verbose_name = '显示器'
        verbose_name_plural = verbose_name

'''
class Contract(models.Model):
    sn = models.CharField('合同号', max_length=64,unique=True)
    name = models.CharField('合同名称', max_length=64 )
    memo = models.TextField('备注', blank=True)
    cost = models.IntegerField('合同金额')
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    license_num = models.IntegerField('license数量',blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"
    def __unicode__(self):
        return self.name
'''
class Assets(models.Model):
    device_type_choice = (
        ('server', '服务器'),
        ('switch', '交换机'),
        ('router', '路由器'),
        ('firewall','防火墙'),
        ('storeage', '存储'),
        ('acc_cpu', 'CPU'),
        ('acc_mem', '内存'),
        ('acc_disk', '硬盘'),
        ('acc_net', '网卡'),
        ('acc_monitor', '显示器'),
        ('acc_others', '其他'),
    )
    device_type = models.CharField('设备类型', max_length=64, choices=device_type_choice,
                                   default='server')
    name = models.CharField('名称', max_length=64)
    hostname = models.CharField('主机名', max_length=64, null=True, blank=True)
    asset_op = models.CharField(max_length=32, null=True, blank=True)
    #contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
    trade_time = models.DateTimeField('购买时间', null=True, blank=True)
    warranty = models.DateTimeField('保修时间', null=True, blank=True)
    price = models.FloatField('价格', null=True, blank=True)
    businessunit = models.ForeignKey('BusinessUnit', verbose_name='业务线',
                                     null=True, blank=True)
    function = models.CharField(max_length=32, null=True, blank=True)
    admin    = models.ForeignKey('UserProfile', verbose_name='设备管理员',
                                 related_name='+', null=True, blank=True)
    client   = models.ForeignKey('UserProfile', verbose_name='所属业务',
                                 null=True, blank=True)
    idc      = models.ForeignKey('Idc', verbose_name='所属机房',
                                 null=True, blank=True)
    cabinet_num  = models.CharField('机柜号', max_length=64, blank=True, null=True)
    cabinet_order= models.CharField('机柜中序号', max_length=64, null=True, blank=True)
    device_status_choice = (
        (1, '未初始化'),
        (2,'备用'),
        (3, '在线'),
        (4, '下线'),
        (5, '不可达'),
        (6, '维修'),
    )
    status = models.CharField('设备状态', max_length=64,choices=device_type_choice,
                             null=True, blank=True)
    comment = models.TextField('备注')
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('更新时间', auto_now=True)
    def __str__(self):
        return 'ID:%s Hostname: %s' % (self.id, self.hostname)
    class Meta:
        verbose_name = '资产'
        verbose_name_plural = verbose_name

class UserProfile(models.Model):
      user = models.OneToOneField(User)
      name = models.CharField('姓名', max_length=64)
      token = models.CharField('Token', max_length=128)
      department = models.CharField('部门', max_length=128)
      businessunit = models.ManyToManyField('BusinessUnit')
      email = models.EmailField('邮箱')
      phone = models.CharField('座机', max_length=32)
      mobile = models.CharField('手机', max_length=32)
      back_name = models.ForeignKey('self',verbose_name='备用联系人', max_length=64,
                                   blank=True, null=True,
                                   related_name ='user_backup_name')
      leader = models.ForeignKey('self', verbose_name='领导', null=True,
                                 blank=True)
      commnet = models.TextField('备注')
      create_at = models.DateTimeField('创建时间',blank=True, auto_now_add=True)
      update_at = models.DateTimeField('更新时间', blank=True, auto_now=True)
      def __str__(self):
          return  self.name
      class Meta:
          verbose_name = '用户信息'
          verbose_name_plural = verbose_name

class BusinessUnit(models.Model):
     name  = models.CharField('业务线', max_length=128, blank=True)
     comment = models.TextField('备注')
     def __str__(self):
         return self.name
     class Meta:
         verbose_name = '业务线'
         verbose_name_plural = verbose_name

class ProductVersion(models.Model):
    name = models.CharField('产品型号',max_length=64, unique=True)
    version = models.CharField('产品版本号',max_length=64,blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '产品版本'
        verbose_name_plural =verbose_name

class RaidAdaptor(models.Model):
    sn          = models.CharField('SN', max_length=50, blank=True)
    name = models.CharField(u'插口', max_length=32, blank=True)
    manufactory = models.CharField('制造商', max_length=50, default=None,
                                   blank=True)
    model       = models.CharField('型号', max_length=50, blank=True)
    comment     = models.TextField('备注')

    def __str__(self):
        return  self.model

    class Meta:
        verbose_name = 'RAID卡类型'
        verbose_name_plural = verbose_name

class Server(models.Model):
    asset = models.OneToOneField('Assets')
    created_by_choice = (
        ('auto', '自动'),
        ('manual', '手动')
    )
    created_by = models.CharField(max_length=32, choices=created_by_choice, default='auto')  # auto: auto created,   manual:created manually
    sn = models.CharField('SN', max_length=64)
    manufactory = models.CharField('制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    cpu_count = models.SmallIntegerField('CPU个数', blank=True)
    cpu_core_count = models.SmallIntegerField('CPU核数', blank=True)
    cpu_model = models.ForeignKey('CPU')
    nic = models.ManyToManyField('NIC', verbose_name='网卡列表')
    raid_type = models.TextField('RAID类型', blank=True)
    physical_disk_driver = models.ManyToManyField('Disk', verbose_name='硬盘', blank=True)
    raid_adaptor = models.ManyToManyField('RaidAdaptor', verbose_name='Raid卡', blank=True)
    # memory
    ram_size = models.IntegerField('内存总大小GB', blank=True)
    ram = models.ManyToManyField('Mem', verbose_name='内存配置', blank=True)

    # software
    software = models.ManyToManyField('Software', verbose_name='软件',
                                      null=True, blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
        index_together = ["sn", "asset"]

class Configuration(models.Model):
    definded_raid_type = models.CharField('预定义raid类型', max_length=32, blank=True, null=True)
    primary_ip = models.ManyToManyField('NIC', verbose_name=u'网卡列表', blank=True)
    os = models.ForeignKey('Software', verbose_name='OS', blank=True, null=True)

    os_installed = models.BooleanField(default=1)
    puppet_installed = models.BooleanField(default=1)
    zabbix_configured = models.BooleanField(default=1)
    auditing_configured = models.BooleanField(default=1)
    approved = models.BooleanField(default=1)

    def __str__(self):
        return '%s ' % self.id
    class Meta:
        verbose_name = '配置信息'
        verbose_name_plural = verbose_name

class NetworkDevice(models.Model):
    asset = models.OneToOneField('Assets')
    sn = models.CharField('SN', max_length=64, unique=True)
    manufactory = models.CharField('制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    firmware = models.ForeignKey('Software')
    port_num = models.SmallIntegerField('端口个数')
    device_detail = models.TextField('设置详细配置')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class Software(models.Model):
    os_types_choice = (
        (1, 'GNU/Linux'),
        (2, 'MS/Windows'),
        (3, 'Network Firmware'),
        (4, 'Softwares'),
    )
    types = models.SmallIntegerField('系统类型', choices=os_types_choice,
                                      help_text=u'eg. GNU/Linux')
    version = models.CharField('软件/系统版本', max_length=64,
                               help_text=u'eg. CentOS release 6.5 (Final)',
                               unique=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"

class Maintainence(models.Model):
    name = models.CharField('事件名称', max_length=100)
    change_choices = (
        (1, '硬件更换'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
        (7, '其它'),
    )
    maintain_type = models.SmallIntegerField('变更类型', choices=change_choices)
    description = models.TextField('事件描述')
    device_sn = models.CharField('AssetID', max_length=64, blank=True)
    event_start = models.DateTimeField('事件开始时间', blank=True)
    event_end = models.DateTimeField('事件结束时间', blank=True)
    applicant = models.ForeignKey('UserProfile', verbose_name='发起人',
                                  related_name='applicant_user')
    performer = models.ForeignKey('UserProfile', verbose_name='执行人')
    memo = models.TextField('备注', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '变更纪录'
        verbose_name_plural = "变更纪录"

class EventLog(models.Model):
    uuid = models.CharField('请求ID', max_length=128, unique=True)
    post_data = models.TextField('请求Data', blank=True)
    detail = models.TextField('详细描述', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True, null=True)

    def __str__(self):
        return self.uuid
    class Meta:
        verbose_name = '事件日志'
        verbose_name_plural = verbose_name

class ApiAuth(models.Model):
    url = models.CharField('接口url', max_length=64)
    description = models.CharField('简介', max_length=64)
    method_choice = (
        ('GET', '允许Get(可读)'),
        ('POST', '允许POST(可修改)'),
        ('PUT', '允许PUT(可 创建)'),
        ('HEAD', 'HEAD(暂不用)'),
        ('PATCH', 'PATCH(暂不用)'),
    )
    method_type = models.CharField('可用方法', choices=method_choice, max_length=32)
    users = models.ManyToManyField('UserProfile', null=True, blank=True)

    class Meta:
        unique_together = ("url", "method_type")
        verbose_name = '接口权限'
        verbose_name_plural = "接口权限"

    def __str__(self):
        return '%s:: %s' % (self.method_type, self.url)
