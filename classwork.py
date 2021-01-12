import psycopg2
import psycopg2.sql
import sys
from psycopg2.extensions import AsIs
from psycopg2 import sql
import datetime
from prettytable import PrettyTable

class Connection:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "8081"
        self.database = "postgres"
        self.loginid = 0

    #Login/out function calls
    def loginIn(self,usrName,Pasword,employeeid):
        try:
            conn = psycopg2.connect(user = usrName,
                                    password = Pasword,
                                    host = self.host,
                                    port = self.port,
                                    database = self.database)
            myCursor = conn.cursor()
            date = datetime.datetime.now().date()
            time = datetime.datetime.now().time()
            role = self.roleCheck(conn)
            print("Login ID: ", self.loginid)
            myCursor.execute("Insert into login values (%s,%s,%s,%s,%s,%s,%s) ", (self.loginid,role,'None',time,employeeid,date,'None'))
            conn.commit()
            return conn
        except(Exception, psycopg2.Error) as error:
            print ("Error while connecting to PostgreSQL", error)
            return
    
    def loginOut(self,conn):
        myCursor = conn.cursor()
        outdate = datetime.datetime.now().date()
        outtime = datetime.datetime.now().time()
        myCursor.execute("update login set (logouttime,logoutdate)=(%s,%s) where loginid = %s",(outtime,outdate,self.loginid))
        conn.commit()
        conn.close()
        print("PostgeSQL connection is closed.")
        return

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #User function calls
    def newUser(self,conn):
        try:
            myCursor = conn.cursor()
            invalid=True
            while(invalid):
                usrName = input("Enter a username: ")
                Password = input("Enter a password: ")
                confPassword = input("Confirm the password: ")
                if Password == confPassword:
                    try:
                        #manually scrub username for errors- special case
                        myCursor.execute("Create user %s with password %s", (AsIs(usrName),Password, )) #(AsIs(usrName), Pasword, ))
                        conn.commit()
                        userType = input("What type user is this user: ")
                        myCursor.execute("Grant insert,update on login to %s",(AsIs(usrName),))
                        conn.commit()
                        myCursor.execute("Grant %s to %s", (AsIs(userType),AsIs(usrName)))
                        conn.commit()
                        print("New User has been added")
                        print("New user: %s Password: %s" % (usrName, Password))
                        self.newEmployee(conn)
                        invalid=False
                    except(Exception,psycopg2.Error) as error:
                        if error == 42710: #User does not exist 
                            print("User already exist, try a new username")
                        else:
                            print("Error : ", str(error))
                            conn.commit()
                else:
                    print("Passwords do not match, please try again")
            print("User created successfully!")
        except KeyboardInterrupt:     
            self.loginOut(conn)

    def updateUser(self,conn):
        valid=False
        try:
            myCursor = conn.cursor()
            while(valid !=True):
                usrName = input("Enter a username you want to update: ")
                newPasword = input("Enter a password: ")
                confnewPassword = input("Confirm the password: ")
                
                if newPasword == confnewPassword:                        
                    try:
                        myCursor.execute("Alter user %s with password %s", (AsIs(usrName),newPasword))
                        conn.commit()
                        userType = input("What type of user is this user: ")
                        myCursor.execute("Grant %s on %s to %s", (AsIs(userType),self.database,AsIs(usrName)))
                        conn.commit()
                        print("New User has been added")
                        valid=True
                    except(Exception,psycopg2.Error) as error:
                        valid=False
                        if error == 42704:
                            print("User does not exit")
                        else:
                            print("Error %s" % error)
                else:
                    print("Password did not match")
                    valid=False
                print("User updated successfully!")
        except KeyboardInterrupt:     
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Customers function calls
    def newCustomer(self,conn):
        try:
            myCursor = conn.cursor()
            fName = input("Enter First Name: ")
            lName = input("\nEnter Last Name: ")
            myCursor.execute("select * from customer where firstName = %s and lastName = %s", (fName, lName))
            conn.commit()
            duplicateName = myCursor.fetchall() #if this list is empty then the customer has not been added yet
            if duplicateName:
                ques = input("Customer with that name already exists. Is this a different customer with the same name? (Y/N)")
                if ques.lower() == "y":
                    cId = self.getMaxID(conn,'customer','customerid')+1
                    myCursor.execute("Insert into Customer (customerid,firstname,lastname) values (%s,%s,%s)", (cId, fName,lName))
                    conn.commit()
                else:
                    print("Exiting...")
            else:
                cId = self.getMaxID(conn,'customer','customerid')+1 
                myCursor.execute("Insert into Customer (customerid,firstname,lastname) values (%s,%s,%s)", (cId, fName,lName))
                conn.commit()
            print("Customer created successfully!")
        except KeyboardInterrupt:     
            self.loginOut(conn)
    def updateCustomer(self,conn):
        try:
            myCursor = conn.cursor()
            invalid = True
            while invalid == True:
                confirmCId = input("Please enter the ID of the customer you want to update: ")
                myCursor.execute("select * from Customer where customerId = %s", (confirmCId))
                idExists = myCursor.fetchall() #list of that customerId, should not be empty
                if idExists:
                    invalid = False
                else:
                    tryAgain = input("Customer ID does not exist. Would you like to try another ID? (Y/N)")
                    if tryAgain.lower() != "y":                        
                        return
            fName = input("\nEnter new First Name: ")
            lName = input("\nEnter new Last Name: ")
            myCursor.execute("select * from customer where firstName = %s and lastName = %s", (fName, lName))
            conn.commit()
            duplicateName = myCursor.fetchall() #if this list is empty then the customer has not been added yet
            if duplicateName:
                ques = input("Customer with that name already exists. Is this a different customer with the same name? (Y/N)")
                if ques.lower() == "y":
                    myCursor.execute("update Customer set firstName = %s, lastName = %s where customerId = %s", (fName, lName, confirmCId))
                    conn.commit()
                else:
                    print("Exiting...")
            else:
                myCursor.execute("update Customer set firstName = %s, lastName = %s where customerId = %s", (fName, lName, confirmCId))
                conn.commit()
            print("Customer updated successfully!")
        except KeyboardInterrupt:     
            self.loginOut(conn)
    def viewCustomers(self,conn):
        try:
            table = PrettyTable(['Customer ID', 'First Name', 'Last Name'])
            myCursor = conn.cursor()
            myCursor.execute("select * from Customer")
            allCust = myCursor.fetchall()
            for i in range(len(allCust)):
                table.add_row([allCust[i][0], allCust[i][1], allCust[i][2]])
            print(table)
        except KeyboardInterrupt:     
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Model function calls
    def newModel(self,conn):
        try:
            myCursor = conn.cursor()
            invalid = True
            while invalid == True:
                dsnNmbr = input("Please enter the design ID of the design that you would like to make a model and add to the inventory: ")
                myCursor.execute("select designid from design where designid = %s", (dsnNmbr))
                doesExist = myCursor.fetchall()
                if doesExist:
                    invalid = False
                else:
                    tryAgain = input("Invalid design ID. Would you like to try another design ID? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
            name = input("Please enter a name for this model: ")#needs error checking
            cost = input("Please enter how much this item cost to manufacture: ")
            price = input("Please enter how much this item will sell for: ")
            time = input("Please enter how long it took to manufacturer this model in days: ")
            category = input("Please enter a category for this model: ")
            quantity = input("Please enter a quantity for this model: ")
            invId = self.getMaxID(conn,'inventory','inventoryid')+1
            myCursor.execute("insert into Model values (%s, %s, %s, %s)", (name, cost, doesExist[0], time))
            conn.commit()
            myCursor.execute("insert into inventory (inventoryId, saleprice, category, modelname, quantity) values (%s, %s, %s, %s, %s)", (invId, price, category, name, quantity))
            conn.commit()
            print("Model successfully added!")
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def updateModel(self, conn):
        try:
            myCursor = conn.cursor()
            invalid=True
            while(invalid):
                try:
                    id=input("Please enter the name of the model: ")
                    myCursor.execute("Select modelname from model where modelname=%s", (id, ))
                    newCost=input("Please enter the new cost of the model: ") #error checking
                    newLead=input("Please enter the new lead time: ")
                    sql="UPDATE model SET costmodel=%s, leadtime=%s WHERE modelname=%s"
                    myCursor.execute(sql, (newCost, newLead, id,))
                    conn.commit() #should include after all executions
                    invalid=False

                except(KeyboardInterrupt,psycopg2.Error)as error:
                    print("Error:",error)
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def deleteModel(self,conn):
        try:
            invalid = True
            myCursor = conn.cursor()
            while invalid == True:
                delModel = input("What model would you like to delete: ")
                desId = input("What is the design ID of this model: ")
                myCursor.execute("select modelname from model where designid=%s and modelname=%s", (desId, delModel))
                confirm = myCursor.fetchall()
                if confirm:
                    invalid = False
                else:
                    tryAgain = input("Model doesn't exist. Would you like to try again? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
            myCursor.execute("delete from model where designid = %s and modelname = %s", (desId, delModel))
            print("Model %s has been deleted", (delModel))
            conn.commit()
        except KeyboardInterrupt:     
            self.loginOut(conn)

    def viewModels(self,conn):
        try:
            table = PrettyTable(['Model Name', 'Cost Model', 'Design ID', 'Lead Time'])
            myCursor = conn.cursor()
            myCursor.execute("select * from Model")
            allMod = myCursor.fetchall()
            for i in range(len(allMod)):
                table.add_row([allMod[i][0], allMod[i][1], allMod[i][2], allMod[i][3]])
            print(table)
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    

    #Design function calls- verify why the double employee id check
    def newDesign(self,conn):
        try:
            myCursor = conn.cursor()
            invalidemp = True
            while(invalidemp):
                employeeID = input("Enter your employee ID: ")
                try:
                    empCheck = myCursor.execute("Select employeeid from employee where employeeid = %s", employeeID)
                    conn.commit()
                    invalidemp = False
                except(Exception, psycopg2.Error) as error:
                    print(error)
            invalid=True
            while(invalid):
                designid = self.getMaxID(conn,'design','designid')+1
                try:
                    designrev = input("Enter the revision: ")
                    myCursor.execute("Insert into design values (%s,%s,%s)", (designid,employeeID,designrev))
                    conn.commit()
                    return

                except(Exception, psycopg2.Error) as error:
                    print(error)
                    invalid=True
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)
                
    def updateDesign(self,conn):
        
        try:
            myCursor = conn.cursor()
            invalidDesign = True
            while(invalidDesign):
                designUp = input("What design are you updating: ")
                try:
                    designCheck = myCursor.execute("Select designrev from design where designid = %s", designUp)
                    Rev = myCursor.fetchone()
                    newRev = Rev[0]+1
                    myCursor.execute("Update design set designrev = %s where designid = %s",(newRev,designUp))
                    conn.commit()
                    invalidDesign = False
                except(Exception, psycopg2.Error) as error:
                    print(error)           
            return
            
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)
    
    def viewDesigns(self,conn):
            try:
                table = PrettyTable(['Design ID', 'Employee ID', 'Design Revisions'])
                myCursor = conn.cursor()
                myCursor.execute("select * from Design")
                allDes = myCursor.fetchall()
                for i in range(len(allDes)):
                    table.add_row([allDes[i][0], allDes[i][1], allDes[i][2]])
                print(table)
            except (KeyboardInterrupt,psycopg2.Error):     
                self.loginOut(conn)        
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Employee function calls
    def newEmployee(self,conn):
        try:
            myCursor = conn.cursor()
            employeeid = self.getMaxID(conn,'employee','employeeid')+1
            firstname = input("Enter the Employees first mame: ")
            lastname = input("Enter the Employees last name: ")
            ssn = input("Enter the Employees ssn: ")
            paytype = input("Enter the Employees paytype: ")
            jobtype = input("Enter the Employees job type: ")
            salary = input("Ennter the Employees salary: ")
            myCursor.execute("Insert into employee (employeeid,firstname,lastname,ssn,paytype,jobtype,salary) values (%s,%s,%s,%s,%s,%s,%s)", (employeeid,firstname,lastname,ssn,paytype,jobtype,salary))
            print("employee created successfully, employee id: %s" % (employeeid))
            conn.commit()
            return
        except(KeyboardInterrupt, Exception, psycopg2.Error) as error:
            print(error)     
            classConnect.loginOut(conn)

    def updateEmployee(self,conn):
        try:
            myCursor = conn.cursor()
            invalid = True
            invalid1 = True
            while invalid == True:
                eId = input("What is the employee ID of the employee you want to update:")
                myCursor.execute("select employeeid from employee where employeeid = %s", (eId))
                eIdTuple = myCursor.fetchone()
                if eIdTuple:
                    invalid = False
                else:
                    tryAgain = input("Invalid employee ID. Would you like to try another ID? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
            change = input("Select an option (number):\n1. Change name\n2. Change pay type\
                            \n3. Change job type\n4. Change salary: ")
            while invalid1 == True:
                if change == "1":
                    invalid1 = False
                    fName = input("\nEnter new First Name: ")
                    lName = input("\nEnter new Last Name: ")
                    myCursor.execute("update Employee set firstName = %s, lastName = %s where employeeid = %s",
                                    (fName, lName, eId))
                    conn.commit()
                elif change == "2":
                    invalid1 = False
                    ptype = input("Enter new pay type (hourly or salary): ")
                    myCursor.execute("update Employee set paytype = %s where employeeid = %s", (ptype, eId))
                elif change == "3":
                    invalid1 = False
                    jtype = input("Enter new job type (Sales, Engineer, HR, Admin): ")
                    myCursor.execute("update Employee set jobtype = %s where employeeid = %s", (jtype, eId))
                elif change == "4":
                    invalid1 = False
                    newSalary = input("Enter new salary (hourly rate if hourly pay type): ")
                    myCursor.execute("update Employee set salary = %s where employeeid = %s", (newSalary, eId))
                else:
                    print("Please choose a valid option")
                conn.commit()
                print("Update successful!")
        except (Exception, KeyboardInterrupt) as error:     
           print(error)
           self.loginOut(conn)
            

    def employeeInfo(self,conn,jobtype):
        try:
            print("in here")
            myCursor = conn.cursor()
            if jobtype == "engineer":
                table = PrettyTable(['Fist Name', 'Last Name', 'Job Type'])
                myCursor.execute("select * from engineeremployeeview")
                employees = myCursor.fetchall()
                for i in range(len(employees)):
                    table.add_row([employees[i][0], employees[i][1], employees[i][2]])
                print(table)
            elif jobtype == "postgres":
                table = PrettyTable(['Employee ID', 'First Name', 'Last Name', 'Social Security Number', 'Pay Type', 'Job Type', 'Salary'])
                myCursor.execute("select * from employee")
                employees = myCursor.fetchall()
                for i in range(len(employees)):
                    table.add_row([employees[i][0], employees[i][1], employees[i][2], employees[i][3], employees[i][4], employees[i][5], employees[i][6]])
                print(table)           
            else:
                table = PrettyTable(['Employee ID', 'First Name', 'Last Name', 'Pay Type', 'Job Type'])
                myCursor.execute("select * from hremployeeview")
                employees = myCursor.fetchall()
                for i in range(len(employees)):
                    table.add_row([employees[i][0], employees[i][1], employees[i][2], employees[i][3], employees[i][4]])
                print(table)
        except (Exception, KeyboardInterrupt)as error: 
            print(error)    
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Przmek
    #Report function calls
    def createTotalRevenue(self, conn): #Neeeds testing
        #total revenue from sale, associate employee and customer
        try:
            myCursor=conn.cursor()
            sql="create or replace view total_revenue as select employeeid, customerid, sum(saleprice) from orders group by employeeid, customerid;"
            myCursor.execute(sql)
            conn.commit()
            return
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def createCustomerPrediction(self, conn): #Neeeds testing
        #Customer model bought and quantity to make prediction and understand trending
        try:
            myCursor=conn.cursor()
            sql= "create or replace view customer_prediction as select orders.customerid, inventory.modelname, count(orders) from orders, inventory group by customerid, modelname;"
            myCursor.execute(sql)
            conn.commit()
            return
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def createOrderInentory(self, conn): #Neeeds testing
        #For each order, the associated parts and available inventory
        try:
            myCursor=conn.cursor()
            sql="create or replace view parts as select orders.ordernumber, inventory.modelname, inventory.quantity from orders inner join inventory on orders.inventoryid=inventory.inventoryid;"
            myCursor.execute(sql)
            conn.commit()
            return
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def viewExpenseReport(self, conn): #Neeeds testing
        #Expense report, employee showing salary, bonus expense and part cost
        try:
            myCursor=conn.cursor()
            modelCostQuery="select sum(costmodel) from model"
            salaryCostQuery="select sum(employee.salary) from employee where employee.paytype= 'salary'"
            hourlyCostQuery="select sum(employee.salary * 40 * 52) from employee where employee.paytype= 'hourly'"

            myCursor.execute(modelCostQuery)
            modelCost=list(list(myCursor.fetchall())[0])[0]
            print("cost for models is: ")
            print(modelCost)

            myCursor.execute(salaryCostQuery)
            salaryCost=list(list(myCursor.fetchall())[0])[0]
            print("cost for the salary employee is: ")
            print(salaryCost)

            myCursor.execute(hourlyCostQuery)
            hourlyCost=list(list(myCursor.fetchall())[0])[0]
            print("cost for the hourly employee's working 40 hour workweeks 52 weeks a year: ")
            print(hourlyCost)

            print("Total cost of expenses $%s" % (salaryCost+modelCost+hourlyCost))
            return
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def viewTotalRevenue(self,conn): #Neeeds testing
        try:
            print("TotalRevenue")
            table = PrettyTable(['Employee ID', 'Customer ID', 'Total Sales'])
            myCursor = conn.cursor()
            myCursor.execute("select * from total_revenue")
            allRev = myCursor.fetchall()
            for i in range(len(allRev)):
                table.add_row([allRev[i][0], allRev[i][1], allRev[i][2]])
            print(table)
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def viewCustomerPrediction(self,conn): #Neeeds testing
        try:
            table = PrettyTable(['Customer ID', 'Model Name', 'Count'])
            myCursor = conn.cursor()
            sql = "select * from customer_prediction"
            myCursor.execute(sql)
            custPred=myCursor.fetchall()
            for i in range(len(custPred)):
                table.add_row([custPred[i][0], custPred[i][1], custPred[i][2]])
            print(table)
        except (KeyboardInterrupt, Exception) as error:
            print(error)     
            self.loginOut(conn)



    def viewOrderInventory(self,conn): #Neeeds testing
        try:
            table = PrettyTable(['Order Number', 'Model Name', 'Quantity'])
            myCursor = conn.cursor()
            sql = "select * from parts"
            myCursor.execute(sql)
            ordInv=myCursor.fetchall()
            for i in range(len(ordInv)):
                table.add_row([ordInv[i][0], ordInv[i][1], ordInv[i][2]])
            print(table)
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Abdallah
    #Table function calls
    def updateTable(self, conn):
        #to prompt for table name
        try:
            myCursor = conn.cursor()
            invalid = True
            myCursor.execute("select table_name from information_schema.tables where table_schema = 'public'")
            tblNames = myCursor.fetchall() #list of all tables and views
            while invalid == True:
                tblName = input("Please enter the name of the table: ")
                for i in range(len(tblNames)):
                    tables= tblNames[i][0]
                    if tblName == tables:
                        invalid = False
                        correctTable = str(tables)
                    else:
                        continue
            print(correctTable)
            #to list all columns in that table
            myCursor.execute("select column_name from information_schema.columns where table_schema = 'public' and table_name = %s", (correctTable,))
            cols = myCursor.fetchall() #list of tuples i.e. [(employeeId), (firstName)...(salary)]

            #to do an operation on columns of table
            print("Please select an option (number):\n1. Rename column\n2. Add coulumn\n3. Delete column")
            option = input("Please select and option:")
            invalid = True
            while invalid == True:
                if option == "1":
                    invalid = False
                    invalid1 = True
                    while invalid1 == True:
                        col = input("Please enter the name of the column you want to rename: ")
                        for i in range(len(cols)):
                            columns = cols[i][0]
                            if col == columns:
                                invalid1 = False
                                correctCol = str(columns)
                            else:
                                continue
                        if invalid1 == True:
                            print(correctCol)
                            tryAgain = input("Column doesn't exist. Would you like to try another name? (Y/N)")
                            if tryAgain.lower() != "y":
                                return
                    newCol = input("Please enter the new column name: ")
                    myCursor.execute("alter table %s rename column %s to %s", (AsIs(correctTable), AsIs(correctCol), AsIs(newCol)))
                    conn.commit()
                elif option == "2":
                    invalid = False
                    invalid1 = True
                    while invalid1 == True:
                        col = input("Please enter the name of the column you want to add: ")
                        if col not in cols:
                            invalid1 = False
                        else:
                            tryAgain = input("Column already exists. Would you like to try another name? (Y/N)")
                            if tryAgain.lower() != "y":
                                return
                    print("Please choose the data type (number):\n1. String\n2. Int")
                    prompt = input("Please select and option:")
                    if prompt == "1":
                        colType = 'varchar(50)'
                    elif prompt == "2":
                        colType = 'int4'
                    myCursor.execute("alter table %s add column %s %s", (tblName, col, colType))
                elif option == "3":
                    invalid = False
                    invalid1 = True
                    while invalid1 == True:
                        col = input("Please enter the name of the column you want to delete: ")
                        if col in cols:
                            invalid1 = False
                        else:
                            tryAgain = input("Column doesn't exist. Would you like to try another name? (Y/N)")
                            if tryAgain.lower() != "y":
                                return
                    myCursor.execute("alter table %s drop column %s", (tblName, col))
                else:
                    tryAgain = input("Invalid input. Would you like to try again? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
        except KeyboardInterrupt:     
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Inventory function calls
    def viewInventory(self,conn):
        try:
            table = PrettyTable(['Inventory ID', 'Sale Price', 'Category', 'Model Name', 'Quantity'])
            myCursor = conn.cursor()
            myCursor.execute("select * from Inventory")
            allInv = myCursor.fetchall()
            print
            for i in range(len(allInv)):
                table.add_row([allInv[i][0], allInv[i][1], allInv[i][2], allInv[i][3], allInv[i][4]])
            print(table)
        except (KeyboardInterrupt,psycopg2.Error) as error: 
            print(error)    
            self.loginOut(conn)

    def updateInventory(self,conn):
        try:
            myCursor = conn.cursor()
            valid_input = False
            while valid_input == False:
                print("Update Inventory Menu:")
                print("1. Update Quantity \n 2. Remove Item")
                menuSelect = input("Please select and option:")
                if menuSelect == "1":
                    valid_input = True
                    inventoryid = input("What inventory ID would you like to update: ")
                    invenid = myCursor.execute("select inventoryid from inventory where inventoryid = %s",inventoryid)
                    inventvals = myCursor.fetchone()[0]
                    if inventvals:
                        newQuantity = input("What is the updated quantity: ")
                        myCursor.execute("update inventory set quantity = %s where inventoryid = %s", (newQuantity,inventoryid))
                        conn.commit()
                        return
                elif menuSelect == "2":
                    valid_input = True
                    inventoryid = input("What inventory ID would you like to remove: ")
                    invenid = myCursor.execute("select inventoryid from inventory where inventoryid = %s",inventoryid)
                    inventvals = myCursor.fetchone()[0]
                    if inventvals:
                        myCursor.execute("delete from inventory where inventoryid = %s", inventoryid)
                        conn.commit()
                        return
                else:
                    tryAgain = input("Invalid input. Would you like to try again? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
        except (KeyboardInterrupt,psycopg2.Error)as error: 
            print(error)    
            self.loginOut(conn)



#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



    #Order function calls
    def createOrder(self,conn):
        try:
            myCursor = conn.cursor()
            ordernumber = getMaxID(conn,'order','ordernumber')+1
            custumerid = input("Enter the custumers ID number: ")
            custIdCheck = myCursor.execute("select custumerid from customer where customerid = %s",custumerid)
            custvals = myCursor.fetchall()
            if custvals:
                employeeid = input("Enter your employee ID number: ") 
                inventoryid = input("Enter the inventory ID you would like to purchase: ")
                myCursor.execute("select quantity from inventory where inventoryid = %s",inventoryid)
                checkInventory = myCursor.fetchone()[0]
                if checkInventory > 0:
                    myCursor.execute("select saleprice from inventory where inventoryid = %s",inventoryid)
                    saleprice = myCursor.fetchone()[0]
                    myCursor.execute("Insert into orders (ordernumber,customerid,employeeid,saleprice,inventoryid) values (%s,%s,%s,%s,%s)", (ordernumber, customerid, employeeid, saleprice, inventoryId))
                    conn.commit()
                    myCursor.execute("Update inventory set inventory = %s where inventoryid = %s",
                                    (checkInventory-1,inventoryid))
                    conn.commit()
            return
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)
    def updateOrder(self,conn):
        try:

            invalid = True
            while invalid == True:
                myCursor = conn.cursor()
                orderid = input("What is your order number: ")
                checkOrder = myCursor.execute("select ordernumber from orders where ordernumber = %s", orderid)
                checkOrderId = str(myCursor.fetchone()[0])
                if orderid == checkOrderId:
                    invalid = False
                    newInventoryId = input("What inventory ID would you like to change your order to: ")
                    myCursor.execute("select inventoryid from orders where ordernumber = %s", orderid)
                    oldInventoryId = str(myCursor.fetchone()[0])
                    myCursor.execute("select quantity from inventory where inventoryid = %s", oldInventoryId)
                    oldInventoryQuantity = int(myCursor.fetchone()[0])
                    myCursor.execute("select quantity from inventory where inventoryid = %s",newInventoryId)
                    checkInventory = int(myCursor.fetchone()[0])
                    myCursor.execute("select saleprice from inventory where inventoryid = %s",newInventoryId)
                    saleprice = list(myCursor.fetchone())[0]
                    if checkInventory > 0:
                        myCursor.execute("update inventory set quantity = %s where inventoryid = %s", (str(checkInventory-1),newInventoryId))
                        conn.commit()
                        myCursor.execute("update inventory set quantity = %s where inventoryid = %s", (str(oldInventoryQuantity+1),oldInventoryId))
                        conn.commit()
                        myCursor.execute("update orders set inventoryid = %s, saleprice=%s where ordernumber = %s", (newInventoryId,saleprice,orderid))
                        conn.commit()
                else:
                    tryAgain = input("Order doesn't exit. Would you like to try another order number? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def deleteOrder(self,conn):
        try:
            myCursor = conn.cursor()
            invalid = True
            while invalid == True:
                ordNum = input("Please enter the Order number: ")
                myCursor.execute("select ordernumber from orders where ordernumber = %s", ordNum)
                confirm = myCursor.fetchall()
                if confirm:
                    invalid = False
                else:
                    tryAgain = input("Order doesn't exist. Would you like to try again? (Y/N)")
                    if tryAgain.lower() != "y":
                        return
            myCursor.execute("delete from orders where ordernumber = %s", ordNum)
            print("Order number %s has been deleted", ordNum)
            conn.commit()
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

    def viewOrders(self,conn):
        try:
            table = PrettyTable(['Order Number', 'Customer ID', 'Employee ID', 'Sale Price', 'Inventory'])
            myCursor = conn.cursor()
            myCursor.execute("select * from orders")
            orders = myCursor.fetchall()
            for i in range(len(orders)):
                table.add_row([orders[i][0], orders[i][1], orders[i][2], orders[i][3], orders[i][4]])
            print(table)
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    #Useful functions
    def getMaxID(self,conn,table,column):
        try:
            myCursor = conn.cursor()
            myCursor.execute("select max(%s) from %s", (AsIs(column),AsIs(table)))
            maxID = myCursor.fetchone()
            if maxID:
                return maxID[0]
            return 1
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)
    
 
    def roleCheck(self, conn):
        try:
            cur = conn.cursor()
            cur.execute('''SELECT current_user;''')
            rows=cur.fetchall()
            currentUser=rows[0]  #grab username
            
            query="SELECT rolname FROM pg_roles WHERE pg_has_role( (%s), oid, 'member');" #see which role the user has
            cur.execute(query, currentUser)
            rows=cur.fetchall()
            roleType=[]
            for i in range(len(rows)-1):
                    roleType.append(''.join(rows[i]))
            #print(roleType) all roles including inherited types, excludes name

            #assume that emplyees can't have more than one role (not including inherited)
            return roleType[len(roleType)-1] #the last role will contain the actual role of the user


            conn.commit()
        except (KeyboardInterrupt,psycopg2.Error):     
            self.loginOut(conn)