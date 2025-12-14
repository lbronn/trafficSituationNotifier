# 🚦 Traffic Situation Bot

A simple Python automation tool that checks real-time traffic conditions from your **Home** to **Office** and sends a detailed advisory to your Discord server.

It uses Google Maps to calculate travel times for cars, motorcycles, and public transit, helping you decide when to leave or which route to take.

---

### ✨ Features
* **Real-time Updates:** Fetches live traffic data using Google's Routes API.
* **Multi-Mode:** Shows travel times for Driving 🚗, Motorcycle 🏍️, and Commute 🚌.
* **Smart Detours:** Automatically suggests alternative routes if they save you more than 5 minutes.
* **Visual Map:** Sends a map image with your specific route, including "Home" (H) and "Office" (O) markers.
* **Heavy Traffic Alerts:** Warns you specifically if traffic is causing significant delays.

---

### 🛠️ Setup Guide

#### 1. Prerequisites
* **Python** installed on your computer.
* A **Google Cloud API Key** (with **Routes API** and **Maps Static API** enabled).
* A **Discord Webhook URL**.

#### 2. Installation
Download the project files (`trafficSituationNotifier.py`, `google_data.py`, `config.py`) and install the required Python libraries:
```bash
pip install -r requirements.txt
```

#### 3. Configuration
Create a file named `.env` in the same folder and add your specific keys and coordinates. The script will read these values.

```bash
# .env file

GOOGLE_API_KEY=your_google_api_key_here
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here

# Coordinates (Must be in decimal format, e.g., 14.5995)
LAT_HOME=xx.xxxx
LNG_HOME=xx.xxxx
LAT_DESTINATION=xx.xxxx
LNG_DESTINATION=xx.xxxx
```

#### 4. Running the Bot
**Manual Test:** To run the bot immediately (good for testing the webhook and API keys)
```bash
python trafficSituationNotifier.py
```

**Automated Schedule (Mac/Linux):** To have the bot run automatically at your scheduled times *e.g.6 AM, 12 PM, and 4 PM PHT*, you must set up a cron job.

**Step 1.** Open your Terminal and type:
```bash
crontab -e
```

**Step 2.** Add the following line, making sure to replace `/path/to/your/` with the actual directory path where you saved the Python script:
```bash
0 6,12,16 * * * /usr/bin/python3 /path/to/your/trafficSituationNotifier.py
```

---

### 📱 Example Notification

This is what the final message will look like in your Discord channel:

**🔴 Traffic Situation Advisory Date:**

**Date:** March 12, 2025 05:30 PM

**Route:** Home (H) ➡️ Office (O)

**Estimated Travel Times:**

- 🏍️ Motorcycle: 35 mins
- 🚗 Car: 55 mins
- 🚌 Commute: 85 mins

**⚠️ HEAVY TRAFFIC REPORT:**

Current conditions are adding an estimated 20 minutes of delay compared to free-flow traffic.

**ALTERNATIVE ROUTE FOUND!**

Please be advised to take an alternate route that saves 8 minutes. (Travel time: 47 mins)

*[Map Image Included Here]*

---