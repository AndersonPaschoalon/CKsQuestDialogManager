@echo off

echo === Initializing Environment
call Env/Scripts/activate.bat

rem echo === Creating requirements.txt
rem pipreqs --encoding=utf8 .

echo === Building CKQuestDialogManager
python -m PyInstaller --onefile --clean --log-level DEBUG  --noconsole --icon=.\AppClear\Docs\Img\Snowberry_crostata_Blur_WinIcon.ico CKQuestDialogManager.py

echo === Creating Release
robocopy /S /E .\AppClear  dist\\App

