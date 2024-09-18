# Oxyscan: Recarbonized

import flet as ft

def main(page: ft.Page):
    # ID
    page.add(ft.Row([ft.Text("ID da Garrafa"), ft.Text(" *",color="red")]))

    id_Garrafa = ft.TextField(hint_text="ID aqui")
    page.controls.append(id_Garrafa)
    page.update()

    page.add(ft.Row([ft.Text("Lote"),ft.Text(" *",color="red")]))

    lote_Garrafa = ft.TextField(hint_text="Lote aqui")
    page.controls.append(lote_Garrafa)
    page.update()

    page.add(ft.Row([ft.Text("Localização"),ft.Text(" *",color="red")]))

    gps_Garrafa = ft.TextField(hint_text="Localização aqui")
    page.controls.append(gps_Garrafa)
    page.update()

ft.app(main)
