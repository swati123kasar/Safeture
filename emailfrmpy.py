import smtplib

content = 'ACCIDENT DETECTED...'
mail=smtplib.SMTP('smtp.gmail.com',587)

mail.ehlo()

mail.starttls()

mail.login('swatikasar17@gmail.com','sk27$9806')

mail.sendmail('swatikasar17@gmail.com','poojamane0101@gmail.com',content)

mail.close()

