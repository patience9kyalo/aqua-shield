
# Aqua-Shield Telemetry Node: Predictive Aquaculture Analytics

Aqua-Shield is a full-stack predictive analytics dashboard designed to optimize fish pond management. By pulling real-time atmospheric metrics directly from an external weather service, the platform runs localized telemetry algorithms to dynamically calculate metabolic feeding multipliers, predict hydrological overflow risks, and monitor dissolved oxygen stability boundaries.

To ensure high availability and minimize external API request overhead, the architecture utilizes a high-performance caching layer managed via a **Dockerized Redis** instance.

---

## 🛠️ Tech Stack

* **Frontend:** React (TypeScript), Native CSS3, Lucide React (Iconography)
* **Backend:** FastAPI (Python), HTTPX (Asynchronous API requests)
* **Database & Caching:** Redis (Hosted via Docker)

---

## 🚀 Key Features

* **Live Weather AI Streaming:** Fetches live, real-world atmospheric conditions (temperature, precipitation, humidity, and wind velocity) based on user-submitted GPS coordinates.
* **Metabolic Feed Optimization:** Processes air-to-pond calculations instantly using a customized mathematical scale multiplier to minimize inventory waste and preserve water chemistry.
* **Predictive Risk Matrices:** Monitors cumulative rainfall metrics to flag hydrological overflow hazards and tracks ambient wind velocity to evaluate dissolved oxygen stability.
* **Operational Checklist:** Generates a real-time, interactive checklist of actionable safety routing tasks based on current telemetry metrics.
* **Dockerized Cache Pipeline:** Implements a 15-minute Redis Time-to-Live (TTL) cache strategy to drastically reduce external API network latency.

---

## 📦 Quick Start & Commands

### 1. Start the Caching Infrastructure (Docker)

Spin up the background Redis caching layer container cleanly using Docker:

```bash
docker run --name aquashield-redis -p 6379:6379 -d redis

```

### 2. Launch the Backend (FastAPI)

1. Navigate to the backend directory and activate your virtual environment:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Mac/Linux: source venv/bin/activate

```


2. Install dependencies and start the server:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

```


*Make sure to configure your `.env` file with your `WEATHER_AI_API_KEY` in the root of the backend folder.*

### 3. Launch the Frontend (Vite/React)

1. Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install

```


2. Start the local development web server:
```bash
npm run dev

```


3. Open your browser and navigate to `http://localhost:5173` to interact with the dashboard.

---

## 🔄 Development Maintenance

To clear out stale or corrupted data metrics from your Dockerized Redis memory cache and force a live API refresh, run:

```bash
docker exec -it aquashield-redis redis-cli flushall

```

---

## 📝 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
