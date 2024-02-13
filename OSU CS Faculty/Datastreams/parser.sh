#!/bin/bash

cat Raw?.txt | grep 'hreflang="en">' | sed '/<\/a>$/!d' | sed -r 's#.*>(.*)<\/a>#\1#' > Names1.txt
cat Raw?.txt | grep 'mailto' | sed -e 's#.*mailto:\(.*\)".*#\1#' > Emails1.txt
sed '1i\site title,email found' merged.csv | sed 'G' > ../osu-emails.csv
