html = """
<html>
    <head>
        <meta charset="utf-8">
    </head>

    <body>
        <font color=red> @title</font>
    <table border=1>
            <tr bgcolor=yellow>
                <td> 이름 </td>  <td> @name </td> 
            </tr>  
            <tr>
                <td> email </td>  <td> @email </td> 
            </tr>
    </table>
    </body>
</html>
"""

html = html.replace("@title",  "네덜란드 암스테르담")
html = html.replace("@name",  "박윤수")
html = html.replace("@email",  "tlgus1995@gmail.com")

print(html)


def renderfile(file, data):
    html = open(file, "rt", encoding="utf-8").read()
    for v in data:
        html = html.replace("@"+v, data[v])
    return html

data = {"title":"네덜란드 암스테르담", "name":"박윤수", "email":"tlgus1995@gmail.com"}
print(renderfile("template.html", data))