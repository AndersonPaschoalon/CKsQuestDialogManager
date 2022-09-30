@echo off

echo ================================================
echo Initializing Environment
echo ================================================
call Env/Scripts/activate.bat

echo ================================================
echo Building CKQuestDialogManager
echo ================================================
python -m PyInstaller --onefile --clean --log-level DEBUG  --noconsole --icon=.\resources\Snowberry_crostata_Blur_WinIcon.ico CKQuestDialogManager.py

echo ================================================
echo Building CsvDicEditorApp
echo ================================================
python -m PyInstaller --onefile --noconsole   --icon=.\resources\csv01.ico CsvDicEditorApp.py

echo ================================================
echo Creating Release
echo ================================================
rem update CsvDicEditorApp in the AppClear directory
robocopy  dist\ AppClear\Bin\ CsvDicEditorApp.exe
rem update CsvDicEditorApp in the App directory
move dist\CsvDicEditorApp.exe App\Bin\
rem Package for release AppClear
robocopy /S /E .\AppClear  dist\\App
rem package for release CKQuestDialogManager
