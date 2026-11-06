# RB application logic: total encoded payload bytes by codec.
read "benchmark.csv"
csv
group-stats codec bytes
sort-by sum asc
emit
