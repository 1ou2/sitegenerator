---
title: CouchDB
date: 2024-10-06
tags: tech
---

# Couchdb

## Installation
As of 2024-10-03 ubuntu 24.04 "noble" is not available in apache artifactory, 
After running the command 
```
echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ ${VERSION_CODENAME} main" \
    | sudo tee /etc/apt/sources.list.d/couchdb.list >/dev/null
sudo apt update
The repository 'https://apache.jfrog.io/artifactory/couchdb-deb noble Release' does not have a Release file.
```
we need to install via snap
https://github.com/apache/couchdb-pkg/blob/main/README-SNAP.md


```
sudo snap install couchdb
export COOKIE=`echo $(dd if=/dev/random bs=1 count=38 status=none | base64 | tr -cd '[:alnum:]')`
sudo snap set couchdb admin=[your-password-goes-here] setcookie=$COOKIE
sudo snap restart couchdb.server
```

The general syntax using curl is the following
```curl -s -X GET "http://admin:password@127.0.0.1:5984/_COMMAND" | jq```

To troubleshoot and access the logs:
```sudo snap logs couchdb.server -f```

## Unistall
snap list
sudo snap stop couchdb
sudo snap remove couchdb
sudo snap remove --purge couchdb
ls /var/snap/couchdb
sudo rm -rf /var/snap/couchdb
snap list

## Configure
Set 
- hostname=127.0.0.1:5984
- userame=admin
- password=admin-password

```
curl -X POST "${hostname}/_cluster_setup" -H "Content-Type: application/json" -d "{\"action\":\"enable_single_node\",\"username\":\"${username}\",\"password\":\"${password}\",\"bind_address\":\"0.0.0.0\",\"port\":5984,\"singlenode\":true}" --user "${username}:${password}"
```

from the documentation :
```
curl -X POST "${hostname}/_cluster_setup" -H "Content-Type: application/json" -d "{\"action\":\"enable_single_node\",\"username\":\"${username}\",\"password\":\"${password}\",\"bind_address\":\"0.0.0.0\",\"port\":5984,\"singlenode\":true}" --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/chttpd/require_valid_user" -H "Content-Type: application/json" -d '"true"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/chttpd_auth/require_valid_user" -H "Content-Type: application/json" -d '"true"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/httpd/WWW-Authenticate" -H "Content-Type: application/json" -d '"Basic realm=\"couchdb\""' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/httpd/enable_cors" -H "Content-Type: application/json" -d '"true"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/chttpd/enable_cors" -H "Content-Type: application/json" -d '"true"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/chttpd/max_http_request_size" -H "Content-Type: application/json" -d '"4294967296"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/couchdb/max_document_size" -H "Content-Type: application/json" -d '"50000000"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/cors/credentials" -H "Content-Type: application/json" -d '"true"' --user "${username}:${password}"
curl -X PUT "${hostname}/_node/couchdb@127.0.0.1/_config/cors/origins" -H "Content-Type: application/json" -d '"app://obsidian.md,capacitor://localhost,http://localhost"' --user "${username}:${password}"
```

## Setup
Create a database
curl -X PUT http://admin:password@127.0.0.1:5984/mydatabase
Edit configuration
```
sudo nano /var/snap/couchdb/current/etc/local.ini 
[vhosts]
example.com:1234 = /mydatabase/
```
Restart the server 
### Commands
Check node configuration
```
curl -s -X GET "http://admin:password@127.0.0.1:5984/_membership" | jq
{
  "all_nodes": [
    "couchdb@127.0.0.1"
  ],
  "cluster_nodes": [
    "couchdb@127.0.0.1"
  ]
}
```
Get all databases

```
curl -s -X GET "http://$admin:$password@127.0.0.1:5984/_all_dbs" | jq
[
  "_replicator",
  "_users"
]
```

Delete and create a database named ```notes```
```bash
curl -X DELETE "http://$admin:$password@127.0.0.1:5984/notes"
curl -X PUT "http://$admin:$password@127.0.0.1:5984/notes"live
```

