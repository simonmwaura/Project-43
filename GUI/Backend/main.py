from lib.Certification import Certification
from lib.Client import Client
from lib.config import conn,cursor
from lib.Equipment import Equipment
from lib.Financials import Financials
from lib.Materials import Materials
from lib.Personnel import Personnel
from lib.Projects import Projects
from lib.Suppliers import Suppliers
import sys

def main_menu():
    print("|------------------------------------------------------|")
    print("|                      MAIN MENU                       |")
    print("|------------------------------------------------------|")
    print("|    1.Manage Client                                   |")
    print("|    2.Manage Certificates                             |")
    print("|    3.Manage Equipment                                |")
    print("|    4.Manage Financials                               |")
    print("|    5.Manage Materials                                |")
    print("|    6.Manage Personnel                                |")
    print("|    7.Manage Projects                                 |")
    print("|    8.Manage Suppliers                                |")
    print("|    9.Exit                                            |")
    print("|------------------------------------------------------|")

    choice=(input("\nEnter your choice: "))

    if choice =="1":
        return Client_operations()
    
    elif choice == "2":
        return Certificate_operations()
    
    elif choice == "3":
        return Equipment_operations()
    
    elif choice == "4":
        return Financials_operations()
    
    elif choice == "5":
        return Materials_operations()
    
    elif choice == "6":
        return Personnel_operations()

    elif choice == "7":
        return Projects_operations() 

    elif choice == "8":
        return Supplier_operations() 
    
    elif choice == "9":
        print("<-----Exiting the application----->")
        sys.exit()
    else:
        print("<-----Invalid input------>")    
    

def Client_operations():
    while True:
        print("|------------------------------------------------------|")
        print("|                      CLIENT MENU                     |")
        print("|------------------------------------------------------|")
        print("|    1.Add Client                                      |")
        print("|    2.Update Client                                   |")
        print("|    3.Fetch Client by Name                            |")
        print("|    4.Fetch all Clients                               |")
        print("|    5.Delete Client by Name                           |")
        print("|    6.Return to main menu                             |")
        print("|------------------------------------------------------|")

        choice = input("\n Enter your choice: ")

        client=Client()
        if choice=="1":
            name = input("Enter client name: ").strip().upper()
            email = input("Enter client email: ").strip()
            phone_number = input("Enter phone number (+254XXXXXXXXX): ").strip()
            identity_number = input("Enter national identity number: ").strip()

            client_id = client.create_client(name, email, phone_number, identity_number)
            print(f"\nClient created successfully! ID: {client_id}")

        elif choice=="2":
            old_name=input("Enter current client name: ").strip().upper()
            new_name = input("Enter new name: ").strip().upper() 
            new_email = input("Enter new email: ").strip() 
            new_phone_number = input("Enter new phone number (+254XXXXXXXXX): ").strip()  
            new_identity_number = input("Enter new identity number: ").strip() 
            
            Client.update_single_client(old_name, new_name, new_email, new_phone_number, new_identity_number)

            print(f"Client '{old_name}' updated to '{new_name}' successfully")

        elif choice=="3":
            fetch_name =input("Enter client name to fetch: ").strip().upper()
            client_data = client.fetch_single_client(fetch_name)
            if client_data:
                print("\nClient Details:")
                print(f"ID: {client_data[0]}")
                print(f"Name: {client_data[1]}")
                print(f"Email: {client_data[2]}")
                print(f"Phone: {client_data[3]}")
                print(f"National ID: {client_data[4]}")
            else:
                print("\nNo client found with that name")
        elif choice =="4":
            all_clients=client.fetch_all_clients()
            print("\n All Users \n")
            print("-" * 90)
            print(f"{'ID':<5}{'Name':<20}{'Email':<25}{'Phone':<15}{'National ID':<15}")
            print("-" * 90)
            for client_data in all_clients:
                print(f"{client_data[0]:<5}"  
                    f"{client_data[1]:<20}"  
                    f"{client_data[2]:<25}"  
                    f"{client_data[3]:<15}"  
                    f"{client_data[4]:<15}")  
            print("-" * 90)
            print(f"Total clients: {len(all_clients)}\n")
        
        elif choice == "5":
            delete_name =input("Enter client name to delete: ").strip().upper()
            delete_results=client.delete_single_client(delete_name)
            print(f"Client with name : {delete_results} deleted successfully.")
            
        elif choice == "6":
            return main_menu() 
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def Supplier_operations():
    while True:
            print("|------------------------------------------------------|")
            print("|                      SUPPLIERS MENU                  |")
            print("|------------------------------------------------------|")
            print("|    1.Add Supplier                                    |")
            print("|    2.Fetch single Supplier by id                     |")
            print("|    3.Update Supplier                                 |")
            print("|    4.Delete Supplier                                 |")
            print("|    5.Fetch all Suppliers                             |")
            print("|    6.Count suppliers                                 |")
            print("|    7.Return to main menu                             |")
            print("|------------------------------------------------------|")

            choice = input("\n Enter your choice: ")
            supplier= Suppliers()
            if choice=="1":
                Supplier_name = input("Enter Supplier name: ")
                Supplier_email = input("Enter Supplier email: ")
                Supplier_phone_number = input("Enter your phone number (+254 format): ")
                Supplier_identity_number = input("Enter your National Identity Number: ")
                Supplier_status = input("Enter the status of the suppliers AVAILABLE OPTIONS (Active,Inactive,Pending,Suspended):")
                Remaining_amount = input("Enter remaining balance (KES): ")
                Supplier_id = supplier.create_suppliers(Supplier_name, Supplier_email, Supplier_phone_number, Supplier_identity_number,Supplier_status,Remaining_amount) 
                print(f"\nSupplier with id {Supplier_id} was added successfully")

            elif choice=="2":
                Supplier_id =input("Enter Supplier ID to fetch: ")
                single_Supplier = supplier.fetch_single_supplier(Supplier_id)
                print(single_Supplier)    

            elif choice=="3":
                Supplier_id=input("Enter Supplier ID to update: ")
                Supplier_name = input("Enter new name: ")
                Supplier_email= input("Enter new email: ")
                Supplier_phone_number=input("Enter new phone number: ")
                Supplier_identity_number=input("Enter new identity number: ")
                Supplier_status = input("Enter  new status of  suppliers AVAILABLE OPTIONS ('Active','Inactive','Pending','Suspended'):")
                Remaining_amount = input("Enter new balance : ")

                Supplier_id=supplier.update_supplier_by_id(Supplier_id,Supplier_name, Supplier_email, Supplier_phone_number, Supplier_identity_number,Supplier_status,Remaining_amount)
                print(f"\n Supplier with id {Supplier_id} updated successfully")

            elif choice == "4":
                Supplier_id=input("Enter Supplier id to delete: ")
                delete_Supplier_id = supplier.delete_single_supplier(Supplier_id)

                print(f"Supplier with id {delete_Supplier_id} deleted successfully.")    

            elif choice =="5":
                all_Suppliers=supplier.fetch_all_supplier()
                print("\n All Suppliers \n")
                print(all_Suppliers)
            
            elif choice =="6":
                count_Suppliers=supplier.count_suppliers()
                print(f"Total number of suppliers : {count_Suppliers}")
                
            elif choice == "7":
                return main_menu() 
                
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

def Projects_operations():
    while True:
        print("|------------------------------------------------------|")
        print("|                     PROJECTS MENU                    |")
        print("|------------------------------------------------------|")
        print("|    1.Add Project                                     |")
        print("|    2.Fetch single Project                            |")
        print("|    3.Fetch single Project by Client id               |")
        print("|    4.Fetch all Projects                              |")
        print("|    5.Update Project                                  |")
        print("|    6.Delete Project                                  |")
        print("|    7.Count Projects                                  |")
        print("|    8.Count Projects by Client_id                     |")
        print("|    9.Return to main menu                             |")
        print("|------------------------------------------------------|")
        
        choice = input("\n Enter your choice: ")

def Personnel_operations():
    while True:
        print("|------------------------------------------------------|")
        print("|                     PERSONNEL MENU                   |")
        print("|------------------------------------------------------|")
        print("|    1.Add Personnel                                   |")
        print("|    2.Fetch single Personnel                          |")
        print("|    3.Fetch all Personnel                             |")
        print("|    4.Update Personnel                                |")
        print("|    5.Delete Personnel                                |")
        print("|    6.Count Personnel                                 |")
        print("|    7.Return to main menu                             |")
        print("|------------------------------------------------------|")
        
        choice = input("\n Enter your choice: ")

def Materials_operations():
    while True:
        print("|------------------------------------------------------|")
        print("|                     MATERIALS MENU                   |")
        print("|------------------------------------------------------|")
        print("|    1.Add Materials                                   |")
        print("|    2.Fetch single Material                           |")
        print("|    3.Fetch single Material by Supplier id            |")
        print("|    4.Fetch all Materials                             |")
        print("|    5.Update Materials                                |")
        print("|    6.Delete Materials                                |")
        print("|    7.Count Material                                  |")
        print("|    8.Count Materials by Supplier id                  |")
        print("|    9.Return to main menu                             |")
        print("|------------------------------------------------------|")
        
        choice = input("\n Enter your choice: ")

def Equipment_operations():
    while True:
        print("|------------------------------------------------------|")
        print("|                     EQUIPMENT MENU                   |")
        print("|------------------------------------------------------|")
        print("|    1.Add Equipment                                   |")
        print("|    2.Fetch single Equipment                          |")
        print("|    3.Fetch single Equipment by Supplier id           |")
        print("|    4.Fetch all Equipment                             |")
        print("|    5.Update Equipment                                |")
        print("|    6.Delete Equipment                                |")
        print("|    7.Count Equipment                                 |")
        print("|    8.Count Equipment by Supplier id                  |")
        print("|    9.Return to main menu                             |")
        print("|------------------------------------------------------|")
        
        choice = input("\n Enter your choice: ")

def Certificate_operations():
    while True:
        print("|------------------------------------------------------|")
        print("|                     CERTIFICATE MENU                 |")
        print("|------------------------------------------------------|")
        print("|    1.Add Certificate                                 |")
        print("|    2.Fetch single Certificate                        |")
        print("|    3.Fetch single Certificate by Personnel id        |")
        print("|    4.Fetch all Certificate                           |")
        print("|    5.Update Certificate                              |")
        print("|    6.Delete Certificate                              |")
        print("|    7.Count Certificate                               |")
        print("|    8.Count Certificate by Personnel id               |")
        print("|    9.Return to main menu                             |")
        print("|------------------------------------------------------|")
        
        choice = input("\n Enter your choice: ")

def Financials_operations():
    print("<-------------------Comming soon------------------->")

main_menu()     