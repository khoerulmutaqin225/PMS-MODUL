# ist with the elements in increasing order.
from datetime import datetime
from datetime import timedelta
yesterday = datetime.today() - timedelta(days=1)
today = datetime.today()
tomorrow = datetime.today() + timedelta(days=1)

date_list =[today, tomorrow, yesterday]
print(date_list)

# Ascending (Kecil Ke besar)
date_list.sort(reverse=False)
# Descending (Besar ke kecil)
date_list.sort(reverse=True)
date_list.a()
print(date_list)