# CK's Quest Dialog Manager

Creatin Kit's Quest Dialog Manager, as the name says, is a tool for helping mod creators to manage Creation Kit's Quest dialogs in a simple way.

It is possible to export quests dialog information from creation kit into text file. The idea is to import that information, and use it to create a content manager.


# Who this tool is usefull for? 

**Short answer**: 

*For skyrim modders who:*

* *Want to review or share quest dialogs in a readable format;*
* *Want to manage dialog files easily. By manager, I mean, find files, list to, open at the location, replace, extract information, and convert into different formats (mp3, wav, xwm, fuz)*


**Long answer**: 

> ![](Img/1.png)
> *Dialog View window in the creation kit.*

When you create a new quest for the game, usually it will have dialogs and scenes, so the Dragonborn will be able to interact with other people in the world. 

So, as a mod developer, I wrote down a draft of the speeches and inserted it into the Creation Kit. But I found the process of reviewing the dialogs for correcting typos, fixing little things, and applying some changes, PAINFULL AND TEDIOUS.

I had to click in dozens of boxes to find the text I wanted to review. Since changes were frequently applied to the dialogs, the drafts were completely outdated. 
When some people started to appear offering help, I had to provide the most current version of the story script, in a readable format. How should sustainably do that?

I saw that I need to find some way to auto-generate documentation for the dialogues, so I or another person could review the most updated version simply, always using the most recent version. 

Creating Kit allows you to export the dialogs in a (horrible to read as a human) CSV table, with lots of information, really hard to understand without context.

I decided to create a tool to help me with the task of creating readable documentation automatically. It started as a simple script. With the time, it evolved into a content manager tool, since I implemented  many more features using all information I was already importing.

In this current version, this tool:

* Allows me to create beautifull documentation for my quests in many formats: HTML, Markdown, DOCX and JSON;

* Allows the management of audio files from quests in a reasonable way. As stated before, I can easily find and open (in player or in the Windows file explorer) and audio file according to its  subititle. I can extract information, and convert into many formats; 

* It is possible to generate mute audio files with the aproximate time lenght expent for a real person to speak the the audio text.


Once I had and stable version in my hands, I decided to share with the community in the Nexus. Hope this can be useful for someone else as well.


# Tutorial

## Application folder 

CK's Quest Dialog Manager is an auto-executable application, therefore it does not requere installation. It shoud have the following structure:

> ![](Img/app-folder.jpg) 
> *CKQuestDialogManager application's folder structure.*


* *App*: Application folder, this store files required byt the application to work properly. 

* *OUTPUT*: this folder is created after the application is executed for the first time. This folder store generated documentation and reports.

* *CKQuestDialogManager.exe*: application executable.


## Main Window

> ![](Img/main-window.jpg)
> *CKQuestDialogManager main window.*

Executing the application will launch this windows.  This Windows is divided inth three sections:


**Application Settings**
* *Settings*: Allows the basic cofiguration of the application. Usually the settings do not need to be changed.
    * *Skyrim Path*: the most inportant configuration, the path where Skyrim is intalled, usually `C:\\Program Files (x86)\\Steam\\steamapps\\common\\Skyrim`.
    * *Docgen Folder*: usually `OUTPUT` folder. 
    * *Sort by Name(true) or Form ID (false)*: the branches in the documentation will be sorted in the alphabetical order if it is set as true, or by the Form ID if it is set as false. 
    
> ![](Img/settings-window.jpg)
> *Settings window.*

* *Profiles*: 
Profiles allows the Mod developer to manage the Dialogs from many mods in different workspaces, keeping their imported assets separate. Each profile will store all the settings and imported files from the Creation Kit. 
The application is going to have a "Default" profile configured in the first time it is used, but it can be renamed later with a proper name. 
You can choose color schemas for each profile as well. The profile management window will indicates wich profile is currently active with an arrow. To help identifying each profile, you can put some comments or description about the profile as well. Finally, you can Create new profiles, Load, Edit and Delete using this window. Take care, Delete option cannot be undone. 


> ![](Img/prefile-main.jpg)
> *Profiele management window.*

> ![](Img/profile-edit.jpg)
> *Profile editing window.*

> ![](Img/profile-new.jpg)
> *Profile creation window.*



## Step 1: Preparing the quest

For the auto-generation of the documentation to work properly, when a dialog is spoken by a unique actor, he/she must be set on the "**Speaker:**" field on the **Topic Info** window.  In the figure down belows is indicated where this option is located.

> ![](Img/ck-speaker-window.png)
> *Location of the field "Speaker", in the Topic Info window. This field usually is optional, but it is really important to be properly filled in for this application to work properly.*

## Step 2: Export the dialogs from Creation Kit

To generate the documentation, CkQuestDialogManager needs to export the dialogs from the Creation Kit.

In the quest object editor, in the "Quest Data" tab of the quest you want to manage,  you must click on both button presented in the image down below: "Export Scene Dialogue" and "Export Quest Dialog".

> ![](Img/ck-export-files.png)
> *Buttons that must be clicked for each quest you want to manage the dialogs.*

For the first Button "Export Scene Dialog", you are going to be asked wich actor you want to export the data. Select all actors (one each time) of the mod you want to manage. 

Next, click on the button "Export Quest Dialog" on the "Quest Data" tab from your selected quest.

> ![](Img/ck-export01.png)
> *"Export Scene Dialog" and "Export Quest Dialog" buttons on the "Quest Data" tab.*

Then, click ok.

>![](Img/ck-export02.png)
> *Confirmation window.*

If you proceed well these steps, all the quest dialog data was properly exported to text files. In the image down below, we show an example of exported files.

> ![](Img/ck-export-files.jpg)
> *Exported files from Creation kit.*


## Step 3: Configuring CkDialogDocGen

On CkDiagDocgen, click on settings.

![](Img/ck-main-settings.png)

* You must check if the "Skyrim Path" option is pointing to the Skyrim installation folder on your computer.
* The DocGen folder points to the folder where you want to save the generated documentation. You may leave it as it is, or change it to a different folder if you want to.
* Sort by name or by FormId defines the sorting methods for the **Topics** in the same **Branch**. If you have a good name conversion, true should be the best option.

> ![](Img/settings-window.jpg)
> *Settings window.*


## Step 4: Previwing the documentation

At this point, you can already generate the documentation. 

First, we have to fill the dictionaries Actos.csv and Comments.csv. Click on "Export Objects to CSV files". 

![](Img/7.png)

A pop-up will be displayed with the list of files processed, and the Objects and actors found.  In this example, we exported the data from two quests: "DSilHand_M10SilverHunt", and "DSilHand_M80AssaultJor". 

![](Img/8.png)

Then click OK.

If you open the files Comments.csv or Actos.csv with a text editor or with a CSV editor*, you will notice that the listed actors and objects IDs were written right there. 

(*) Such as Libre Office Calc or Excel. But if you want to use a tool like that, you should use a semicolon (;) as a separator.

![](Img/8a.png)
![](Img/8b.png)
![](Img/8c.png)
![](Img/8d.png)

Now, you can generate the documentation, by clicking on the button "Generate Documentation".

![](Img/9.png)


It will display a pop-up with the quests it was able to generate the documentation.

![](Img/10.png)


If you enter the directory where the documentation was supposed to be generated, you will notice 4 subfolders:
* Docx;
* Html;
* Markdown;
* Json.
These are the formats the documentation will be generated in. They have the same content but in different formats.

![](Img/10a.png)

Opening the document "DSilHand_M10SilverHunt.docx" generated for the first quest, you will see the following structure:

![](Img/10b.png)

The document title is "Quest \<quest-ID\>", and a paragraph with the text ?quest-commenty?  The following subtitles are the Branchs IDs. 
First, it will have a text "?branch-comment?", followed by some useful information about this branch -- such as if the branch is a PlayerDialog or a Scene, the race, and the voice type of the speaking actor, and so on. 

Then, you are going to have a sub-subtitle for each topic in the branch. This subsection contains a player (if it applies) and a list of dialogs for the actor to who its branch belongs (if any). The actor is indicated by its ID and is followed by its mood and the file name for the voice audio.  

A first version for the documentation was already generated!
But it has some problems: 

* You may want to give some context for the branches, so the one who read the documentation may understand the context of the dialogues.  so who read the documentation can understand the context. 
* You may want to explain the quest history as well at the start of the document, for a better understanding of the whole picture of the dialogues, and how the branches connect.
* The characters have their actor's IDs, not their actual names at the start of the dialogues. 

Yes, you can write that information indirectly on your document, but if you regenerate the documentation again, you will have to rewrite the information all over again. 

For solving this issue we have the Comments.csv and Actors.csv files. 


## Step 5: Adding comments and naming the Actors

Open the Actors.csv file and the Comments.csv file with your favorite CSV or text editor, and add the Actual names for the actors and your commentaries for the quests and branches*.

After you are done, just save it. But keep in mind you must preserve the CSV format if you are using a CSV editor. 
If you are using a text editor, remember the separator is a semicolon.

**Note: You should not use semicolons on comments or Actors' names.**

![](Img/11a.png)

![](Img/11b.png)

(*) The current version of the documentation does not support comments for the Topics.


## Step 6: Generating the docuementation

Repeat the same procedure from Step 4: click on "Generate Documentation", and "OK".

**Note: You may click on "Export Objects to CSV files" many times you want to or need. No row from the tables is going to be removed, and its content removed. It will just add new blank rows (if necessary) at the end of the files.**

![](Img/12.png)


# Observations

* Whan you press the button "Export the Objects to CSV files", **it does not overwrite or erase any of the entries** are already on the files Actors.csv and Comments.csv. It only adds new entries. Therefore, the same CSV files can be used to generate the documentation for multiple quests from different mods, with no issue, as long the IDs for the objects are unique (as they should be).

* Make sure the documentation files are **CLOSED** after regenerating the documentation. It may lead to unexpected errors.

* This program has logged. Usually, you are not going to use them, but if some strange error occurs (and the documentation files are not closed), you may send them to me in my email (anderson dot paschoalon at gmail dot com), with a description of what you have done. If it is a bug, I will fix it as soon as possible. If it is not, I will fix it as soon as possible. Or, if it is not a bug, I'll improve the documentation.



