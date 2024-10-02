# Oxyscan: Recarbonized

# Nota! page.views[-1].controls.append serve para ler a página atual depois de estar tudo já inicializado.

from time import sleep
import flet as ft

def main(page: ft.Page):
    addlist = ft.ListView(auto_scroll=True, height=page.window.height-60 if page.window.height!=None else 300)
    removelist = ft.ListView(auto_scroll=True, height=page.window.height-60 if page.window.height!=None else 300)
    searchlist = ft.ListView(auto_scroll=True, height=page.window.height-60 if page.window.height!=None else 300)

    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        on_change=page.update(),
        tabs=[
            ft.Tab(
                text="Adicionar",
                icon=ft.icons.CREATE,
                content = ft.Column(expand=True, controls=[
                    ft.Text(" "),

                    ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="ID aqui"),

                    ft.Row([ft.Text("Lote"),ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="Lote aqui"),

                    ft.Row([ft.Text("Localização"),ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="Localização aqui"),

                    ft.Text("Utente"),
                    ft.TextField(hint_text="Nome de utente aqui"),
                    ft.Text(" "),
                    ft.ElevatedButton(
                        "Criar garrafa",
                        icon=ft.icons.ADD,
                        icon_color="blue400",

                    ),
                    addlist
                    ]
                 )
                
            ),
            ft.Tab(
                text="Remover",
                icon=ft.icons.DELETE,
                content = ft.Column(expand=True, controls=[
                    ft.Text(" "),

                    ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="ID aqui"),

                    ft.Row([ft.Text("Lote"),ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="Lote aqui"),
                    ft.Text(" "),
                    ft.ElevatedButton(
                        "Apagar garrafa",
                        icon=ft.icons.DELETE,
                        icon_color="red400",
                    ),
                    removelist
                    ]
                 )
  
            ),
            ft.Tab(
                text="Pesquisar",
                icon=ft.icons.SEARCH,
                content = ft.Column(expand=True, controls= [
                    ft.Text(" "),

                    ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="ID aqui"),

                    ft.Row([ft.Text("Lote"),ft.Text(" *",color="red")]),
                    ft.TextField(hint_text="Lote aqui"),
                    ft.Text(" "),
                    ft.ElevatedButton(
                        "Procurar garrafa",
                        icon=ft.icons.SEARCH,
                        icon_color="blue400",
                    ),
                    ft.Text(" "),
                    searchlist
                    ]
                 )
                
            ),
        ],
        expand=0,
    )
    
    page.add(t)
    
    for i in range(0, 60):
        sleep(1)
        addlist.controls.append(ft.Text(f"addlist test: {1 * i}"))
        removelist.controls.append(ft.Text(f"addlist test: {1 * i}"))
        searchlist.controls.append(ft.Text(f"addlist test: {1 * i}"))
        page.update()
    page.go("/add")
    page.update()
ft.app(main)
