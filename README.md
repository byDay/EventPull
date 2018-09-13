# EventPull
EventPull program for ATLbyDay.com

#Credentials

EventPull : 52.23.55.129
postgres : eventpull_user/dalvikking
postgres : postgres/dalvikking2108
Admin : eventpull_admin/dalvik2108

celery -A EventPullingService worker -l info

celery flower -A EventPullingService --broker=redis://127.0.0.1:6379/0
