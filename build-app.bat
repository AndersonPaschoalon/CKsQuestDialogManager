call Env/Scripts/activate.bat
python -m PyInstaller --onefile --noconsole --icon=.\App\Img\sbc.ico main.py
robocopy /S /E ./App  dist/App