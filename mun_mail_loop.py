from mun_mail_read import get_columns
from mun_mail_send import send_email

ids, emails = get_columns(r'C:\Users\ASUS\Downloads\BITSMUN Core Reviews (Responses).xlsx')

print(ids)
print(emails)
count=1
for i in range (len(ids)):
    text='Dear '+ids.iloc[i,0]+',\n\n'+'Thank you for your efforts'+'\n\n'+'Regards,\n'+'Your Secretariat\n'+'BITSMUN 2024'+'\nP.S.-Acche se kaam karte rehna nahi to socials lite ho jayega tum log ka\n'+'P.P.S.-Kuch kaam nahi kiya is saal, to ignore the above message\n'
    send_email('Subject', text, 'vineetkrishna.bitsmun@gmail.com', emails.iloc[i, 0], 'ohjj rttc xihf mqez')
    print('Sent '+ids.iloc[i,0]+' to ' + emails.iloc[i, 0])
    print(count)
    count+=1
    
