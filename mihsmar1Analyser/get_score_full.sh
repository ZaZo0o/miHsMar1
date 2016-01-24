#!/bin/bash

cd $1

paste nb_id_itr1.tmp nb_id_itr1.tmp nb_id_itr1.tmp | awk 'NR==1{print "Score_full"} NR>1 {print (($1+$2+$3)/90)*100}' > score_full.tmp
