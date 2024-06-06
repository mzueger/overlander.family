from datetime import datetime
from pyquery import PyQuery    

def toSeoFriendly(s, maxlen):
    t = '-'.join(s.split())                                # join words with dashes
    u = ''.join([c for c in t if c.isalnum() or c=='-'])   # remove punctation   
    return u[:maxlen].rstrip('-').lower()                  # clip to maxlen

def outputFileName(title):
    return toSeoFriendly(title, 128)

def cleanupAuthor(author):
    if author.find("franzi"):
        return "Fränzi"
    if author.find("martin"):
        return "Martin"
    return "unknown"

def datePrefix(dtStr):
    dt = datetime.fromisoformat(dtStr)
    return dt.strftime("%Y-%m")

def cleanupImagePath(path):
    start = path.find("/")
    if start != -1:
        return path[start + 1:]
    else:
        return path

def cleanupPublishedDate(datetime):
    end = datetime.find("+")
    if end != -1:
        return datetime[:end]
    else:
        return datetime

inputDirPath = "D:/Private/overlander.family/import"
inputFileName = "Bolivien Zwei Rheintaler unterwegs.htm"
outputDirPath = "D:/Private/overlander.family/source/_posts"

html = PyQuery(filename=inputDirPath + "/" + inputFileName, encoding='utf-8')

author = html('span.username').text()
title = html('h1#page-title').text()
published = html('p.submitted>time').attr['datetime']
titleImg = html('div.field-name-field-title-img>div>div>img').attr['src']
period = html('div.field-name-field-period').text()
mainContent = html('article.node-blog-entry').remove('header').remove('div.field-name-field-title-img').remove('div.field-name-field-period').remove("div.view-photo-gallery").remove("div.field-name-field-tags").remove("ul.links.inline")
text = mainContent("div.field-name-body>div>div").html().replace("<h2>", "\n## ").replace("</h2>", "\n").replace("<p>", "").replace("</p>", "\n\n").replace("<i>", "_").replace("</i>", "_").replace("&amp;", "&").replace("&nbsp;", " ").replace("<sup>2</sup>", "²")

with open(outputDirPath + "/" + outputFileName(title) + ".md", "w", encoding='utf-8') as output:
    output.write("---\n")
    output.write("title: " + title + "\n")
    output.write("tags:\n")
    output.write("  - Südamerika\n")
    output.write("category:\n")
    output.write("  - Reiseberichte\n")
    output.write("  - Panamericana 2015/2016\n")
    output.write("date: " + cleanupPublishedDate(published) + "\n")
    output.write("author:\n")
    output.write("  name:" + cleanupAuthor(author) + "\n")
    output.write("published: false\n")
    output.write("---\n")
    output.write("\n")
    output.write("![](images/" + datePrefix(published) + "_" + outputFileName(title) + "/" + cleanupImagePath(titleImg) + ")\n")
    output.write("\n")
    output.write(period.replace('\n', ' ') + " - geschrieben von " + cleanupAuthor(author) + "\n")
    output.write("\n")
    output.write(text)
    output.close()
