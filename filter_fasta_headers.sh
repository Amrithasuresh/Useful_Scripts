# Filter multi-entry .fasta file by partial match to id line in bash
# https://stackoverflow.com/questions/60386496/filter-multi-entry-fasta-file-by-partial-match-to-id-line-in-bash

awk 'BEGIN {RS = "(^|\n)>"}
   /3C/ {
        sub(/\n$/, "");
        print ">" $0
   }
' protein.faa > 3c-like.faa
