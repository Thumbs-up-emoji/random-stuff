from mun_mail_read import get_columns
from mun_mail_send import send_email

ids, emails = get_columns(r'C:\Users\ASUS\Downloads\Untitled.xlsx')

print(ids)
print(emails)
count=1

for i in range (len(ids)):
    send_email('Subject', ids.iloc[i, 0], 'vineetkrishna.bitsmun@gmail.com', emails.iloc[i, 0], 'ohjj rttc xihf mqez')
    print('Sent '+ids.iloc[i,0]+' to ' + emails.iloc[i, 0])
    
