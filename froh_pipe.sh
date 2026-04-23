#!/bin/bash
set -euo pipefail

### RUN ROH
bcftools roh --AF-tag AF --rec-rate 1e-8 autosomes.af.vcf.gz > roh.txt

### ROH PER INDIVIDUAL
awk '$1=="RG"{sum[$2]+=$6} END{for (i in sum) print i, sum[i]}' roh.txt > roh_total_bp.txt

###COMPUTE GENOME LENGTH
# compute autosomal genome length (sum of contig lengths in header, excluding Z)
Z=$(cat sex_chr.txt)

bcftools view -h autosomes.vcf.gz | \
grep '^##contig' | \
grep -v "$Z" | \
sed 's/.*length=//' | sed 's/>//' | \
awk '{sum += $1} END {print sum}' > genome_bp.txt

GENOME_BP=$(cat genome_bp.txt)

### COMPUTE FROH
awk -v G=$GENOME_BP '{print $1, $2/G}' roh_total_bp.txt > froh.txt

### MERGE WITH POPULATION DATA
cut -d',' -f1,2 buow_withpop.csv | tail -n +2 | sed 's/,/ /g' > id_pop.txt

sort froh.txt > froh.sorted.txt
sort id_pop.txt > id_pop.sorted.txt
join froh.sorted.txt id_pop.sorted.txt > froh_with_pop.txt

### POPULATION SUMMARY
awk '{
  pop=$3;
  val=$2;
  sum[pop]+=val;
  sumsq[pop]+=val*val;
  count[pop]+=1
}
END {
  for (p in sum) {
    mean=sum[p]/count[p];
    var=(sumsq[p]/count[p])-(mean*mean);
    sd=sqrt(var);
    print p, count[p], mean, sd
  }
}' froh_with_pop.txt > pop_froh_summary.txt

### FLAG SMALL GROUPS
awk '{
  if ($2 < 5) print $1"*", $2, $3, $4;
  else print $1, $2, $3, $4;
}' pop_froh_summary.txt > pop_froh_final.txt
