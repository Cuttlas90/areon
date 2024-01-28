# Areon Workbench
Areon Workbench, allow data scientists and developers easily get a broad access to analyze network.
Areon workbench is more than a API, or just data interpretation. it allows users to customize their data flow.
- Get exactly the data you need:
With Areon workbench you can build your data pipelines with SQL. Get the data you need to handle even the most complex scenarios.

- it is Flexible
Transform and combine data from different datasets to form your unique view of the blockchain.

- Easy-to-use
Areon network fully manages the underlying operations of pipeline, providing developers with a simple, easy-to-use development environment.

- Scalable
Our efficient streaming engine can process data up to gigabytes per second.

## repository consist of for part:

- streamer: responsible for connecting to areon blockchain using web3 package read blockchain data (currently blocks and transaction) and storing them in a postgres database
- api: responsible for query the database and retieriving data
- workbench: an interface that allows user to write the query they want and send them to server, server will retrieve the answer and will show it as a table in workbench
- dashboard: an example for how much powerful this system can be and some minimum example of how user can request

## Step-By-Step
### stream
it lets you convert blockchain data into convenient formats like CSVs and relational databases.

currently you can Easily export Blocks and Transaction but it can expand for logging other data from the areon blockchain

```sh
python.exe .\ethereumetl.py stream -o postgresql+pg8000://postgres:123%40Abcd@127.0.0.1:5432/areondb -e block,transaction --log-file log.txt --provider-uri https://testnet-rpc.areon.network
```

### API

it provide api for connecting to database, it will provide a nodejs app

```sh
npm install
node bin/www-
```
### workbench

it provide a simple interface that let user interactively query the blockchain.
data will be shown in table style
this part is a html & css

### dashboard

to show how much powerful this project can be a demo dashboard is lunch, all data is collected using a single endpoint. there is no limitation for accessing blockchain data. users can easily use powerful sql language two retrieve desired data.

for running the dashboard

```sh
pip install -r requirement.txt
streamlit run streamlit_app.py
```
## DEMO

currently you can find workbench and dashboard demo here
- [workbench](https://areon.cuttlas.app/)
- [Dashboard](https://areon-dashboard.cuttlas.app/)


