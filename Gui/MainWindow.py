import PySimpleGUI as sg
from emoji import emojize

FI = 1.618
WINDOW_HIGH = 500
WINDOW_WIDTH = int(WINDOW_HIGH*FI)
HLINE = "-----------------------------------------------------------------------------"
FONT_TEXT = ('MS Sans Serif', 10, 'bold')
FONT_TITLE2 = ('MS Sans Serif', 14)
FONT_TITLE1 = ('MS Sans Serif', 18,)
FONT_SKIPLINE1 = ('MS Sans Serif', 20,)
FONT_SKIPLINE2 = ('MS Sans Serif', 15,)

if __name__ == '__main__':
    #sg.theme('DarkTeal9')
    sg.theme('DarkBlue17')
    #sg.theme('DarkPurple2')

    layout_title_main = [sg.Text(emojize(":fleur-de-lis:") + " CreationKit-DialogDocGen " + emojize(":fleur-de-lis:"), font=('Any', 32))]
    layout_title_config = [sg.Text(emojize(":hammer_and_wrench:") + " Application Setup", font=FONT_TITLE2)]
    layout_title_export = [sg.Text(emojize(":scroll:") + " Export Documentation", font=FONT_TITLE2)]
    layout_title_help = [sg.Text(emojize(":globe_with_meridians:") + " Help", font=FONT_TITLE2)]

    # Buttons
    layout_settings = [sg.Button("Settings"), sg.Button("Export Objects to Comments.csv"), sg.Button("Export Actor's IDs to Actors.csv"), sg.Button("Choose Theme")]
    layout_export = [sg.Button("Export Documentation")]
    layout_tutorial = [sg.Text("Tutorial"), sg.Text("Github"), sg.Text("Nexus")]

    # Layout
    layout = [layout_title_main, [sg.Text("", font=FONT_SKIPLINE1)],
              layout_title_config, layout_settings, [sg.Text("", font=FONT_SKIPLINE2)],
              layout_title_export, layout_export, [sg.Text("", font=FONT_SKIPLINE2)],
              layout_title_help, layout_tutorial, [sg.Text("", font=FONT_SKIPLINE2)],
              ]


    #layout = [[sg.Text(emojize(":fleur-de-lis:") + " CreationKit-DialogDocGen " + emojize(":fleur-de-lis:"), font=('Any', 32))], [sg.Text("")], [sg.Text(emojize(":hammer_and_wrench:") + "Settings", font=FONT_TITLE2)], [sg.Text(HLINE, font=FONT_TITLE2)], [sg.Button("OK1"), sg.Button("OK2"), sg.Button("OK3")]]
    #sg.Window(title="Hello World", layout=layout, margins=(WINDOW_WIDTH, WINDOW_HIGH)).read()
    #sg.Window(title="Hello World", layout=layout, size=(WINDOW_WIDTH, WINDOW_HIGH), background_color=BACKGROUND_COLOR).read()
    sg.Window(title="Creation Kit - Dialog Doc Generator", layout=layout, size=(WINDOW_WIDTH, WINDOW_HIGH), icon="../App/Img/sbc.ico").read()