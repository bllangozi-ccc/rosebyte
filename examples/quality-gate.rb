# Application logic written in RB: find failed or slow checks by stage.
read "test-results.csv"
csv
where-any status ne pass duration_ms gt 3000
group-stats stage duration_ms
sort-by sum desc
emit
