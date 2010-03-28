#!/bin/bash
outputfolder="../wiki"
baseurl="http://ml.wikipedia.org"
topics="topicslist.txt"
#--------------------------------------------------------
echo "Copying the framework..."
mkdir $outputfolder
cp -rf content  $outputfolder
cp index.html $outputfolder
echo "Normalising the topics file"
#To be changed according to the language
perl -e "s/ൽ/ല്‍/g;" -pi $topics
perl -e "s/ൾ/ള്‍/g;" -pi $topics
perl -e "s/ൻ/ന്‍/g;" -pi $topics
perl -e "s/ർ/ര്‍/g;" -pi $topics
perl -e "s/ൺ/ണ്‍/g;" -pi $topics
perl -e "s/ൿ/ക്‍/g;" -pi $topics
perl -e "s/ന്‍റ/ന്റ/g;" -pi $topics
echo "Retrieving the pages..."
LANG=en_US.UTF8  python grab_pages.py $baseurl  $topics $outputfolder/content
#Normalize the retrieved pages
#To be changed according to the language
perl -e "s/ൽ/ല്‍/g;" -pi $outputfolder/content/*.html
perl -e "s/ൾ/ള്‍/g;" -pi $outputfolder/content/*.html
perl -e "s/ൻ/ന്‍/g;" -pi $outputfolder/content/*.html
perl -e "s/ർ/ര്‍/g;" -pi $outputfolder/content/*.html
perl -e "s/ൺ/ണ്‍/g;" -pi $outputfolder/content/*.html
perl -e "s/ൿ/ക്‍/g;" -pi $outputfolder/content/*.html
perl -e "s/ന്‍റ/ന്റ/g;" -pi $outputfolder/content/*.html
echo "Fixing the links"
perl -e "s/http:\/\/upload.wikimedia.org/upload.wikimedia.org/g"  -pi $outputfolder/content/*.html
perl -e "s/http:\/\/bits.wikimedia.org/bits.wikimedia.org/g" -pi  $outputfolder/content/*.html
perl -e "s/href=\"\//href=\"http:\/\/ml.wikipedia.org\//g" -pi $outputfolder/content/*.html
perl -e "s/href=\"http:\/\/ml.wikipedia.org\//href=\"http:\/\/ml.wikipedia.org\//g" -pi $outputfolder/content/*.html


