import pysrt
from datetime import datetime


def accuracy(text1, text2):
    list1 = text1.split(" ")
    # list2 = text2.split(" ")
    # print(list1)
    
    count = 0
    for elem in list1:
        if elem in text2:
            count += 1
    
    return (count/len(list1))*100
            
def error():
    sub1 = pysrt.open("test.srt")
    sub2 = pysrt.open("tbbt.srt")
    
    first  = sub1[0].text.lower()
    
    print(first)
    print(sub1[0].start)
    
    for i in range(len(sub2)):
        temp1 = sub2[i].text.lower()
        if accuracy(first,temp1) > 50:
            print(sub2[i].start)
            print(sub2[i].text)
    print("test")
    

error()

