#made using https://github.com/goldsmith/Wikipedia

import wikipedia
import urllib
import urllib2
import json
import threading

def main():
	open("logos/notfound.txt", 'w').close()
	brandNames = [line.strip() for line in open('brands.txt')]
	for brand in brandNames:
		thr = threading.Thread(target=getCompanyLogo, args = [brand])
		thr.start()

def getCompanyLogo(companyName):
	try:
		logoURL = None
		if logoURL == None:
			#using google as a fallback
			print(companyName+ " logo")
			logoURL = google_image(companyName+" logo")
		if logoURL == None:
			logoURL = getWikiLogoURL(companyName)
		if logoURL == None:
			addToNotFoundList(companyName)
			return

		urllib.urlretrieve(logoURL, "logos/"+companyName+getExtension(logoURL))
		print(logoURL)
	except:
		addToNotFoundList(companyName)
		return

#to do ensure its in the class logo
def getWikiLogoURL(pageName):
	try:
		myPage = wikipedia.page(pageName)
		imageUrls = myPage.images
		logoLinks = []
		for url in imageUrls:
			lowerCaseUrl = url.lower();
			if "commons-logo" not in lowerCaseUrl and "-logo" not in lowerCaseUrl and "_logo" in lowerCaseUrl and ".svg" in lowerCaseUrl:
				logoLinks.append(url)
		print(logoLinks)
		return logoLinks[0]
	except:
		return None
def google_image(x):
        search = x.split()
        search = '%20'.join(map(str, search))
        print(search)
        url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s&safe=off' % search
        search_results = urllib2.urlopen(url)
        js = json.loads(search_results.read().decode())
        results = js['responseData']['results']
        for i in results: 
        	rest = i['unescapedUrl']
        	print(rest)
        	break
        print(rest)
        return rest
def getExtension(url):
	for i in range(len(url)-1, -1, -1):
		if url[i] == '.':
			return url[i:]
def addToNotFoundList(companyName):
	f = open("logos/notfound.txt", 'a')
	f.write(companyName+"\n")
	f.close()

main()