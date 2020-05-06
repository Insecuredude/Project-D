#!/usr/bin/python3.8 -tt
import argparse
import urllib.request

def Connect2Web(url = "https://www.ecosia.org/images?q=plastic+bottle"):
    page = urllib.request.urlopen(url)
    web_pg = str(page.read())

    content = str.split(web_pg)
    cnt = 0
    main = False
    result = False
    maincontent = []
    results = []
    images = []
    urls = []
    for contentblck in content:
        cnt = cnt + 1
        if (contentblck == "<main"):
            main = True
        elif (contentblck == "</main>\n"):
            main = False
        if main:
            maincontent.append(contentblck)

    for maincontentblock in maincontent:
        if (maincontentblock == "class=\"image-results"):
            result = True
        elif (maincontentblock == "class=\"loading-animation"):
            result = False
        if result:
            results.append(maincontentblock)
    
    for resultblck in results:
        if "data-src=" in resultblck:
            images.append(resultblck)

    for img in images:
        rawURL = img.split("=",1)
        betterURL = rawURL[1].strip("\"")
        url = betterURL[:-3]
        if url[len(url)-1] == "i":
            urls.append(url)
    
    print(len(urls))

    f = open('urls.txt', "w")
    for url in urls:
        string = str(url) + "\n"
        f.write(string)
    f.close()


#Define a main() function that prints a litte greeting
def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", required=False,
        help="url to website to get urls from")
    args = vars(ap.parse_args())
    if args["url"]:
        Connect2Web(args["url"])
    else:
        Connect2Web()

# This is the standard boilerplate that calls the maun function.
if __name__ == '__main__':
    main()