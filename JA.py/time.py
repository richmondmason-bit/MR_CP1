import time
import datetime as date 

current_time = time.time()
readable_time = time.ctime(current_time)
new_current_time = date.datetime.now()
hour = new_current_time.strftime("%h")

print(f"Current time in seconds since january 1,1970(epoch): {current_time}")
print(f"Today is {readable_time}")
print(f"today is {readable_time}")

print(f"The hour is saved as an integer {isinstance(hour, int)}")
print(f"The hour is saved as an float {isinstance(hour, float)}")
print(f"The hour is saved as an string {isinstance(hour, str)}")
print(hour.isalpha)

print (f"has a value: {bool(True)}")


#minutes = %m
#weekday = %a %A
#day = %d
#month %b
#month num = %m
#year = %y
#seconds = %s