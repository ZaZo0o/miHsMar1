#!/bin/bash
# $1-> path to the xml file

# Initiate variables
xmlFile=../$1
workingDir=`basename ../$xmlFile`
currentPath=`pwd`

echo ""
echo "Start analysing $workingDir"
echo ""


# Create working directory containing temporary files
if [ ! -d "$workingDir" ]; then
	mkdir $workingDir
fi


# Associative table:
#   key == script
#   value == message to print in the terminal

declare -A align_scripts
align_scripts[get_sequence.py]="Extract sequences for each match"
align_scripts[get_coord.py]="Extract match coordinates"
align_scripts[get_score_itr1.py]="Align first ITRs"
align_scripts[get_score_itr2.py]="Align second ITRs"
######################################################################################
# align_scripts[get_score_linker_oriented.py]="Align Linkers"
# align_scripts[get_size_linker.py]="Get linker size"
# align_scripts[get_coord_linker.py]="Extract linker coordinates"
######################################################################################

echo ""


align_matches (){
	declare -A pid_scripts
	for script in "${!align_scripts[@]}"; do
		echo "Run ${align_scripts[$script]}..."
		python $script $xmlFile $currentPath $workingDir &
		pid_scripts[${align_scripts[$script]}]=$!
	done

	echo ""
	for pid in "${!pid_scripts[@]}"; do
		while kill -0 ${pid_scripts[$pid]} 2> /dev/null; do
	    echo -en "$pid... /\033[1G" ; sleep .09
	    echo -en "$pid... -\033[1G" ; sleep .09
	    echo -en "$pid... \ \033[1G" ; sleep .09
	    echo -en "$pid... |\033[1G" ; sleep .09
		done &&
		echo "$pid DONE"
	done
}

align_matches


sh get_score_itrs.sh $workingDir &&


######################################################################################
# sh get_score_full.sh $workingDir &&

# echo "Run Align ITR1 vs ITR2..."
# python get_score_itr1_vs_itr2.py $xmlFile $currentPath $workingDir &
# 	pid=$!
# 	# If this script is killed, kill the `cp'.
# 	trap "kill $pid 2> /dev/null" EXIT
# 	# While script is running...
# 	while kill -0 $pid 2> /dev/null; do
# 	    echo -en "Running... /\033[1G" ; sleep .09
# 	    echo -en "Running... -\033[1G" ; sleep .09
# 	    echo -en "Running... \ \033[1G" ; sleep .09
# 	    echo -en "Running... |\033[1G" ; sleep .09
# 	done &&
# 	# Disable the trap on a normal exit.
# 	trap - EXIT
# 	echo "Running... DONE"
######################################################################################


paste $workingDir/coord.tmp $workingDir/score_itr1.tmp $workingDir/score_itr2.tmp $workingDir/score_itrs.tmp > $workingDir/RESULT_$workingDir.txt

######################################################################################
# $workingDir/score_inter_itrs.tmp \
# $workingDir/score_linker.tmp \
# $workingDir/score_full.tmp \
# $workingDir/nb_id_itr1.tmp \
# $workingDir/nb_id_linker.tmp \
# $workingDir/nb_id_itr2.tmp \
# $workingDir/size_linker.tmp \
# $workingDir/coord_Linker.tmp \
# $workingDir/sequences.tmp \
# > $workingDir/RESULT_$workingDir.txt
######################################################################################

cd $workingDir/
	sh ../remove_dup_array_complet.sh RESULT_$workingDir.txt
cd ..

cp -rf $workingDir ../Results
rm ../Results/$workingDir/*.tmp
rm ../Results/$workingDir/*.et
rm ../Results/$workingDir/*.fasta

# rm $workingDir

echo "$workingDir analysis COMPLETE!"
echo ""
exit

