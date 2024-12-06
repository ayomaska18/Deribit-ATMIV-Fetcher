# Deribit ATMIV Fetcher

This repository fetches and stores At-The-Money (ATM) Implied Volatility (IV) data for BTC, ETH, and SOL from Deribit Exchange. It uses **InfluxDB** for storage and **Grafana** for visualization, all running within Docker containers.

## Features
- Fetches ATM IV data for BTC, ETH, and SOL.
- Stores the data in InfluxDB.
- Visualizes the data using Grafana dashboards.

---

## Prerequisites

1. Install **Docker** and **Docker Compose** on your system:
2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Deribit_ATMIV_Fetcher.git
   cd Deribit_ATMIV_Fetcher
   ```

---

## Configuration

1. Create a `.env` file in the root directory of the project. Use the following template:

   ```dotenv
   INFLUXDB_URL=
   INFLUXDB_USERNAME=
   INFLUXDB_PASSWORD=
   INFLUXDB_ORG=
   INFLUXDB_BUCKET=
   INFLUXDB_ADMIN_TOKEN=
   GRAFANA_URL=
   GRAFANA_ADMIN_USER=
   GRAFANA_ADMIN_PASSWORD=   
   GRAFANA_SECURITY_ALLOW_EMBEDDING=
   GRAFANA_AUTH_ANONYMOUS_ENABLED=
   GRAFANA_AUTH_ANONYMOUS_ORG_ROLE=
   GRAFANA_SERVER_ROOT_URL=
   GRAFANA_SERVER_SERVE_FROM_SUB_PATH=
   ```

   Replace the placeholder values with your actual credentials:
   - `DERIBIT_CLIENT_ID` and `DERIBIT_CLIENT_SECRET`: Obtain these from the [Deribit API](https://docs.deribit.com/#public-auth).
   - `INFLUXDB_*`: Configure according to your InfluxDB setup.

2. Ensure the `docker-compose.yml` file is properly set up for your environment. No changes are typically needed unless you have specific configurations.
3. Ensure the `datasource.yaml` file token is the same as the token with `INFLUXDB_ADMIN_TOKEN`

---

## Running the Application

1. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Open Grafana in your browser to view the dashboards:
   - By default, Grafana runs on [http://localhost:3000](http://localhost:3000).

3. Log in to Grafana using the default credentials:
   - **Username**: `admin`
   - **Password**: `admin`

   You can change the password on the first login.

4. Go to Dashboards section and you can view the dashboards
---
## Stopping the Application

To stop and remove the containers, use:
```
docker-compose down
```
