#!/bin/bash
FILE=$1
echo ${FILE} >> /tmp/list_read
INDEX_SEARCH=$2
if [[ $# -lt 2 ]]
then
echo "2 needed"
exit
fi
COUNT=`head -1 $FILE  | grep -c $INDEX_SEARCH`
LINETOADD="{ \"create\": { \"_index\": \"${INDEX_SEARCH}\", \"_type\": \"doc\"}\"}"
if [[ $COUNT -eq 0 ]]
then
	echo ${FILE} >> /tmp/list_changed
	echo ${LINETOADD} > /tmp/____junk_____
	cat $FILE >> /tmp/____junk_____
	mv /tmp/____junk_____ $FILE
	echo 1
fi
echo 0
