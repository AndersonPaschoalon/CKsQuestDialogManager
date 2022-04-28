call Env/Scripts/activate.bat
python -m PyInstaller --onefile --noconsole --icon=.\App\Img\sbc.ico CKQuestDialogManager.py
python -m PyInstaller --onefile --noconsole --icon=.\App\Img\csv01.ico CsvDicEditorApp.py
move dist\CsvDicEditorApp.exe App\Bin\
robocopy /S /E ./App  dist/App