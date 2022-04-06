import easygui

card_catalogue = {
  "Stoneling" : {
    "Strength" : 7,
    "Speed" : 1,
    "Stealth" : 25,
    "Cunning" : 15
  },
  "Vexscream" : {
    "Strength" : 1,
    "Speed" : 6,
    "Stealth" : 21,
    "Cunning" : 19
  },
  "Dawnmirage" : {
    "Strength" : 5,
    "Speed" : 15,
    "Stealth" : 18,
    "Cunning" : 22
  },
  "Blazegolem" : {
    "Strength" : 15,
    "Speed" : 20,
    "Stealth" : 23,
    "Cunning" : 6
  },
  "Websnake" : {
    "Strength" : 7,
    "Speed" : 15,
    "Stealth" : 10,
    "Cunning" : 5
  },
  "Moldvine" : {
    "Strength" : 21,
    "Speed" : 18,
    "Stealth" : 14,
    "Cunning" : 5
  },
  "Vortexwing" : {
    "Strength" : 19,
    "Speed" : 13,
    "Stealth" : 19,
    "Cunning" : 2
  },
  "Rotthing" : {
    "Strength" : 16,
    "Speed" : 7,
    "Stealth" : 4,
    "Cunning" : 12
  },
  "Froststep" : {
    "Strength" : 14,
    "Speed" : 14,
    "Stealth" : 17,
    "Cunning" : 4
  },
  "Wispghoul" : {
    "Strength" : 17,
    "Speed" : 19,
    "Stealth" : 3,
    "Cunning" : 2
  }
}

VALUE_MIN =  1

VALUE_MAX = 25  


def display_options(): 
    '''Displays options and gets user to indicate what they want to do''' 
    options = { 
        "Add card": add_combo, 
        "Find card": search, 
        "Delete card": delete, 
        "Output all cards": output_menu, 
        "Exit": leave}
 
    # Loop until user selects "Exit" options
    msg = "What would you like to do?",
    title = "MENU MAKER OPTIONS",
    choices = list(options.keys())
    while True: 
        if options[easygui.buttonbox(msg, title, choices)]() == "No":
            break

def get_fields(msg, title, fields):
    """Get values for multiple fields.  Returns values in dictionry"""
    values = easygui.multenterbox(msg, title, fields)
   
    # Validate field values
    while True:
        missing_fields = [field for field, value in zip(fields, values) if not value.strip()]
        invalid_values = []
        for field, value in zip(fields, values):
            try:
                value = int(value)
                if not VALUE_MIN <= value <= VALUE_MAX:
                    invalid_values.append(field)  # Not in range
            except ValueError:
                invalid_values.append(field)   # Not a number
 
        if missing_fields:
            missing_fields = ", ".join(missing_fields)
            values = easygui.multenterbox(f"Enter values for {missing_fields}", title, fields, values)
        elif invalid_values:
            invalid_values = ", ".join(invalid_values)
            values = easygui.multenterbox(f"{invalid_values} must be in range {VALUE_MIN}..{VALUE_MAX}", title, fields, values)
        else:
            return {field:value for field, value in zip(fields, values)}


def add_combo(): 
    '''Add new combo to menu''' 
    while True:
        combo_name = easygui.enterbox(
            "Enter Monster Card name: ",
            title = "Monster Card Name").capitalize()
  
        if check_exists(combo_name): 
            easygui.msgbox("That card name has already been used.") 
        else:
            card_catalogue[combo_name] = get_fields(
                msg="Enter Values",
                title="Monster Card Value",
                fields=("Strength", "Speed", "Stealth", "Cunning"))
  
        if not confirm("Do you want to add another monster card?"):
            break

def confirm(msg, title="Confirm"):
    """Return True if user selects Yes, else return False"""
    choices = ["Yes", "No"]
    return easygui.buttonbox(msg, title, choices) == choices[0]



def search(): 

  '''Searches for specified combo in the menu. 
    If the combo is in the menu, the combo details are displayed on 
    screen. Otherwise, the user is told that there is no such combo 
    and given the option to add the combo. 
  ''' 
  msg = "Enter card name:" 
  title = "Card to search for" 
  search = easygui.enterbox(msg, title) 



  # Calls function to check whether the combo already exists 

  combo = check_exists(search) 

  if combo: 

      # Calls function to display combo details on screen. 

      show_menu(combo)


  else: 

      # If the combo does not exist, the user is told this and 

      # given the option to add the combo. 

      msg = "There is no such combo on the menu.\nWould you like to add the combo?" 
      title = "Card does not exist" 
      choices = ["Yes", "No"] 
      add = easygui.buttonbox(msg, title, choices) 

      if add == "Yes": 
        add_combo() # Calls function to add a combo.


def delete(): 

    '''Allows user to delete a combo.''' 

    del_combo = "" 

    while del_combo == "": 

        msg = "Enter name of the card you want to delete." 

        title = "Card to delete" 

        del_combo = easygui.enterbox(msg, title) 

 

        # Calls function to check if the combo entered by user exists. 

        del_combo = check_exists(del_combo) 

         

        # If the combo exists, the user is asked to confirm whether 

        # they want to delete the combo. Otherwise, they are shown an 

        # error message. 

        if del_combo: 

            msg = "Are you sure you want to delete the " + del_combo + " Card?" 

            title = "Confirm delete" 

            choices = ["Yes","No"]  

            sure = easygui.buttonbox(msg, title, choices) 

            if sure == "Yes": 

                card_catalogue.pop(del_combo) 

        else: 

            msg = "That combo is not on the menu." 

            title = "ERROR: Combo not on menu" 

            easygui.msgbox(msg, title) 

            del_combo = "" 

def output_menu(): 

    '''Outputs the full menu to Python Shell (for printing)''' 

    output = ""

    for combo_name, combo_info in card_catalogue.items(): 

        print("\n\n" + combo_name.upper() + " MONSTER CARD") 
        output += f"{combo_name.capitalize()}:\n"

 

        for key in combo_info: 
            price = format(combo_info[key]) 
            print(key + ": " + price)
            output += f"\t{key}: {price}\n"            

        print("_" * 26) 

    easygui.textbox("These are the contents of the card catalogue",
                    "Display All Combos", output) 


def validate_value(value, item): 

    """Input validation: Checks that the user has input a valid value. 
    """ 

    # If the user presses the Cancel button, function is called to  

    # confirm that the user wants to exit. 

    if value == None: 
      
      value = query_cancel() 

 

    # If the user presses the OK button without entering a value, 

    # the no_value() function is called to display an error message 

    # and get input. 

    

    while value == "": 
      
      value = no_value(item) 
      

 

    # The while loop checks that input is valid (from VALUE_MIN to  

    # VALUE_MAX), and if not an error message is displayed, and the  

    # user is prompted to re-enter the value. 

    while float(value) < VALUE_MIN or float(value) > VALUE_MAX: 
      
      
      msg = "Please enter a valid value for " + item + " (from " + str(VALUE_MIN) + " to " + str(VALUE_MAX) + ")." 
      title = "ERROR" 
      value = easygui.enterbox(msg, title) 
      

 

        # If the user pressed OK without entering a value, the function 

        # is called to display and error message and get input. 

      while value == "": 
        value = no_value(item) 

 

        # If the user presses the Cancel button, function is called to  

        # confirm that the user wants to exit. 

      if value == None: 
        
        value = query_cancel()
        
        return (value) 


def no_value(item): 

    """Input validation: If the user presses the OK button without  
    entering a value, they are shown an error message, and prompted 
    again to enter a value. 
    """ 

    msg = "You must enter a value for " + item + " (from $" + str(VALUE_MIN) + " to $" + str(VALUE_MAX) + ")." 

    title = "ERROR" 

    value = easygui.enterbox(msg, title) 

         

    # If the user presses the Cancel button, function is called to  

    # confirm that the user wants to exit. 

    if value == None: 
      
      value = query_cancel() 
      
      return value 

 

def query_cancel(): 

    """Input validation: If the user presses the Cancel button, they are 
    asked if they are sure they want to exit the current menu item. 
    """ 

    leave = easygui.buttonbox("Do you want to exit?", choices=["Yes", "No"]) 

 

    # If the user confirms they want to exit, they are shown the main 

    # list of options. 

    if leave == "Yes": 

        # Takes back to the main menu or you could simply have exit() 

        display_options() 

    else: 

        # Returns nothing so that the program continues 

        return 0 

 

 

def check_exists(name): 
    '''Checks whether a combo exists.  Return combo name if found, else None'''
    name = name.capitalize()
    if name in card_catalogue:
        return name
    return None


def show_menu(name):
  
  '''Displays the details for the combo that has been added.'''
  
  output = ["\n\n***" + name + " Combo details***\n"]
  
  for value in card_catalogue[name]:
    price = format(card_catalogue[name][(value)])
    info = value + ": " + price
    easygui.msgbox(output.append(info))
  
  easygui.msgbox("\n".join(output))

       

def add_items(combo): 

    '''Allows the user to add items to a specified combo.''' 

    msg = "Enter item/s for combo, separated by a comma." 

    title  = "Enter card items" 

    items = easygui.enterbox(msg, title) 

 
    items_list = items.split(",") 

    

    for i in items_list: 

        # Input handling: To handle a situation where the user enters 

        # a space after the comma when entering items. 

        item = i.strip() 

        msg = item + ": Enter Strength/Speed/Stealth/Cunning Value:" 

        title  = item + " Monster Card Value:" 

        card_catalogue[combo][item] = easygui.enterbox(msg, title) 

 


     

def leave(): 

    '''Farewells user if they have chosen to exit the program.''' 

    easygui.msgbox("Thanks for using the menu builder.") 

    return "N" 

 

 

# The main program starts below. 

display_options() 