#!/bin/bash
#Change the following properties as per your requirement
outputfolder="../samplewiki"
baseurl="http://en.wikipedia.org"
topics="topicslist.txt"
#The topics list is a plain text file with each line containing the title of the wiki article.
#--------------------------------------------------------
echo "Copying the framework..."
mkdir $outputfolder
cp -rf content  $outputfolder
cp index.html $outputfolder
echo "Retrieving the pages..."
rm imagenamefix.sh
rm toc_cd_fix.sh
LANG=en_US.UTF8  python wiki2cd.py $baseurl  $topics $outputfolder/content
echo "Fixing the links"
mv $outputfolder/content/bits.wikimedia.org $outputfolder/content/bits
perl -e "s/http:\/\/upload.wikimedia.org/upload.wikimedia.org/g"  -pi $outputfolder/content/*.html
perl -e "s/http:\/\/bits.wikimedia.org/bits/g" -pi  $outputfolder/content/*.html
perl -e "s/href=\"\//href=\"http:\/\/en.wikipedia.org\//g" -pi $outputfolder/content/*.html
#The following section of the code is required for making the content suitable for ISO9660 file system
#The CD/DVD file system has lots of limitation on filenames and directory depth.
#We are going to rename all files to numbers(eg:1234.html, 3434.jpg etc)
#Comment out the following lines if you don't want to make the repository CD read
bash imagenamefix.sh
bash toc_cd_fix.sh
rm -rf $outputfolder/content/upload.wikimedia.org
echo "---------------------------------------------"
echo "Done!"
echo "---------------------------------------------"







