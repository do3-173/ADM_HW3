cat TSV/course_1.tsv > merged_courses.tsv
for i in {2..6000}
do
   tail -n +2 TSV/course_${i}.tsv >> merged_courses.tsv
done
echo -n "Country that offers most Master's Degrees: "
cut -f11 merged_courses.tsv | sort | uniq -c | sort -nr | head -1 | awk '{print substr($0, index($0,$2)) ", number of occurrences: " $1}'
echo -n "City that offers most Master's Degrees: "
cut -f10 merged_courses.tsv | sort | uniq -c | sort -nr | head -1 | awk '{print substr($0, index($0,$2)) ", number of occurrences: " $1}'
part_time=$(awk -F'\t' 'tolower($0) ~ /part[- ]time/ {print $2}' merged_courses.tsv | sort | uniq | wc -l)
echo "Number of universities that offer part-time courses: ${part_time}"
total_courses=$(awk -F'\t' 'NR > 1 && $1 != ""' merged_courses.tsv | wc -l)
engineering_courses=$(awk -F '\t' 'tolower($1) ~ /engineer/' merged_courses.tsv | wc -l)
percentage=$(echo "scale=2; $engineering_courses * 100 / $total_courses" | bc)
echo "Percentage of engineering courses: $percentage%"