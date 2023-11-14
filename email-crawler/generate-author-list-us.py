import csv
import gzip

from lxml import etree as ElementTree

filename = "dblp_names_us.csv"
def parseDBLP(filename):
    # with open('dblp.xml', mode='r') as f:
    print("alias,name")
    csv.writer(open(filename, "w")).writerow(['alias', 'school'])

    dtd = ElementTree.DTD(file="dblp.dtd")
    with gzip.open("dblp.xml.gz", mode="rb") as f:
        # with open("dblp.xml", mode="r", encoding="utf-8") as f:

        oldnode = None

        for (event, node) in ElementTree.iterparse(
            f, events=["start", "end"], load_dtd=True
        ):

            if oldnode is not None:
                oldnode.clear()
            oldnode = node
            authors = 0
            schools = 0
            authorList = []
            schoolList = []
            # ATTEMPT TO REMOVE THESE LIMITS
            if node.tag != "www":
                continue

            # print("FIND: ", node.findtext("author", default="None"))
            # print("DATE", node.get("mdate", ""))
            # print("KEY", node.get("key",""))

            # Skip non-home page entries.
            if not node.get("key", "").startswith("homepages/"):
                continue

            # print("WWW")
            # print(node.getchildren())
            for child in node.getchildren():
                # from pprint import pprint
                # print(child)
                # print(child.tag)
                # print(child.findtext("author", "NOTEXT"))
                if child.tag != "author":
                    continue
                # print(dir(child))
                # print("AUTHOR", child.text)
                # print(dir(child))
                # print("WWW adding", child.text)
                authorName = child.text
                if not authorName:
                    continue
                # print("ADDING ", authorName)
                authorName = authorName.strip()
                authors += 1
                authorList.append(authorName.encode("utf-8"))
                # print("author list", authorList)

            if not authors:
                continue
            for child in node.getchildren():
                if child.tag != "school":
                    continue
                school = child.text
                if not school:
                    continue
                schools += 1
                school = school.strip
                schoolList.append(school.encode("utf-8"))
            # print("AUTHORS", authorList)
            if not schools:
                continue
            if schools == authors:
                pairs = [(authorList[i], schoolList[i]) for i in range(0, schools)]
            else:
                print("schools: " + str(schools) + ", authors: " + str(authors))
                return
            file = open(filename, "a")
            for p in pairs:
                csv.writer(file).writerow([p[0], p[0]])
                print(p[1].decode("utf-8") + "," + p[0].decode("utf-8"))
            file.close()


parseDBLP(filename)