#/bin/bash

curl -G "http://0.0.0.0:8000/" \
    --data-urlencode "sort[0]=title:asc" \
    --data-urlencode "filters[title][\$eq]=hello" \
    --data-urlencode "populate[author][fields][0]=firstName" \
    --data-urlencode "populate[author][fields][1]=lastName" \
    --data-urlencode "fields[0]=title" \
    --data-urlencode "pagination[pageSize]=10" \
    --data-urlencode "pagination[page]=1" \
    --data-urlencode "publicationState=live" \
    --data-urlencode "locale[0]=en" \
    --data-urlencode "test[0][foo]=bar" \
    --data-urlencode "test[1][0]=test"
