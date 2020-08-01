ECHO Create 2 stores

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"address": "37.3327° N, 122.0053° W",  "name": "Apple Park Visitor Center"}' 'http://localhost:8080/stores'

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"address": "37.3327° N, 122.0053° W",  "name": "Apple Park Visitor Center"}' 'http://localhost:8080/stores'

ECHO List all stores
curl -X GET --header 'Accept: application/json' 'http://localhost:8080/stores'

ECHO Update store 1
curl -X PUT --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"address": "37.3327° N, 122.0053° W", "name": "Apple Park Visitor Center", "tags": ["Apple Store", "Consumer Electronics", "Support", "Computers", "Tech", "Travel"]}' 'http://localhost:8080/stores/1'

ECHO Detail store 1
curl -X GET --header 'Accept: application/json' 'http://localhost:8080/stores/1'

ECHO Delete store 2
curl -X DELETE --header 'Accept: application/json' 'http://localhost:8080/stores/2'

