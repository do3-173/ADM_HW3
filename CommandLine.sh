cat TSV/course_1.tsv > merged_courses.tsv
for i in {2..6000}
do
   tail -n +2 TSV/course_${i}.tsv >> merged_courses.tsv
done
echo -n "Country: "
cut -f11 merged_courses.tsv | sort | uniq -c | sort -nr | head -1 | awk '{count=$1; $1=""; sub(/^ /,""); print $0 ", number of occurrences: " count}'
echo -n "City: "
cut -f10 merged_courses.tsv | sort | uniq -c | sort -nr | head -1 | awk '{count=$1; $1=""; sub(/^ /,""); print $0 ", number of occurrences: " count}'
part_time=$(awk -F'\t' 'tolower($X) ~ /part[- ]time/ {print $2}' merged_courses.tsv | sort | uniq | wc -l)
echo "Number of universities that give part time: ${part_time}" 
total_courses=$(wc -l < merged_courses.tsv)
engineering_courses=$(awk -F '\t' 'tolower($1) ~ /engineer/' merged_courses.tsv | wc -l)
echo "Percentage of engineering courses: $(echo "scale=2; $engineering_courses * 100 / $total_courses" | bc) %"
