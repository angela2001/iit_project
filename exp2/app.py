# TEMPLATE="""
#     Hello {name}
# """

# def main():
#     print(TEMPLATE.format(name="JJ"))



#TEMPLATE="""This is {p:+} and this is {n:x}"""

from jinja2 import Template

#TEMPLATE=""" hello world {{name}}"""
#TEMPLATE="""This is {{p}} and this is {{n}}"""


a=[{"a1":10,"a2":20,"a3":30},{"a1":40,"a2":50,"a3":60},{"a1":70,"a2":80,"a3":90}]

  
def main():
    templateFile=open("template.html.jinja2")
    temp= templateFile.read()
    template =Template(temp)
    templateFile.close()
    #print(template.render(a=a))
    content= template.render(a=a)
    htmlDoc=open('a.html','w')
    htmlDoc.write(content)
    htmlDoc.close()

if __name__=="__main__":
    main()