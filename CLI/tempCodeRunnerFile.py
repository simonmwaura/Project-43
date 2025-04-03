   if choice=="1":
            Client_name = input("Enter your name: ")
            Client_email = input("Enter your email: ")
            Client_phone_number = input("Enter your phone number: ")
            Client_identity_number = input("Enter your identity number: ")
            Client_id = client.create_client(Client_name, Client_email, Client_phone_number, Client_identity_number)
            print(f"\nClient with id {Client_id} was added successfully")
