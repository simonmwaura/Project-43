# from lib.config import Database
from lib.Client import Client
from lib.config import conn,cursor
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
        print("|    3.Fetch Client by id                              |")
        print("|    4.Fetch all Clients                               |")
        print("|    5.Delete Client                                   |")
        print("|    6.Return to main menu                             |")
        print("|------------------------------------------------------|")

        choice = input("\n Enter your choice: ")

        client=Client()
        if choice=="1":
            Client_name = input("Enter your name: ")
            Client_email = input("Enter your email: ")
            Client_phone_number = input("Enter your phone number: ")
            Client_identity_number = input("Enter your identity number: ")
            Client_id = client.create_client(Client_name, Client_email, Client_phone_number, Client_identity_number)
            print(f"\nClient with id {Client_id} was added successfully")

        elif choice=="2":
            Client_id=input("Input the client id that you want to update: ")
            Client_name = input("Input the new client name: ")
            Client_email= input("Input the new client email: ")
            Client_phone_number=input("Input the new client phone number: ")
            Client_identity_number=input("Input the new client identity number: ")

            Client_id=Client.update_single_client(Client_name, Client_email, Client_phone_number, Client_identity_number)
            print(f"\n Client with id {Client_id} updated successfully")

        elif choice=="3":
            Client_id =input("Enter client id to fetch: \n")
            single_client = client.fetch_single_client(Client_id)
            print(single_client)

        elif choice =="4":
            all_clients=client.fetch_all_clients()
            printf=("\n All Users \n")
            print(all_clients)
        
        elif choice == "5":
            Client_id=input("Enter client id to delete: ")
            deleted_client_id=client.delete_single_user(Client_id)
            print(f"Client with id {deleted_client_id} deleted successfully.")
            
        elif choice == "6":
            return main_menu() 
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

main_menu()     

