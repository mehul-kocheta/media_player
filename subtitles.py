import pysrt
from datetime import time

def date_time_to_millisecond(obj):
  return obj.to_time().hour*3600000 + obj.to_time().minute*60000 + obj.to_time().second*1000 + obj.to_time().microsecond/1000

def srt_to_dict():
  subs = pysrt.open("tbbt.srt")
  l = []
  for i in range(len(subs)):
    l1 = []
    
    l1.append(date_time_to_millisecond(subs[i].start))
    l1.append(date_time_to_millisecond(subs[i].end))
    l1.append(subs[i].text)
    
    l.append(l1)
  
  # print(l[1])
  return l
srt_to_dict()