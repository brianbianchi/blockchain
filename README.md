# blockchain

### endpoints
* `GET /chain`
  * returns blockchain
* `GET /mine`
  * creates new block
* `GET /transactions`
  * returns current transactions
* `POST /transactions`
  * creates new transaction
* `GET /nodes`
  * returns list of nodes
* `POST /nodes/register`
  * adds new nodes to list of nodes
* `GET /nodes/resolve`
  * compares local version of blockchain with other nodes
  * updates copy of blockchain if it is behind