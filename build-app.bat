python -m PyInstaller --onefile --noconsole --icon=.\App\Img\sbc.ico  MainWindow.py
robocopy . ./dist/ Comments.csv
robocopy . ./dist/ Actors.csv
robocopy /S /E ./App  dist/App
robocopy /S /E ./Sandbox  dist/Sandbox