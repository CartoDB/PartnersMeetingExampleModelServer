# A sample server for serving a model



### Installation

```bash
git clone https://github.com/CartoDB/PartnersMeetingExampleModelServer.git
```

### Build & Launch

```bash
docker-compose up
```

### Endpoint

/predict

Takes arguments :

- username: The username of the account
- apikey: The API Key of the account
- input\_table: The table with the target locations we want to predict on
_ output\_table: Where we want the resutls to be stored.

