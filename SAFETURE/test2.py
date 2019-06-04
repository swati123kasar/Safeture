import serial
ser=serial.Serial('COM4',9600)
arr=[]
arr1=[]
x=0

while x<10:
    t=ser.readline()
    z=int(t)
    print(z)
    if z<=40 and z>=20:
        arr.append(z)
    x+=1
    

print(arr)
for i in arr:
    if i<=29 and i>=25:
        arr1.append("yes")
    else:
        arr1.append("no")

for j in arr1:
    if j=="no":
        print("BAD")
        break
    else:
        print("GOOD")
        break








