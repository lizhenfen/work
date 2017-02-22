

# redis broker
BROKER_URL = 'redis://192.168.15.2:6379/0'
#结果保存
CELERY_RESULT_BACKEND = 'redis://192.168.15.2:6379/0'
#等待被分配到其他职称之前的时间
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600,
                            'fanout_prefix': True  #只被活动的主机接受
                            }

CELERY_ACCEPT_CONTENT=['json']  # Ignore other content
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER='json'
CELERY_TIMEZONE='Europe/Oslo'
CELERY_ENABLE_UTC=True

#降低指定任务的优先级
CELERY_ROUTES = {
    'tasks.add': 'low-priority',
}
#现在处理类型
CELERY_ANNOTATIONS = {
    'tasks.add': {'rate_limit': '10/m'}
}

