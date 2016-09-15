#Login And Connect To Inbox
import imaplib
import re
import email
import datetime
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('myusername@gmail.com', 'mypassword')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

#Getting Mail
result, data = mail.uid('search', None, "ALL") # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

#Parse(~translate) The Emails
email_message = email.message_from_string(raw_email)
print email_message['To']
print email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>
print email_message.items() # print all headers




#POSSIBLE SEARCHES

#Search for header
mail.uid('search', None, '(HEADER Subject "My Search Term")')
mail.uid('search', None, '(HEADER Received "localhost")')

#Search for emails since in the past day
import datetime
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))

#Limit by date, search for a subject, and exclude a sender
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date} HEADER Subject "My Subject" NOT FROM "yuji@grovemade.com")'.format(date=date))

#Fetches
result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')

#Fetch Multiple
result, data = mail.uid('fetch', '1938,2398,2487', '(X-GM-THRID X-GM-MSGID)')




#Use a regex to parse fetch results
result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')
re.search('X-GM-THRID (?P<X-GM-THRID>\d+) X-GM-MSGID (?P<X-GM-MSGID>\d+)', data[0]).groupdict()
# this becomes an organizational lifesaver once you have many results returned.
