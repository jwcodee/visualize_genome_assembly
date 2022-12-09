library(chromPlot)

# parse arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: Rscript chromplot.R <input_bed> <output_file>")
}


input <- read.delim(args[1], header = FALSE)
colnames(input) <- c(
  "Chrom", "Start", "End",
  "Name", "Qual", "Strand", "Colors"
)
png(args[2], width = 6, height = 5, units = "in", res = 1200)
chromPlot(bands = input, title = "Ideogram")
dev.off()
