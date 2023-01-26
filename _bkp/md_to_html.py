import markdown

file = open('tutorial.md',mode='r')
md = file.read()
file.close()
html_file = open("tutorial.html", "w")
html = markdown.markdown(md)
html_file.write(html)
html_file.close()