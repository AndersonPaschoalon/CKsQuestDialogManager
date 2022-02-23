import PySimpleGUI as sg
from emoji import emojize
import webbrowser
import  os


FI = 1.618
WINDOW_HIGH = 500
WINDOW_WIDTH = int(WINDOW_HIGH*FI)
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HIGH)
FONT_TEXT = ('MS Sans Serif', 10, 'bold')
FONT_TITLE2 = ('Any', 14)
FONT_TITLE1 = ('Any', 18,)
FONT_SKIPLINE1 = ('Any', 20,)
FONT_SKIPLINE2 = ('Any', 15,)

def open_tutorial():
    filename = 'file:///' + os.getcwd() + '/' + '../App/Pages/sample.html'
    webbrowser.open_new_tab(filename)

if __name__ == '__main__':
    #sg.theme('DarkTeal9')
    #sg.theme('DarkBlue17')
    #sg.theme('DarkPurple2')
    sg.theme('DarkGrey13')


    layout_title_main = [sg.Text(emojize(":fleur-de-lis: CreationKit-DialogDocGen :fleur-de-lis:", variant="emoji_type"), font=('Any', 32))]
    layout_title_config = [sg.Text(emojize(":hammer_and_wrench:Application Setup", variant="emoji_type"), font=FONT_TITLE2)]
    layout_title_export = [sg.Text(emojize(":scroll:     Documentation Generation", variant="emoji_type"), font=FONT_TITLE2)]
    layout_title_help = [sg.Text(emojize(":globe_with_meridians:     Help", variant="emoji_type"), font=FONT_TITLE2)]

    # Buttons
    layout_settings = [sg.Button("Settings"), sg.Button("Choose Theme")]
    layout_export = [sg.Button("Export Objects to Comments.csv"), sg.Button("Export Actor's IDs to Actors.csv"), sg.Button("Generate Documentation")]
    layout_tutorial = [sg.Button("Tutorial", key=lambda: open_tutorial()), sg.Button("Github"), sg.Button("Nexus")]

    # Layout
    layout = [layout_title_main, [sg.Text("", font=FONT_SKIPLINE1)],
              layout_title_config, layout_settings, [sg.Text("", font=FONT_SKIPLINE2)],
              layout_title_export, layout_export, [sg.Text("", font=FONT_SKIPLINE2)],
              layout_title_help, layout_tutorial, [sg.Text("", font=FONT_SKIPLINE2)],
              ]


    #layout = [[sg.Text(emojize(":fleur-de-lis:") + " CreationKit-DialogDocGen " + emojize(":fleur-de-lis:"), font=('Any', 32))], [sg.Text("")], [sg.Text(emojize(":hammer_and_wrench:") + "Settings", font=FONT_TITLE2)], [sg.Text(HLINE, font=FONT_TITLE2)], [sg.Button("OK1"), sg.Button("OK2"), sg.Button("OK3")]]
    #sg.Window(title="Hello World", layout=layout, margins=(WINDOW_WIDTH, WINDOW_HIGH)).read()
    #sg.Window(title="Hello World", layout=layout, size=(WINDOW_WIDTH, WINDOW_HIGH), background_color=BACKGROUND_COLOR).read()
    window = sg.Window(title="Creation Kit - Dialog Doc Generator", layout=layout, size=WINDOW_SIZE, icon="../App/Img/sbc.ico").read()

    while True:  # Event Loop
        event, values = window.read()
