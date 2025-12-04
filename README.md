# 🚀 Airflow + Kafka + Telegram Bot + OpenAI Integration (WORK IN PROGRESS)

This project demonstrates a **modular pipeline** that connects a Telegram bot with Kafka, Airflow, OpenAI and SQLite.  
It allows users to send messages via Telegram, process them with OpenAI, and store numeric responses in a database for downstream workflows.

---

## 📦 Components

- **Apache Airflow**  
  Orchestrates tasks and manages DAGs. Runs in Docker.

- **Kafka + Zookeeper**  
  Provides a message broker for communication between the Telegram bot and Airflow consumer.

- **Telegram Bot**  
  Non-numeric messages → processed by OpenAI (LLM prompt).  
  Numeric messages → pushed directly into Kafka.

- **OpenAI API**  
  Generates contextual numeric questions when users send free text.

- **SQLite**  
  Stores consumed Kafka messages for persistence and analysis.

---

## 🗂 Project Structure
```
├── docker-compose.yaml # Airflow + Kafka + Redis + Postgres + Bot services  
├── bot_app/  
│ ├── bot_producer_llm.py # Telegram bot producer logic  
│ └── config.py # Secrets (OPENAI_KEY, TELEGRAM_KEY)  
├── dags/  
│ └── kafka_consumer_dag.py # Airflow DAG consuming Kafka → SQLite  
├── requirements.txt # Python dependencies  
└── Dockerfile # Custom Airflow image with bot + requirements
```

---

## ⚙️ Setup

### 1. Environment Variables
Create a `.env` file in the project root:

```env
OPENAI_TOKEN=your_openai_api_key
BOT_TOKEN=your_telegram_bot_token
```
### 2. Build & Start Services

```bash
docker-compose build #creates images
docker-compose up #creates containers
```

This will start:

-   Airflow (scheduler, workers, API server, etc.)
    
-   Kafka + Zookeeper
    
-   Telegram bot producer
    

## 📖 Usage

1.  **Start the Telegram bot**
    
    -   Send a message to your bot.
        
    -   If it’s **text**, OpenAI reformulates it into a numeric question.
        
    -   If it’s a **number**, it’s sent directly to Kafka.
        
2.  **Kafka → SQLite via Airflow DAG**
    
    -   Airflow DAG (`kafka_consumer_dag`) runs every 5 minutes.
        
    -   Consumes messages from Kafka topic `telegram_topic`.
        
    -   Stores them in `telegram.db` under table `kafka_messages`.
        
3.  **Inspect Stored Data**
    

```bash
sqlite3 telegram.db
sqlite> SELECT * FROM kafka_messages;

```


## 🧩 Example Flow

-   User sends:
    
    ```Code
    I like to travel!
    ```
    
-   Bot replies (via OpenAI):
    
    ```Code
    How many countries have you visited?
    ```
    
-   User sends:
      
    ```Code
    13
    ```
    
-   Bot acknowledges and pushes `13` → Kafka → Airflow DAG → SQLite.
    

## 🛠 Development Notes

-   **Airflow Image**: Extended from `apache/airflow:2.9.0` with extra requirements. Dockerfile was built on top of the original Airflow Dockerfile.
    
-   **docker-compose.yaml** was adjusted to start from an own image and in order to launch Zookeeper, a Kafka broker and topic, as well as the bot.
    
-   **Secrets**: Managed via `.env` file and `config.py`.
    

## ⚠️ Warnings

-   This setup is for **local development only**.
    
-   Do **not** use in production without securing secrets, scaling Kafka, and hardening Airflow.
    
