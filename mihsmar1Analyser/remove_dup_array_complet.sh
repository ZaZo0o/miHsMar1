#!/bin/bash 
# prend en paramèrte ($1) le fichier de résultat issu de l'interface miHsmar1Viewer 


# copie l'entête du tableau dans le fichier final et rajoute ITRs vs consensus
cat $1 | awk 'NR==1 { print $0 }' > FILTERED_$1

# pour toute ligne autre que l'entête, on sauvegarde sur la première ligne les coordonnées plus le score ITRs_vs_consensus
# on regarde les coordonnées suivantes
# si ces coordonnées (début et fin) son comprise dans une fourchette de + ou - 5 autour des coordonnées sauvegardées, ça se chevauche
# on compare les score pour garder le hit avec le meilleurs
# sinon, il s'agit de nouveau hit, on l'affiche puis on sauvegarde les nouvelles coordonnées et le score

cat $1 | awk 'NR>1{ if ($3>60 && $4>60) print $0 }' | sort -n +0 -1  | awk 'NR==1{begin=$1; end=$2; score=$5; ligne=$0} 
	NR>=1{
		if ($1>(begin-5) && $1<(begin+5)) {
			if ($2>(end-5) && $2<(end+5)) {
				if ($5>=score) {
					begin=$1; end=$2; score=$5; ligne=$0
				}
			}
		}
		else {
			print ligne ; begin=$1; end=$2; score=$5; ligne=$0
		}
	}
        END { print $0
	}' >> FILTERED_$1
