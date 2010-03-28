# -*- coding: utf-8 -*-
"""
  Copyright (c) 2010 Santhosh Thottingal

  This is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3.0 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import codecs
import urllib
import urllib2
import os,sys
from sgmllib import SGMLParser
class ImageLister(SGMLParser):
	def reset(self):                              
		SGMLParser.reset(self)
		self.images = []
	def start_img(self, attrs):         
		src = [v for k, v in attrs if k=='src'] 
		if src:
			self.images.extend(src)
def maketoc(topicslist,toc_filename):
	ensure_dir(toc_filename)
	toc_file = codecs.open(toc_filename, "w", "utf-8")
	fp = codecs.open(topicslist, "r", "utf-8")
	toc_header=u"""
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
						"http://www.w3.org/TR/html4/loose.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ml" lang="ml" dir="ltr">
	<head>
	  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	   <script src="js/jquery-latest.js"></script>
	   <script src="js/swanalekha-ml.js"></script>
	  <link rel="stylesheet" href="css/jquery.treeview.css" type="text/css" />
	   <script type="text/javascript" src="js/jquery.treeview.js"></script>
	  <script type='text/javascript' src='js/jquery.autocomplete.js'></script>
	  <link rel="stylesheet" type="text/css" href="css/jquery.autocomplete.css" />
	<!--[if IE]>
		  <style type="text/css">
			@font-face {
			  font-family: Meera;
			  src: url("css/Meera_04-2.eot");
			}
		  </style>
	   <![endif]-->
		<style type="text/css">
		  @font-face {
			font-family: Meera;
			src: local('Meera'), url('css/Meera_04-2.ttf') format("truetype");
		  }
		body {
		/*font: x-small sans-serif;*/
		font: normal normal 120% Meera;
		background: #f9f9f9 url(headbg.jpg) 0 0 no-repeat;
		color: black;
		margin: 0;
		padding: 0;

		}
		 </style>
	  <script>
	  $(document).ready(function(){
		$("#example").treeview();
	  });
	  </script>

	</head>
	<body>
	<form action="" onsubmit="return false;">
	<input type="text" value="" id="topicsearch"/>
	<input type="button" id="searchbox" value="Go" name="പോകൂ" onclick="lookupLocal();"/>
	</form>
	<br/>
	<hr/>
	<h2>ഉള്ളടക്കം</h2>
	  <ul id="example" class="filetree">
	"""
	toc_footer ="""
	</li>
	</ui>
	<script type="text/javascript">
	function findValue(li) {
		if( li == null ) return alert("No match!");

		// if coming from an AJAX call, let's use the CityId as the value
		if( !!li.extra ) var sValue = li.extra[0];

		// otherwise, let's just display the value in the text box
		else var sValue = li.selectValue;
		parent.content.location.href = sValue.replace(/\ /g , "_") +".html";
	}

	function selectItem(li) {
		findValue(li);
	}

	function formatItem(row) {
		return row[0] + " (id: " + row[1] + ")";
	}
	function lookupLocal(){
		var oSuggest = $("#topicsearch")[0].autocompleter;

		oSuggest.findValue();

		return false;
	}

	$(document).ready(function() {
		var optionTexts = [];
		$("a").each(function() { optionTexts.push($(this).html()) });
		$("#topicsearch").autocompleteArray(
			optionTexts		,
			{
				delay:10,
				minChars:1,
				matchSubset:1,
				onItemSelect:selectItem,
				onFindValue:findValue,
				autoFill:false,
				maxItemsToShow:10
			}
		);
	});
	</script>
	</body>
	</html>
	"""
	toc_file.write(toc_header)
	index = 0
	currentlevel = 0
	previouslevel = -1
	atleaf = False
	while 1:
		text = unicode(fp.readline())
		text= text.strip()
		if text.strip() == "": 
			break
		if text.count("=") > 0:
			currentlevel =  text.count("=")
			text = text.replace("=","")
			leveldiff = previouslevel-currentlevel
			if leveldiff == 0:
				leveldiff = 1
			if atleaf:
				leveldiff =currentlevel-1		
			if atleaf and previouslevel-currentlevel == 0:
				leveldiff = 1		
			if previouslevel-currentlevel > 0:
				leveldiff = -1				
			if atleaf and previouslevel-currentlevel > 0:
				leveldiff = -1				
			if atleaf and previouslevel-currentlevel < 0:
				leveldiff = 2					
			#print previouslevel , " > " , currentlevel , " : ",	leveldiff ,atleaf
			for i in range(0,leveldiff):
				toc_file.write("</ul>\n")
				toc_file.write("</li>\n")
			toc_file.write("<li class='closed'><span class='folder'>"+text+"</span>\n")
			toc_file.write("<ul>\n")
			previouslevel = currentlevel
			atleaf = False	
			continue
		atleaf = True
		link = text.strip().replace(" ", "_")
		toc_file.write("<li><span class='file'><a href='"+link+".html' target='content'>"+text+"</a></span></li>\n")
	toc_file.write(toc_footer+"\n")
	toc_file.close()

def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

def grab_pages(wikibase, topicslist,outputfolder):
	fp = codecs.open(topicslist, "r", "utf-8")
	while 1:
		try:	
			text = unicode(fp.readline())
			text= text.strip()
			if text.strip() == "": 
				break
			if text[0]== "=": 
				continue
			link = text.replace(" ", "_")
			grab_page(wikibase, wikibase + "/wiki/"+link,outputfolder)
		except KeyboardInterrupt:
			return 

def grab_page(wikibase, pagelink,outputfolder):
	metacontent ="""
	<hr/>
	<ul>
	<li><a href="$ONWIKI$" target="_blank" class="metalinks">ഈ ലേഖനത്തിന്റെ ഏറ്റവും പുതിയ പതിപ്പു് മലയാളം വിക്കിപീഡിയയില്‍ വായിക്കുക</a></li>
	<li><a href="http://toolserver.org/~daniel/WikiSense/Contributors.php?wikilang=ml&wikifam=.wikipedia.org&since=&until=&grouped=on&order=-edit_count&max=100&order=-edit_count&format=html&page=$PAGE$" target="_blank"  class="metalinks">ഈ ലേഖനത്തിന്റെ രചനയില്‍ പങ്കെടുത്തവര്‍</a></li>
	<ul>
	"""
	try:
		link= pagelink.strip()
		parts = link.split("/")	
		filename = parts[len(parts)-1]	 
		print "GET " + link + " ==> " + outputfolder + "/"+ filename+  ".html"
		if os.path.isfile(outputfolder + "/"+ filename+  ".html"):
			print "File " + outputfolder + "/"+ filename+  ".html" + " already exists"
			return
		quotedfilename = urllib.quote(filename.encode('utf-8')) 
		link = wikibase +"/wiki/"+quotedfilename
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		infile = opener.open(link)
		page = infile.read()
		parser = ImageLister()
		parser.feed(page)        
		parser.close()
		f= open(outputfolder + "/"+ filename+  ".html",'w')
		metacontent = metacontent.replace("$ONWIKI$",link)
		metacontent = metacontent.replace("$PAGE$",quotedfilename)
		page = page.replace("</body></html>",metacontent+"</body></html>")
		f.write(page)
		f.close()
		for image in parser.images: 
			if not image[0]=="/"	: #relative reference
				grab_image(image,outputfolder)
		
	except KeyboardInterrupt:
		sys.exit()
	except urllib2.HTTPError:
		print("Error: Could not download the page")
		pass

def grab_image(imageurl,outputfolder):
	try:
		link= imageurl.strip()
		parts = link.split("/")	
		filename = parts[len(parts)-1]	 
		output_filename =str(outputfolder + "/" + link.replace("http://",""))
		output_filename=urllib.unquote(output_filename) 
		print "GET IMAGE " + link + " ==> " + output_filename
		if os.path.isfile(output_filename):
			print "File " + output_filename + " already exists"
			return 
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		infile = opener.open(link)
		page = infile.read()
		ensure_dir(output_filename)
		f= open(output_filename,"w")
		f.write(page)
		f.close()
	except KeyboardInterrupt:
		sys.exit()
	except urllib2.HTTPError:
		print("Error: Cound not download the image")
		pass
	
if __name__ == '__main__':
    if len(sys.argv)> 2:
        wikibase = sys.argv[1]
        topicslist = sys.argv[2]
        outputfolder = sys.argv[3]
        maketoc(topicslist,outputfolder+"/toc.html")
        grab_pages(wikibase,topicslist,outputfolder)
    else:
		print("Error: Missing arguments. Eg usage: toc_maker.py http://ml.wikipedia.org topics.txt toc.html")

