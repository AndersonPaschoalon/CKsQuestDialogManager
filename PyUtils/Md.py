import markdown


class Md:
    HTML_HEADER = """<html>
<head>
  <meta http-equiv="Content-Type" content="utf-8">
  <title>###THE_TITLE###</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> 
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script> 
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
body {
  font-family: 'Helvetica', 'Arial', sans-serif;
  max-width: 767px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 10px;
  padding-right: 10px;
}

h1 {
  font-weight: bold;
  font-size: 22px;
  margin: 20px 0;
  text-align: left;
}
h2 {
  font-weight: bold;
  font-size: 18px;
  margin: 20px 0;
  text-align: left;
}
h3 {
  font-weight: bold;
  font-size: 16px;
  margin: 20px 0;
  text-align: left;
}
h4 {
  font-weight: bold;
  font-size: 15px;
  margin: 20px 0;
  text-align: left;
}
h5 {
  font-size: 14px;
  margin: 20px 0;
  text-align: left;
}
h6 {
  font-size: 13px;
  margin: 20px 0;
  text-align: left;
}
p {
    margin: 10px 0;
    padding: 5px;
	font-size: 12px;
}
code{
    padding: 5px;
	color: black
}
    </style>
</head>
<body>
"""
    HTML_FOOTER = """</body>
</html>
"""

    @staticmethod
    def html_file(md: str, filename: str, title=""):
        html = Md.html_str(md, title)
        with open(filename, 'w+') as f:
            f.write(html)
        return True


    @staticmethod
    def html_str(md: str, title=""):
        html = Md.HTML_HEADER.replace("###THE_TITLE###", title)
        html += markdown.markdown(md)
        html += Md.HTML_FOOTER
        html.replace('’', '\'')
        return html
