import datetime

x=datetime.datetime.now()
print(x)

import datetime

x=datetime.datetime.now()
print(x.day)
print(x.year)
print(x.strftime("%A"))
print(x.strftime("%B"))
print(x.strftime("%d"))
print(x.strftime("%p"))
print(x.strftime("%X"))

from datetime import datetime,timedelta
nowdate=datetime.now()
futuredate=nowdate+timedelta(days=5)
print(futuredate)

tomorrow=nowdate+timedelta(days=1)
print(tomorrow.strftime("%A"))
print(nowdate.strftime("%A"))
yesterday=nowdate-timedelta(days=1)
print(yesterday.strftime("%A"))
print(nowdate.strftime("%f"))


from datetime import datetime
d1 = input().strip()
d2 = input().strip()
date1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")

difference = abs((date2 - date1).total_seconds())

print(int(difference))

