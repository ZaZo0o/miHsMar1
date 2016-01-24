#!/bin/bash
# Parameters: 1-> directory containing xml files from Logol

xmlDir=$1


for xml in $xmlDir*.xml; do
	cd mihsmar1Analyser
	./get_array_complet.sh $xml &&
	cd ..
done

exit
