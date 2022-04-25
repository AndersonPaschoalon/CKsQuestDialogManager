python -m PyInstaller --onefile --noconsole --icon=.\App\Img\sbc.ico  MainWindow.py
REM robocopy . ./dist/ Comments.csv
REM robocopy . ./dist/ Actors.csv
robocopy /S /E ./App  dist/App
robocopy /S /E ./Sandbox  dist/Sandbox