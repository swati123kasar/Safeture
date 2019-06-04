import smtplib
import serial
ser=serial.Serial('COM6',9600)
arr=[]
arr1=[]
x=0

content = 'ACCIDENT DETECTED...EEEUUUUUUUU'
mail=smtplib.SMTP('smtp.gmail.com',587)

mail.ehlo()

mail.starttls()

mail.login('poojamane0101@gmail.com','manepuj@')



while x<10:
    t=ser.readline()
    z=int(t)
    print(z)
    if z>1000 :
        print("ACCIDENT DETECTED.")
        mail.sendmail('poojamane0101@gmail.com','swatikasar17@gmail.com',content)
        mail.close()

    if z<=40 and z>20:
        arr.append(z)
    x+=1
    #print(z)#x<5:
   # arr.append(ser.readline)
    #x+=1

print(arr)
for i in arr:
    if i<=30 and i>=25:
        #print("yes")
        arr1.append("yes")
    else:
        #print("no")
        arr1.append("no")

for j in arr1:
    if j=="no":
        print("BAD")
        break
    else:
        print("GOOD")
        break












