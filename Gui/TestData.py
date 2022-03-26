from Gui.AudioData import AudioData


lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def create_audio_list():
    s1 = "I have a 2-dimensional table of data implemented as a list of lists in Python. I would like to sort the data by an arbitrary column. This is a common task with tabular data."
    s2 = "For example, Windows Explorer allows me to sort the list of files by Name, Size, Type, or Date Modified. "
    s3 = "I tried the code from this article, however, if there are duplicate entries in the column being sorted, the duplicates are removed."
    s4 = " This is not what I wanted, so I did some further searching, and found a nice solution from the HowTo/Sorting article on the PythonInfo Wiki. "
    s5 = "This method also uses the built-in sorted() function, as well as the key paramenter, and operator.itemgetter(). "
    s6 = "See section 2.1 and 6.7 of the Python Library Reference for more information.) The following code sorts the table by the second column (index 1)."
    s7 = "Note, Python 2.4 or later is required."
    s8 = "This works well, but I would also like the table to be sorted by column 0 in addition to column 1. In this example, column 1 holds the Last Name and column 0 holds the First Name. I would like the table to be sorted first by Last Name, and then by First Name. Here is the code to sort the table by multiple columns."
    s9 = "The cols argument is a tuple specifying the columns to sort by. The first column to sort by is listed first, the second second, and so on."
    s10 = "An example using Python's groupby and defaultdict to do the same task — posted 2014-10-09"
    s11 = "python enum types — posted 2012-10-10"
    audio_list = []
    audio_list.append(AudioData('audio/01\ -\ Unfinished\ Allegro.mp3', "Angels Cry", "Angra", s1))
    audio_list.append(AudioData('audio/02\ -\ Carry\ On.mp3', "Angels Cry", "Angra", s2))
    audio_list.append(AudioData('audio/03\ -\ Time.mp3', "Angels Cry", "Angra", s3))
    audio_list.append(AudioData('audio/04\ -\ Angels Cry.mp3', "Angels Cry", "Angra", s4))
    audio_list.append(AudioData('audio/05\ -\ Stand Away.mp3', "Angels Cry", "Angra", s5))
    audio_list.append(AudioData('audio/06\ -\ Never Understand.mp3', "Angels Cry", "Angra", s6))
    audio_list.append(AudioData('audio/07\ -\ Wuthering Heights.mp3', "Angels Cry", "Angra", s7))
    audio_list.append(AudioData('audio/08\ -\ Streets Of Tomorrow.mp3', "Angels Cry", "Angra", s8))
    audio_list.append(AudioData('audio/09\ -\ Evil Warning.mp3', "Angels Cry", "Angra", s9))
    audio_list.append(AudioData('audio/10\ -\ Lasting Child.mp3', "Angels Cry", "Angra", s10))
    audio_list.append(AudioData('audio/11\ -\ Rainy Nights.mp3', "Fireworks", "Angra", s11))
    return audio_list

