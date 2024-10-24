# Neon >Oxyscan< Evagelion (version 0.25b)

"""
(Mini)-Patch Notes:

- Started work on making deleting work

Planned for next Patch:

The same as always, so:

- Proper bottle displaying (so no more reading JSON, I suppose)
- Searching for bottles.
- Being able to switch languages. (on release it'll be english, slovakian and portuguese (don't ask why slovakian in specific))
- Continued format of using a single file for the whole app. (lol) ((but i might actually switch if it ends up hurting performance in long-term))
- Barring web devices and scanner-less phones from creating new bottles (even though these are just text boxes) ((you can change this as it'll be a variable you can simply tick "True" for every device, i just felt like it'd be better this way))


Special thanks for this (Mini)-Patch:
- no one this time around

"""

import os
import json
import pymysql as sql
import flet as ft

# Arguments required to connect, check the README.md to see what to do with them
connect_kw_args = {
    'database': "oxyscan",
    'host': 'localhost',
    'port': 3306,
    'user': "oxyscan_test",
    'password': "authorized"
}

# Connect to the server
connection = sql.connect(**connect_kw_args)

# Create variable to check whetever the user is online or not
is_online = False

# Special thanks to Stack Overflow for giving me a hand on these functions
def load_offline_list(file_path):
    if not os.path.exists(file_path): # If it can't find the file, it's going to create it
        with open(file_path, 'w') as file:
            json.dump([], file)

    with open(file_path, 'r') as file: # Else, it'll just convert all the data in here to JSON and return it.
        try:
            return json.load(file)
        except:
            return []


def write_offline_list(file_path, data):
    try:
        data = json.loads(data) # Attempts to load the current data
    except:
        print("JSON loading failed!")
        return

    current_data = load_offline_list(file_path) # Loads the data present on the file
    current_data.extend(data) # Mixes both datas

    with open(file_path, 'w') as file: # Writes all of the given data onto the file
        json.dump(current_data, file, indent=4) 

def load_online_list():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM garrafas")
    items = cursor.fetchall() # Fetch all of the results
    columns = [col[0] for col in cursor.description] # Returns all columns 
    json_data = [dict(zip(columns, row)) for row in items] # Passes all of this data into a dictionary

    with open("garrafas.json", 'w') as file: # Write it all into the file, syncing the offline data with the online
        json.dump(json_data, file, indent=4)
    
    return json_data


def sync_offline_to_online(file_path): # So the reverse of the previous comment: we sync the online with the offline
    offline_data = load_offline_list(file_path)

    if not offline_data: # If there's Nothing There
        print("can't sync data if it doesn't even exist")
        return

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM garrafas")
    existing_ids = {row[0] for row in cursor.fetchall()} # Fetch everything in garrafa_ID


    new_entries = [] # Create a list where we'll store all of the new bottles to add

    for item in offline_data:
        if item['garrafa_ID'] not in existing_ids: # If this ID does not exist 
            new_entries.append({
                'garrafa_ID': item['garrafa_ID'],
                'garrafa_Lote': item['garrafa_Lote'],
                'garrafa_Localizacao': item['garrafa_Localizacao'],
                'garrafa_Utente': item['garrafa_Utente']
            })

        if new_entries: # If there are new bottles
            with connection.cursor() as cursor:
             for thing in new_entries:
                stmt_insert = f'INSERT INTO garrafas (garrafa_ID, garrafa_Lote, garrafa_Localizacao, garrafa_Utente) VALUES ({thing["garrafa_ID"]}, {thing["garrafa_Lote"]}, "{thing["garrafa_Localizacao"]}", "{thing["garrafa_Utente"]}")'
                cursor.execute(stmt_insert)
                connection.commit()
            print(f"inserted {len(new_entries)} new bottles ")
        else:
            print("no bottles added ")
# End of Stack Overflow-aided functions

def main(page: ft.Page):
    # Create the lists seperate from the Tab so we can write in them during code execution
    addlist = ft.ListView(auto_scroll=True, padding=20, spacing=5, height=page.window.height - 200 if page.window.height else 300)
    removelist = ft.ListView(auto_scroll=True, height=page.window.height - 200 if page.window.height else 300)
    searchlist = ft.ListView(auto_scroll=True, height=page.window.height - 200 if page.window.height else 300)

    # Bundle them up in one list so I don't have to write yet another switch/if check
    activeList = [addlist, removelist, searchlist]

    global is_online
    is_online = False

    def updatelist(ind):
        global is_online 
        activeList[ind].controls.clear() # Clear out the list, otherwise it'll pile up quick
        if is_online: # If it's online
            json_list = json.dumps(load_online_list()) # Retrieve data off this function
            for line in json_list.splitlines(): # Split it into lines
                activeList[ind].controls.append(ft.Text(line)) # Apply all lines to the list
        else:
            json_list = json.dumps(load_offline_list("garrafas.json"), indent = 4) # Same thing, but reads off the file instead
            for line in json_list.splitlines():
                activeList[ind].controls.append(ft.Text(line))
        page.update()

    def switchmode(e):
        global is_online

        if is_online == False:
            try: # Syncs, swaps modes, and updates list
                sync_offline_to_online("garrafas.json")
                is_online = not is_online
                updatelist(t.selected_index)
            except:
                print("failed to update, there might be no wifi at all")
        else: # Swaps modes and updates list
            is_online = not is_online
            updatelist(t.selected_index)

    # ALso adding these seperatedly so I can read off their values later
    addid = ft.TextField(hint_text="ID aqui")
    addlote = ft.TextField(hint_text="Lote aqui")
    addgps = ft.TextField(hint_text="Localização aqui")
    addutente = ft.TextField(hint_text="Nome de utente aqui")

    def upload_bottle(e):
        global is_online
        if is_online: # If we're online
            if addid.value and addlote.value and addgps.value: # If these obiligatory values are present
                with connection.cursor() as cursor:
                    stmt_insert = f'INSERT INTO garrafas (garrafa_ID, garrafa_Lote, garrafa_Localizacao, garrafa_Utente) VALUES ({addid.value}, {addlote.value}, "{addgps.value}", "{addutente.value}")'
                    cursor.execute(stmt_insert) # Run this SQL command to insert the values onto the table. PRO-TIP: Don't run any delete operations from the app. It can AND will go wrong.
                connection.commit()
                updatelist()
        else: # Just condense the info and write it to the file if it's offline
            if addid.value and addlote.value and addgps.value:
                informação = {
                    'garrafa_ID': addid.value,
                    'garrafa_Lote': addlote.value,
                    'garrafa_Localizacao': addgps.value,
                    'garrafa_Utente': addutente.value
                }
                write_offline_list("garrafas.json", informação)

    def delete_bottle(e):
        global is_online
        if is_online: # If we're online
            if addid.value and addlote.value: # If these obiligatory values are present
                with connection.cursor() as cursor:
                    stmt_insert = f'DELETE FROM garrafas WHERE garrafa_ID = {addid.value} AND garrafa_Lote = {addlote.value};'
                    cursor.execute(stmt_insert) # Run this SQL command to delete the values off the table. PRO-TIP: Don't run any delete operations from the app. It can AND will go wrong.
                connection.commit()
                
                load_online_list()
                updatelist()
        else: # Just condense the info and write it to the file if it's offline
            if addid.value and addlote.value:
                 if addid.value and addlote.value:
                     with open("garrafas.json", 'r') as file:
                        data = json.load(file)  # Load the JSON data
                         # Fetch an array with a for loop inside that checks if the selected items are part of the file
                        data = [item for item in data if not (item['garrafa_ID'] == addid.value and item['garrafa_Lote'] == addlote.value)]

                     # Write the updated list back to the file
                     with open("garrafas.json", 'w') as file:
                        json.dump(data, file)


    t = ft.Tabs(
        selected_index=0, # Index goes from 0 to 2 if there are 3 present
        animation_duration=300, # This feels fine enough for me
        on_change=page.update(), # Update the page everytime we swap tabs so everything works out
        tabs=[
            # "Adicionar" tab
            ft.Tab(
                text="Adicionar",
                icon=ft.icons.CREATE,
                content=ft.Column(expand=True, controls=[
                    ft.Text(" "),
                    ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *", color="red")]),
                    addid,
                    ft.Row([ft.Text("Lote"), ft.Text(" *", color="red")]),
                    addlote,
                    ft.Row([ft.Text("Localização"), ft.Text(" *", color="red")]),
                    addgps,
                    ft.Text("Utente"),
                    addutente,
                    ft.Text(" "),
                    ft.ElevatedButton(
                        "Criar garrafa",
                        icon=ft.icons.ADD,
                        icon_color="blue400",
                        on_click=upload_bottle
                    ),
                    ft.Switch(label="Ligar a base de dados", value=is_online, on_change=switchmode),
                    addlist
                ])
            ),

            # "Remover" tab
            ft.Tab(
                text="Remover",
                icon=ft.icons.DELETE,
                content=ft.Column(expand=True, controls=[
                    ft.Text(" "),
                    ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *", color="red")]),
                    ft.TextField(hint_text="ID aqui"),
                    ft.Row([ft.Text("Lote"), ft.Text(" *", color="red")]),
                    ft.TextField(hint_text="Lote aqui"),
                    ft.Text(" "),
                    ft.ElevatedButton(
                        "Apagar garrafa",
                        icon=ft.icons.DELETE,
                        icon_color="red400",
                        on_click=delete_bottle
                    ),
                    ft.Switch(label="Ligar a base de dados", value=is_online, on_change=switchmode),
                    removelist
                ])
            ),

            # "Pesquisar" tab
            ft.Tab(
                text="Pesquisar",
                icon=ft.icons.SEARCH,
                content=ft.Column(expand=True, controls=[
                    ft.Text(" "),
                    ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *", color="red")]),
                    ft.TextField(hint_text="ID aqui"),
                    ft.Row([ft.Text("Lote"), ft.Text(" *", color="red")]),
                    ft.TextField(hint_text="Lote aqui"),
                    ft.Text(" "),
                    ft.ElevatedButton(
                        "Procurar garrafa",
                        icon=ft.icons.SEARCH,
                        icon_color="blue400",
                    ),
                    ft.Text(" "),
                    ft.Switch(label="Ligar a base de dados", value=is_online, on_change=switchmode),
                    searchlist
                ])
            ),
        ],
        expand=False
    )
    
    # Add the tabs to the page, change it to the real working page, update it and update our list
    page.add(t)
    page.go("/add")
    page.update()
    updatelist(t.selected_index)

ft.app(main)
