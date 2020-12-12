
cookie=`cat auth.txt`
curl "https://www.geoguessr.com/api/v3/social/feed/?count=$1&page=$2" \
  -H 'authority: www.geoguessr.com' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' \
  -H 'content-type: application/json' \
  -H 'accept: */*' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.geoguessr.com/me/activities' \
  -H 'accept-language: en-US,en;q=0.9,nl;q=0.8,de;q=0.7' \
  -H $cookie \
  --compressed