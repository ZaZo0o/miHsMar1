library("ggplot2")
library("taRifx")

args <- commandArgs(trailingOnly = TRUE)

# resultDir <- args[1]
resultDir <- "Results"

dirs <- dir(resultDir, pattern="^chr[[:alnum:]]")



plot_raw_distribution <- function(file, chr){

	raw_data <- read.csv(file , header=TRUE, sep="\t")

	pdf(paste(file, ".pdf", sep="") , width=9, height=7)

	bad_matches <- length(raw_data[raw_data$Score_ITRs_vs_consensus<75, 1])
	good_matches <- length(raw_data[raw_data$Score_ITRs_vs_consensus>=75, 1])

	dat <- data.frame(Percentage_Idenity=raw_data$Score_ITRs_vs_consensus, above=raw_data$Score_ITRs_vs_consensus>=75)

	q <- qplot(Percentage_Idenity,data=dat,geom="histogram",fill=above, binwidth = 1.8,col=I("black")) + 
		scale_fill_manual(values = c("#af1753","#72d6ed"), labels = c(paste("Null confidence matches (", bad_matches, ")    ", sep=""), paste("Confidence matches (", good_matches, ")", sep=""))) +
		guides(fill=guide_legend(title=NULL)) +
		theme_bw() +
		ggtitle(paste('Old miHsMar1 model on ', chr,' Hg38\n(', length(raw_data$Score_ITRs_vs_consensus) , ' matches)\n', sep="")) +
		theme(plot.title = element_text(size=15, face="bold", vjust=2),legend.position="bottom") +
		ylab("Frequency") +
		xlab("Percentage of identity of the two ITRs")+
		theme(axis.title.x = element_text(size=20),
	          axis.text.x  = element_text(size=16),
			  axis.title.y = element_text(size=20),
	          axis.text.y  = element_text(size=16),
	          plot.title=element_text(size=20),
	          legend.text=element_text(size=16))

	print(q)

	dev.off()

}

plot_filtered_distribution <- function(file, chr){
	filtered_data <- read.csv(file , header=TRUE, sep="\t")

	pdf(paste(file, ".pdf", sep="") , width=9, height=7)

	bad_matches <- length(filtered_data[filtered_data$Score_ITRs_vs_consensus<75, 1])
	good_matches <- length(filtered_data[filtered_data$Score_ITRs_vs_consensus>=75, 1])

	dat <- data.frame(Percentage_Idenity=filtered_data$Score_ITRs_vs_consensus, above=filtered_data$Score_ITRs_vs_consensus>=75)

	q <- qplot(Percentage_Idenity,data=dat,geom="histogram",fill=above, binwidth = 1.8,col=I("black")) + 
		scale_fill_manual(values = c("#af1753","#72d6ed"), labels = c(paste("Null confidence matches (", bad_matches, ")    ", sep=""), paste("Confidence matches (", good_matches, ")", sep=""))) +
		guides(fill=guide_legend(title=NULL)) +
		theme_bw() +
		ggtitle(paste('Old miHsMar1 model on ', chr,' Hg38\n(', length(filtered_data$Score_ITRs_vs_consensus) , ' matches)\n', sep="")) +
		theme(plot.title = element_text(size=15, face="bold", vjust=2),legend.position="bottom") +
		ylab("Frequency") +
		xlab("Percentage of identity of the two ITRs")+
		theme(axis.title.x = element_text(size=20),
	          axis.text.x  = element_text(size=16),
			  axis.title.y = element_text(size=20),
	          axis.text.y  = element_text(size=16),
	          plot.title=element_text(size=20),
	          legend.text=element_text(size=16))

	print(q)


	dev.off()

}


generate_gff_high_confident <- function(file, chr){
	filtered_data <- read.csv(file , header=TRUE, sep="\t")
	high_confident_matches <- filtered_data[filtered_data$Score_ITRs_vs_consensus>=75,]
	if (length(filtered_data$Score_ITRs_vs_consensus>=75)>0){
		seqname <- rep_along(chr,high_confident_matches$Score_ITRs_vs_consensus)
		source <- rep_along("Logol",high_confident_matches$Score_ITRs_vs_consensus)
		feature <- rep_along("high_confident_match",high_confident_matches$Score_ITRs_vs_consensus)
		start <- high_confident_matches$Begin
		end <- high_confident_matches$End
		score <- high_confident_matches$Score_ITRs_vs_consensus
		strand <- rep_along(".",high_confident_matches$Score_ITRs_vs_consensus)
		frame <- rep_along(".",high_confident_matches$Score_ITRs_vs_consensus)
		attribute <- paste("ITR1_ID:",high_confident_matches$Score_ITR1,"; ","ITR2_ID:",high_confident_matches$Score_ITR2,";", sep="")

		gff_high_confident <- cbind(
			seqname,
			source,
			feature,
			start,
			end,
			score,
			strand,
			frame,
			attribute
			)
	} else {
		gff_high_confident <- data.frame(matrix(ncol = 9, nrow = 0))
	}
	write.table(gff_high_confident, paste(file, ".gff", sep=""), sep="\t", col.names = F, row.names = F, quote=FALSE)
	return(gff_high_confident)
}



for (chr in dirs) {
	raw_results <- paste(resultDir, chr, list.files(path=paste(resultDir, chr, sep="/"), pattern="^RESULT_[[:print:]]+txt$"), sep="/")
	filtered_results <- paste(resultDir, chr, list.files(path=paste(resultDir, chr, sep="/"), pattern="^FILTERED_RESULT_[[:print:]]+txt$"), sep="/")
	chr_nb <- unlist(strsplit(chr, "[.]"))[1]
	plot_raw_distribution(raw_results, chr_nb)
 	plot_filtered_distribution(filtered_results, chr_nb)
}


gff <- data.frame(matrix(ncol = 9, nrow = 0))
for (chr in dirs) {
	filtered_results <- paste(resultDir, chr, list.files(path=paste(resultDir, chr, sep="/"), pattern="^FILTERED_RESULT_[[:print:]]+txt$"), sep="/")
	chr_nb <- unlist(strsplit(chr, "[.]"))[1]
	current_chr <- generate_gff_high_confident(filtered_results, chr_nb)
	gff <- rbind(gff, current_chr)
}

write.table(gff, "Hg38_all_chr_High_confident_matches_logol_above_75_percent.gff", sep="\t", col.names = F, row.names = F, quote=FALSE)

