for i in `ls -d /tmp/JUNKS* `
do
	echo "DO CURL FOR $i"
	for j in `ls $i/*`
	do 
		echo $j
	#	curl -s -XPOST localhost:9200/_bulk --data-binary @srajend2_1000.json
	done
done
