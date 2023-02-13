file=open("inventory.txt","w")
item=[] #declare list for item details

print("Welcome to the Inventory Management System",
      "---------------------------------------------",
      "---------------------------------------------",
      "A: Add new item",
      "S: Save all the items in the cuttent cart",
      "D: Dispaly all the items in the cuttent cart",
      "T: Terminte",
      "---------------------------------------------", sep="\n") #dispaly instructions

def run():
    """recursive function to keep asking for the type of command"""

    command_type=input("\nEnter the ecommand type: ").upper() #get command type

    if command_type=="A":
            
        item_name=input("Item Name: ") #get item name
        price_of_one=float(input("Prince of one item: ")) #get price of one item

        if price_of_one<=0 or price_of_one>=1000: #check for invalid price of one item
            print("ERROR: Wrong input")
            run() #restart process
        
        quantity=int(input("Quantity: ")) #get quantity

        if quantity<1 or quantity>100: #check for invalid quantity
            print("ERROR: Wrong input")
            run() #restart process

        item.append(item_name)
        item.append(price_of_one)
        item.append(quantity) #append item datails to list item
        run() #restart process

    elif command_type=="S":
        file.write(str(item[0])+":"+"%3.2f"%float(item[1])+":"+str(item[2])+"\n")
        file.close()
        print("Item saved to inventory.txt")
        run() #restart process

    elif command_type=="D":
        
        print(item[0],":",item[1],":",item[2], sep="")
        item.clear()
        run() #restart process

    elif command_type=="T":
        quit() #terminate process

    else:
        print("ERROR: Wrong input")
        run() #restart process

run()
