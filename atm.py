from tkinter import *
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import random
from datetime import date



#Initialization of database
mydb= mysql.connector.connect(
    host = "localhost",
    user="root",
    database = "atm_auth"

)
myCursor = mydb.cursor()
myCursor1 = mydb.cursor()



#creating main window
top = Tk()
w, h = top.winfo_screenwidth(), top.winfo_screenheight()
top.geometry("%dx%d+0+0" % (w, h))
img=Image.open("pin.jpg")
bac_img = ImageTk.PhotoImage(img)
background = Label(top, image=bac_img,bd=0)
background.pack()
#creating string variable objects for text inputs in create user
R1=StringVar ()
R2 = StringVar  ()
R3 = StringVar ()
R4 = StringVar ()
R5 = StringVar()
R6 = StringVar()
R7 = StringVar()
R8 = StringVar()
R9 = StringVar()
R10 = StringVar()



#main display for login into system
L1 = Label(top,text = "UserName")
L1.place(x=500,y=200)

E1 = Entry(top)
E1.place(x = 580,y = 200)

L2 = Label(top,text = "Password")
L2.place(x=500,y=240)

E2 = Entry(top,show="*")
E2.place(x=580,y=240)




def newWindow():
    #aquiring the username and password from the entry fields
    Username = E1.get()
    Password = E2.get()


    #fetching all values from the database and storing in temp_username as tuples
    myCursor.execute("SELECT * FROM authenticate")
    temp_username = myCursor.fetchall()

    for i in temp_username:
        #comparing the username and password retrieved from the entry boxes with username and password fileds from the the database
        if i[5]==Username and i[6]==Password:
            print("logged in")
            usr_name = i[5]
            cid=i[0]
            #creating a new window for user operations
            newWind = Tk()
            w, h = newWind.winfo_screenwidth(), newWind.winfo_screenheight()
            newWind.geometry("%dx%d+0+0" % (w, h))
            # img = Image.open("pin.jpg")
            # bac_img = ImageTk.PhotoImage(img)
            # background = Label(newWind, image=bac_img, bd=0)
            # background.pack()
            newWind.configure(bg='teal')

            def user_info():
                #Firing query for retriving information about user
                sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
                myCursor.execute(sql)
                Information = myCursor.fetchall()
                #traversing thorugh the tuple
                for j in Information:
                    #top.destroy()
                    print(j)
                    #Printing the information in desired format
                    name_label = Message(newWind, text="Available Balance: " + str(j[11]) + "")
                    name_label.place(x=20, y=10,width=120,height=150)


             #Button for Displaying the information of thr logged in user
            user_info_btn = Button(newWind,text="Balance Enquiry",command=user_info)
            user_info_btn.place(x=580,y=50)

            sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
            myCursor.execute(sql)
            Information = myCursor.fetchall()
            # traversing thorugh the tuple
            for j in Information:
                print(j)
                v1=j[11]
                # Printing the information in desired format
                # balance_disp_label = Label(newWind , text="Current Balance : {}" .format(v1))
                # balance_disp_label.place(x=10, y=10)

            def trans():
                #Firing query for retriving information about user
                sql = "SELECT t.tdate,t.type,t.amt,t.bal FROM transaction t,authenticate a WHERE t.id='" + str(cid) + "' AND a.id='"+str(cid)+"'"
                myCursor.execute(sql)
                Information = myCursor.fetchall()
                #traversing thorugh the tuple
                for j in Information:
                    #top.destroy()
                    print(j)

                    #Printing the information in desired format
                    name_label = Message(newWind, text=" Date : " + str(j[0]) + "\n Type : "+ str(j[1])+"\n Amount :"+ str(j[2]) +"\n Balance :"+ str(j[3])+"\n",relief=RAISED)
                    name_label.place(x=20, y=200,width=120,height=150)



             #Button for Displaying the information of thr logged in user
            tr_btn = Button(newWind,text="Transactions",command=trans)
            tr_btn.place(x=580,y=150)

            sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
            myCursor.execute(sql)
            Information = myCursor.fetchall()
            # traversing thorugh the tuple
            for j in Information:
                print(j)
                v1=j[10]
                # Printing the information in desired format
                # balance_disp_label = Label(newWind , text="Current Balance : {}" .format(v1))
                # balance_disp_label.place(x=10, y=10)



            def withDraw():
                withdraw = Tk()
                w, h = withdraw.winfo_screenwidth(), withdraw.winfo_screenheight()
                withdraw.geometry("%dx%d+0+0" % (w, h))
                withdraw.configure(bg='violet')

#                top.destroy()
                withDraw_Label = Label(withdraw,text="Please enter the amount to be withdrawn : ")
                withDraw_Label.place(x=20,y=50)

                withDraw_Entry = Entry(withdraw)
                withDraw_Entry.place(x=250,y=50)

                def withDrawal():
                    amount = withDraw_Entry.get()
                    int(amount)

                    sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
                    myCursor.execute(sql)
                    Information = myCursor.fetchall()
                    # traversing thorugh the tuple
                    for j in Information:
                        if int(amount) > int(j[11]):
                            messagebox.showinfo("Alert","You do not have sufficient balance \n Available Balance : {} ".format(j[11])).place()
                        else:
                            available_balance = int(j[11])
                            int(available_balance)
                            myid = j[0]
                            t = "withdraw"
                            today = date.today()

                            remaining_balance=int(j[11])-int(amount)
                            # str(remaining_balance)
                            print(remaining_balance)
                            sql1 = "INSERT INTO transaction(id, tdate, type, amt, bal) VALUES (%s,%s,%s,%s,%s)"
                            v = (myid, today, t, amount, remaining_balance)
                            myCursor1.execute(sql1, v)
                            mydb.commit()
                            sql="UPDATE authenticate SET Balance = '"+str(remaining_balance)+"' WHERE UserName='" + usr_name + "'"
                            myCursor.execute(sql)
                            mydb.commit()
                            sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
                            myCursor.execute(sql)
                            Information = myCursor.fetchall()
                            # traversing thorugh the tuple
                            for j in Information:
                                value = random.randint(0,50)

                                messagebox.showinfo("Bill Info","Bill no. {} \nYour current balance is : {}".format(value,j[11]))
                            withdraw.destroy()
                            top.destroy()

                withDraw_btn = Button(withdraw,text="Withdaw",command=withDrawal)
                withDraw_btn.place(x=50,y=100)

                

            withdraw_invoke_btn = Button(newWind,text="Withdraw Amount",command=withDraw)
            withdraw_invoke_btn.place(x=450,y=100)

        # else:
        #     print("Invalid process")

            def dep():
                d = Tk()
                w, h = d.winfo_screenwidth(), d.winfo_screenheight()
                d.geometry("%dx%d+0+0" % (w, h))
                d.configure(bg='steelblue')

                #top.destroy()
                dep_Label = Label(d, text="Please enter the amount to be deposited : ")
                dep_Label.place(x=20, y=50)

                dep_Entry = Entry(d)
                dep_Entry.place(x=250, y=50)

                def Dep():
                    amount1 = dep_Entry.get()
                    int(amount1)

                    sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
                    myCursor.execute(sql)
                    Information = myCursor.fetchall()
                    # traversing thorugh the tuple
                    for j in Information:

                            available_balance = int(j[11])
                            int(available_balance)
                            myid=j[0]
                            t="deposit"
                            today = date.today()
                            remaining_balance = int(j[11]) + int(amount1)
                            # str(remaining_balance)
                            print(remaining_balance)
                            sql1="INSERT INTO transaction(id, tdate, type, amt, bal) VALUES (%s,%s,%s,%s,%s)"
                            v=(myid,today,t,amount1,remaining_balance)
                            myCursor1.execute(sql1, v)
                            mydb.commit()
                            sql = "UPDATE authenticate SET Balance = '" + str(
                                remaining_balance) + "' WHERE UserName='" + usr_name + "'"
                            myCursor.execute(sql)
                            mydb.commit()
                            sql = "SELECT * FROM authenticate WHERE UserName='" + usr_name + "'"
                            myCursor.execute(sql)
                            Information = myCursor.fetchall()
                            # traversing thorugh the tuple
                            for j in Information:
                                value = random.randint(0, 50)

                                messagebox.showinfo("Bill Info",
                                                    "Bill no. {} \nYour current balance is : {}".format(value, j[11]))
                            d.destroy()
                            top.destroy()

                dep_btn = Button(d, text="Deposit", command=Dep)
                dep_btn.place(x=70, y=100)

            dep_invoke_btn = Button(newWind, text="Deposit Amount", command=dep)
            dep_invoke_btn.place(x=700, y=100)

        else:
            print("Invalid process")


#For Creating new user
def Create_User():
    #Creating new window and destroying the main window
    SignUp = Tk()
    w, h = SignUp.winfo_screenwidth(), SignUp.winfo_screenheight()
    SignUp.geometry("%dx%d+0+0" % (w, h))

    top.destroy()

    #labels and entry fields for filling up details
    L1 = Label(SignUp,text="Name: ")
    L1.place(x = 10, y = 10)

    E1 = Entry(SignUp,bd = 5,textvariable=R1)
    E1.place(x =140, y = 10 )
    Name = R1.get()
    R1.set(Name)

    L2 = Label(SignUp,text="Account Number")
    L2.place(x = 10,y = 40)

    E2 = Entry(SignUp,bd=5,textvariable=R2)
    E2.place(x= 140,y= 40)
    Account_No=R2.get()
    R2.set(Account_No)

    L3 = Label(SignUp,text = "Address")
    L3.place(x =10 , y = 70)

    E3 = Entry(SignUp,bd=5,textvariable=R3)
    E3.place(x= 140,y= 70)
    Address=R3.get()
    R3.set(Address)

    L4 = Label(SignUp,text = "Phone Number")
    L4.place(x =10 , y = 100)

    E4 = Entry(SignUp,bd=5,textvariable=R4)
    E4.place(x= 140,y= 100)
    Phone_No=R4.get()
    R4.set(Phone_No)

    L5 = Label(SignUp,text="User Name")
    L5.place(x=10,y=130)

    E5 = Entry(SignUp,bd=5,textvariable=R5)
    E5.place(x=140,y=130)
    Username=R5.get()
    R5.set(Username)

    L6 = Label(SignUp, text="Password")
    L6.place(x=10, y=160)


    E6 = Entry(SignUp, bd=5,textvariable=R6)
    E6.place(x=140, y=160)
    Password=R6.get()
    R6.set(Password)

    L7 = Label(SignUp, text="Bank Name")
    L7.place(x=10, y=190)

    E7 = Entry(SignUp, bd=5, textvariable=R7)
    E7.place(x=140, y=190)
    BankName = R7.get()
    R7.set(BankName)

    L8 = Label(SignUp, text="IFSC Code")
    L8.place(x=10, y=220)

    E8 = Entry(SignUp, bd=5, textvariable=R8)
    E8.place(x=140, y=220)
    IFSC_Code = R7.get()
    R8.set(IFSC_Code)

    L9 = Label(SignUp, text="Adhaar Number")
    L9.place(x=10, y=250)

    E9 = Entry(SignUp, bd=5, textvariable=R9)
    E9.place(x=140, y=250)
    Adhaar_no = R9.get()
    R9.set(Adhaar_no)

    L10 = Label(SignUp, text="PAN Number")
    L10.place(x=10, y=280)

    E10 = Entry(SignUp, bd=5, textvariable=R10)
    E10.place(x=140, y=280)
    PAN_no = R7.get()
    R10.set(PAN_no)


    def Add_User():
        #fetching the values from corresponding entry fields
        Name = E1.get()
        Account_No = E2.get()
        Address = E3.get()
        Phone_No=E4.get()
        UserName=E5.get()
        Password=E6.get()
        BankName=E7.get()
        IFSC_Code=E8.get()
        Adhaar_no=E9.get()
        PAN_no=E10.get()




        print(Name,Password)
        print("Hi")
        #firing query for inserting data into mysql
        sql = "INSERT INTO authenticate (Name,Account_No,Address,Phone_No,UserName,Password,BankName,IFSC_code,Adhaar_No,Pan_No,Balance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (Name,Account_No,Address,Phone_No,UserName,Password,BankName,IFSC_Code,Adhaar_no,PAN_no,20000)

        myCursor.execute(sql,val)
        mydb.commit()
        SignUp.destroy()

    #button for adding the user information to database
    SignUp_But = Button(SignUp,text="Create User",command=Add_User)
    SignUp_But.place(x=70,y=310)



#Buttons for logging in and adding new user
B1 = Button(top,text ="Login",command=newWindow)
B1.place (x=550,y=280)

B2 = Button(top,text="SignUP!",command = Create_User)
B2.place(x=600,y=280)



top.mainloop()
