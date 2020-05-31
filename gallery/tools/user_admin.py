from db import *

# Begins program to interact with database
def db_program():
    # Begin program and only run while option 5 is not entered
    program_run = True
    while (program_run):
        print("1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit")
        prompt = "Enter command> "
        response = input(prompt)
        print()

        # Execute based on option
        if response == "1":
            # List all users using execute() from db.py
            select_all()
            print()    
        elif response == "2":
            # Add user to database
            user = input("Username> ")
            pw = input("Password> ")
            fn = input("Full name> ")
            add(user, pw, fn);
            print()
        elif response == "3":
            user = input("Username to edit> ")
            pw = input("New password (press enter to keep current)> ")
            fn = input ("New full name (press enter to keep current)> ")

            edit(user, pw, fn)
            # If user does not exist in DB, say "No such user."
        elif response == "4":
            user = input("Enter username to delete> ")
            
            # Check if user is real
            yes_no = input("Are you sure you want to delete " + user + "? ")
            if yes_no == "yes":
                # If yes, delete. If no, do nothing
                delete(user)
                print()
        elif response == "5":
            program_run = False

    print("Bye.")

def main():
    db_program()

if __name__ == "__main__":
    main()
