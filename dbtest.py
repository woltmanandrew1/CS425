import psycopg2
import classwork

def mainMenu():
            try:
                  print("Welcome to the ERP DBMS!\n\nMain Menu\n")
                  username = input("Please enter your username: ")
                  passwrd = input("Please enter your password: ")
                  employeeid = input("What is your employee id: ")
                  conn1 = psycopg2.connect(user = 'idcheck',
                                          password = 'gettheid3',
                                          host = '127.0.0.1',
                                          port = 8081,
                                          database = 'postgres')
                  #call one of the following menus after verifying login info
                  #call permisionCheck() to then call correspodning menu
                  classConnect = classwork.Connection()
                  classConnect.loginid = classConnect.getMaxID(conn1,'login','loginid')+1
                  conn = classConnect.loginIn(username, passwrd,employeeid)
                  role = classConnect.roleCheck(conn)
                  print(role)
                  if role == "admins" or role=="postgres":
                        admin_menu(classConnect, conn,employeeid)
                  elif role == "engineer":
                        engineer_menu(classConnect, conn,employeeid)
                  elif role == "sales":
                        sales_menu(classConnect, conn,employeeid)
                  elif role == "hr":
                        hr_menu(classConnect, conn,employeeid)
                  else:
                        print("if you're reading this, something went wrong, check 'mainMenu()' in 'dbtest.py'") 
            except KeyboardInterrupt:
                  classConnect.loginOut(conn)
            except:
                  pass

def admin_menu(classConnect, conn,employeeid):
      try:
            goBack = True
            while goBack == True:
                  valid_input = False
                  valid_input1 = False
                  print("\nSelect a menu (number): \n")
                  while valid_input == False: #loop until valid response
                        option = input("1. Users \n2. Tables \n3. Reports \n4. View Employees\n5. Quit\n") #prompt user for option
                        if option == "1":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Create user\n2. Update user\n3. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          goBack = False
                                          classConnect.newUser(conn)
                                    elif option1 == "2": #this is also for granting access to other users
                                          valid_input1 = True
                                          goBack = False
                                          classConnect.updateUser(conn)
                                    elif option1 == "3": #break out of current while loop and go to the first while loop
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option")
                        elif option == "2":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Update table\n2. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          goBack = False
                                          classConnect.newTable(conn)
                                    elif option1 == "2": 
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option")
                        elif option == "3":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Create report\n2. View report\n3. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          goBack = False
                                          invalid2 = True
                                          while invalid2 == True:
                                                print("Please select which report you would like to create\n")
                                                option2 = input("1. Revenue report\n2. Customer report\n3. Inventory report\n4. Expense report\n")
                                                if option2=='1':
                                                      invalid2 = False
                                                      classConnect.createTotalRevenue(conn)
                                                elif option2=='2':
                                                      invalid2 = False
                                                      classConnect.createCustomerPrediction(conn)
                                                elif option2=='3':
                                                      invalid2 = False
                                                      classConnect.createOrderInventory(conn)
                                                elif option2=='4':
                                                      invalid2 = False
                                                      classConnect.viewExpenseReport(conn)
                                                else:
                                                      tryAgain = input("Invalid input. Would you like to try again? (Y/N)")
                                                      if tryAgain != 'Y':
                                                            return
                                    elif option1 == "2":
                                          valid_input1 == True
                                          goBack = False
                                          invalid2 = True
                                          while invalid2 == True:
                                                print("Please select which report you would like to view\n")
                                                option2 = input("1. Revenue Report\n2. Customer Report\n3. Inventory Report\n4. Expense Report\n")
                                                if option2=='1':
                                                      invalid2 = False
                                                      classConnect.viewTotalRevenue(conn)
                                                elif option2=='2':
                                                      invalid2 = False
                                                      classConnect.viewCustomerPrediction(conn)
                                                elif option2=='3':
                                                      invalid2 = False
                                                      classConnect.viewOrderInventory(conn)
                                                elif option2=='4':
                                                      invalid2 = False
                                                      classConnect.viewExpenseReport(conn)
                                                else:
                                                      tryAgain = input("Invalid input. Would you like to try again? (Y/N)")
                                                      if tryAgain != 'Y':
                                                            return
                                    elif option1 == "3":#break out of current while loop and go to the first while loop
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option")
                        elif option == "4":
                              valid_input = True
                              classConnect.employeeInfo(conn,classConnect.roleCheck(conn))
                        elif option == "5":
                              print("Logging out...")
                              classConnect.loginOut(conn)
                              return
                        else:
                              print("Please choose a valid menu:")
      except KeyboardInterrupt:
                  classConnect.loginOut(conn)

def engineer_menu(classConnect, conn,employeeid):
      try:
            goBack = True
            while goBack == True:
                  valid_input = False
                  valid_input1 = False
                  print("\nSelect a menu (number): \n")
                  while valid_input == False: #loop until valid response
                        option = input("1. Design\n2. Model\n3. Inventory\n4. Employee Infromation\n5. Quit\n") #prompt user for option
                        if option == "1":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Create design\n2. View designs\n3. Update design\n4. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          classConnect.newDesign(conn)
                                    elif option1 == "2":
                                          valid_input1 = True
                                          classConnect.viewDesigns(conn)
                                    elif option1 == "3":
                                          valid_input1 = True
                                          classConnect.updateDesign(conn)
                                    elif option1 == "4":
                                          valid_input = False
                                          break
                                    else:
                                          valid_input1 = False
                        if option == "2":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Create Model\n2. View Models\n3. Update Model\n4. Delete Model\n5. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          classConnect.newModel(conn)
                                    elif option1 == "2":
                                          valid_input1 = True
                                          classConnect.viewModels(conn)
                                    elif option1 == "3":
                                          valid_input1 = True
                                          classConnect.updateModel(conn)
                                    elif option1 == "4":
                                          valid_input1 = True
                                          classConnect.deleteModel(conn)
                                    elif option1 == "5":
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option \n")
                        elif option == "3":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Update inventory\n2. View inventory\n3. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          classConnect.updateInventory(conn)
                                    elif option1 == "2":
                                          valid_input1 = True
                                          classConnect.viewInventory(conn)
                                    elif option1 == "3":
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option \n")
                        elif option == "4":
                              valid_input = True
                              classConnect.employeeInfo(conn, classConnect.roleCheck(conn))
                        elif option == "5":
                              print("Logging out...")
                              classConnect.loginOut(conn)
                              return
                        else:
                              print("Please choose a valid menu: \n")
      except KeyboardInterrupt:
                  classConnect.loginOut(conn)

def sales_menu(classConnect, conn,employeeid):
      try:
            goBack = True
            while goBack == True:
                  valid_input = False
                  valid_input1 = False
                  print("\nSelect a menu (number): \n")
                  while valid_input == False: #loop until valid response
                        option = input("1. Customers\n2. Orders\n3. Reports\n4. Quit\n") #prompt user for option
                        if option == "1":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Create customer\n2. Update customer\n3. View Customers\n4. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          classConnect.newCustomer(conn)
                                    elif option1 == "2":
                                          valid_input1 = True
                                          classConnect.updateCustomer(conn)
                                    elif option1 == "3":
                                          valid_input1 = True
                                          classConnect.viewCustomers(conn)
                                    elif option1 == "4":
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option \n")
                        elif option == "2":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Create order\n2. Update order\n3. Delete order\n4. View Orders\n5. Return to previous menu\n") #prompt user for option
                              
                                    if option1 == "1":
                                          valid_input1 = True
                                          classConnect.createOrder(conn)
                                    elif option1 == "2":
                                          valid_input1 == True
                                          classConnect.updateOrder(conn)
                                    elif option1 == "3":
                                          valid_input1 = True
                                          classConnect.deleteOrder(conn)
                                    elif option1 == "4":
                                          valid_input1 = True
                                          classConnect.viewOrders(conn)
                                    elif option1 == "5":
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option \n")
                        elif option == "3":
                              valid_input = True
                              classConnect.viewTotalRevenue(conn)
                        elif option == "4":
                              print("Logging out...")
                              classConnect.loginOut(conn)
                              return
                        else:
                              print("Please choose a valid menu: \n")
      except KeyboardInterrupt:
                  classConnect.loginOut(conn)

def hr_menu(classConnect, conn,employeeid):
      try:
            goBack = True
            while goBack == True:
                  valid_input = False
                  valid_input1 = False
                  print("\nSelect a menu (number): \n")
                  while valid_input == False: #loop until valid response
                        option = input("1. Employee information\n2. View total revenue report\n3. Quit\n") #prompt user for option
                        if option == "1":
                              valid_input = True
                              print("\nSelect an option (number): \n")
                              while valid_input1 == False: #loop until valid response
                                    option1 = input("1. Update employee\n2. View employees\n3. Return to previous menu\n") #prompt user for option
                                    if option1 == "1":
                                          valid_input1 = True
                                          goBack = False
                                          classConnect.updateEmployee(conn)
                                    elif option1 == "2":
                                          valid_input1 = True
                                          goBack = False
                                          classConnect.employeeInfo(conn,classConnect.roleCheck(conn))
                                          print("Got to the end")
                                    elif option1 == "3":
                                          valid_input = False
                                          break
                                    else:
                                          print("Please choose a valid option \n")
                        elif option == "2":
                              valid_input = True
                              classConnect.viewTotalRevenue(conn)
                        elif option == "3":
                              print("Logging out...")
                              classConnect.loginOut(conn)
                              return
                        else:
                              print("Please choose a valid menu: \n")
      except (KeyboardInterrupt, Exception) as error:
            print(error)
            classConnect.loginOut(conn)              

mainMenu()