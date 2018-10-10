#!/usr/bin/env python3

"""Email me list of available items updated yesterday attached to suppressed bibs

Author: Nina Acosta
"""

import psycopg2
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import date, timedelta
yesterday = date.today() - timedelta(1)
subject = yesterday.strftime ("%m/%d/%Y")

#SQL Query:
q='''SELECT
CONCAT('i',item_view.record_num, 'a', '          ', title)
--adds i prefix to the item record number and the "a" as a placeholder for the check digit, so the number can be easily copied and pasted into Sierra, also includes the title

FROM sierra_view.bib_view
JOIN sierra_view.bib_record_item_record_link
ON bib_view.id = bib_record_item_record_link.bib_record_id
JOIN sierra_view.item_view
ON bib_record_item_record_link.item_record_id = item_view.id
JOIN sierra_view.record_metadata
ON record_metadata.id = item_view.id

WHERE
record_last_updated_gmt > TIMESTAMP 'yesterday' AND
bcode3 = 'n' AND
title not like '%linking%' AND
icode2 != 'n'
-- This limits results to any unsuppressed item records updated since midnight of the previous day, that are attached to a suppressed bib

ORDER BY title
--sorts results alphabetically by title
'''
#This code uses placeholder info to connect to Sierra SQL server, please replace with your own info
conn = psycopg2.connect("dbname='iii' user='******' host='000.000.000.000' port='1032' password='******' sslmode='require'")

#Open session and run query
cursor = conn.cursor()
cursor.execute(q)
rows = cursor.fetchall()
conn.close()

convert = str(rows)
data = convert.replace("',), ('", "\r\n").replace("[('", "").replace("',)]","") #Create linebreaks between results in email

# These are variables for the email that will be sent.
# This code uses placeholders, please add your own email server info
emailhost = 'email.server.midhudson.org'
emailuser = 'emailaddress@midhudson.org'
emailpass = '*******'
emailport = '587'
emailsubject = 'Suppressed records updated ' + str(subject)
emailmessage = '''

The items listed below were updated yesterday, but are attached to a suppressed record.
Please review for possible errors.

''' +str(data) #Appends SQL results to the end of the email

emailfrom= 'emailaddress@midhudson.org'
emailto = 'nacosta@midhudson.org'

#Create an email with an attachement
msg = MIMEMultipart()
msg['From'] = emailfrom
if type(emailto) is list:
    msg['To'] = ', '.join(emailto)
else:
    msg['To'] = emailto
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = emailsubject
msg.attach (MIMEText(emailmessage))
#msg = MIMEText(type._htmlBody, "html")
#Send the email
smtp = smtplib.SMTP(emailhost, emailport)
#for Google connection
smtp.ehlo()
smtp.starttls()
smtp.login(emailuser, emailpass)
#end for Google connection
smtp.sendmail(emailfrom, emailto, msg.as_string())
smtp.quit()
