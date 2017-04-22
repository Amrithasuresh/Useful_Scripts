#Every alternate sunday homeplus (Korean discount store retail chain store) have a holiday.
#Wrote a script to remind my friends through an email. I had set a cron job to run only on alternative saturdays.
#The shop is little far away so my friends return often and mention that it was a holiday. 
# took this script from stackoverflow and altered.

#!/usr/bin/python

import smtplib
from smtplib import SMTP

recipients = ['sample@gmail.com', 'sample@gmail.com','sample@gmail.com',\
              'sample@gmail.com','sample@gmail.com','sample@gmail.com']

def send_email (message, status):
    fromaddr = 'sample@gmail.com'
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('sample@gmail.com', 'PASSWORD')
    server.sendmail(fromaddr, recipients, 'Subject: %s\r\n%s' % (status, message))
    server.quit()

send_email("No homeplus tommorow. So prepare yourself to buy. This is sent by a python script \
           . If you dont like these email let him know. \ 
           I would like this to have a bug (:D) and sent 1000 emails to you","Cheers!!!")
