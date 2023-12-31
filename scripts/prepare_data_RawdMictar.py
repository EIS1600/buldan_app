import re

textPath = "/Users/romanov/_EIS1600_WorkingData/buldan_app/data_initial/0900IbnCabdMuncimHimyari.RawdMictar.Shamela0001043-ara1.mARkdownSimple"
uriBase  = "0900IbnCabdMuncimHimyari.RawdMictar.Shamela0001043-ara1"
reference = "<i>Rawḍ al-miʿṭār fī ḫabar al-aqṭār</i>"


with open("template.html", "r") as f1:
    template = f1.read()
    #print(template)

bioPath = "../data/0900IbnCabdMuncimHimyari.RawdMictar/"
stylePath = "../style.css"
lenName = 350

poetryTemplate2 = '<table class="poetryTable"><tr><td>%s</td><td>%s</td></tr></table>'
poetryTemplate1 = '<table class="poetryTable"><tr><td>%s</td></tr></table>'

def processText(text):
    # clean
    text = re.sub("ms\d+|\$|Page\w+", "", text)
    text = re.sub(r"\n([^\n]+%~%)", r"\n%~% \1", text)
    #text = re.sub(r"\n([^\n]+%~%)", r"\n%~% \1", text)
    text = re.sub(r"(\w)\n(\w)", r"\1 \2", text)

    textL = text.split("\n")
    text = []
    for t in textL:
        print(t)
        if "%~%" in t: # poetry
            #input(t)
            t = re.sub("^%~%|%~%$", "", t.strip())
            #t = t.strip()
            ta = t.split("%~%")
            if len(ta) == 2:
                t = poetryTemplate2 % (ta[0], ta[1])
                #input(ta)
            elif len(ta) == 1:
                t = poetryTemplate1 % (ta[0])
                #input(ta)
            else:
                print(ta)
                #input(t)
                t = poetryTemplate1 % (t)
            text.append(t)
        else: # regular paragraph
            t = '<p class="arabic prose">%s</p>' % t
            text.append(t)
    text = "\n\n".join(text)
    # fix poetry table :: '<table class="poetryTable"><tr><td>%s</td><td>%s</td></tr></table>'
    text = re.sub('</table>\n\n<table[^>]+>', "", text)
    # page numbers
    # headers
    return(text)


def generateData(textPath):
    prosop = []

    with open(textPath, "r") as f1:
        data = f1.read()
        data = re.split(r"###\$(\d+)\$#", data)

        realData = data[1:] # odd - ids; even - text
        print(len(realData))

        for i in range(0, len(realData), 2):
            ID = realData[i]
            text = realData[i+1]
            if "$" in text:
                textFormatted = processText(text)

                final = template
                final = final.replace("#BIO#", ID)
                final = final.replace("STYLEPATH", stylePath)
                final = final.replace("FULLREFERENCE", reference)
                final = final.replace("PASSAGEURI", uriBase+"."+ID)
                final = final.replace("MAINHTMLTEXT", textFormatted)

                name = text.replace("$", "").replace("\n", " ").replace("  ", " ").strip()
                #name = name.split(".")[0]
                name = name[:85]
                name = re.sub("[A-Za-z0-9]+", "", name).replace("  ", " ")
                #if len(name) > lenName:
                #    name = name[:lenName] + "..."
                if re.search("\w$", name):
                    name = name + 'ـ'

                #input(name)

                prosop.append("%s\t%s" % (ID, name))

                with open(bioPath+ID+".html", "w") as f9:
                    f9.write(final)

        with open("../data/prosopData.tsv", "w") as f9:
            f9.write("ID\tNAME\n"+ "\n".join(prosop))

generateData(textPath)