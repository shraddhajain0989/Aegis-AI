# 🛡️ AegisAI: Human Behavior Manipulation Defense Environment

![AegisAI](https://img.shields.io/badge/Status-Hackathon_Ready-success?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

AegisAI is a cutting-edge **OpenEnv-compatible Reinforcement Learning (RL) environment** and **real-time Browser Extension** designed to train and deploy agents capable of protecting vulnerable users from phishing, scams, and social engineering attacks.

Every year, millions of users fall victim to online fraud. AegisAI bridges the gap between state-of-the-art AI threat detection and real-time user protection.

---

## 🚀 Problem Statement & Impact
Social engineering techniques continually evolve to manipulate human psychology, making them incredibly difficult for standard rule-based detection systems to catch. Fraudsters rely on urgency, familiarity, and fear.

**Our Solution:** 
We've built an autonomous AI environment that trains language models (LLMs) to actively assess conversational contexts, investigate suspicious claims through a multi-step verification process, and decisively warn or block malicious intent before the user is harmed.

---

## 🏗️ Technical Architecture

### 1. OpenEnv RL Environment (`env.py`, `inference.py`)
AegisAI features a multi-step conversational environment simulating real-world scam interactions with users.

- **State Representation**: Messages, Context History, Urgency, User Awareness.
- **Action Space**:
  - `verify`: Triggers a secondary check (e.g., verifying an email sender or checking a bank app payload) to gather more context without immediately blocking a safe message.
  - `warn`: Alerts the user of a detected scam.
  - `block`: Strongly blocks malicious interaction.
  - `ignore`: Deems the message safe.
  - `educate`: Provides background information to the user.
- **Reward Logic (Dense & Step-Level)**:
  - +0.2 for successfully verifying a suspicious claim before acting.
  - +1.0 for correctly classifying and warning/blocking a confirmed scam.
  - Penalty (-1.0) for ignoring a scam or incorrectly blocking a normal utility message.

### 2. Browser Extension MVP (`extension/`)
To bring this technology directly to the end user, we've developed a **Chrome Manifest V3 Extension**.
- **Real-Time Text Scanning**: Seamlessly reads page DOM elements and matches against phishing topologies.
- **Live Highlight**: Visually highlights manipulative keywords (`urgent`, `OTP`, `winner`) to break the "psychological spell" of a phishing attempt.
- **Actionable Popup**: Provides an on-demand scanning button and immediate safety scorecard.

---

## ⚙️ How to Run Locally

### 1. Python Environment
Install the requirements and test the environment logic using the provided `inference.py` sandbox policy.
```bash
pip install -r requirements.txt
python inference.py
```
*Expected Output Logs formatting:*
```
[START] task=easy env=scam_defense_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=verify reward=0.20 done=false error=null
[STEP] step=2 action=warn reward=1.00 done=true error=null
[END] success=true steps=2 score=0.600 rewards=0.20,1.00
```

### 2. Docker Execution
Ensuring full reproducibility.
```bash
docker build -t aegis-ai .
docker run aegis-ai
```

### 3. Browser Extension Installation
1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer Mode** (top-right toggle).
4. Click **Load unpacked** and select the `AegisAI/extension` directory.
5. Pin the **AegisAI Defender** icon!

---

## 🏆 Hackathon Goals
- [x] **Deterministic Task Definitions** across Easy, Medium, and Hard complexities.
- [x] **Robust Error Handling** and OpenEnv compliant `[START]/[STEP]/[END]` logging.
- [x] **Real-World Impact Applicability** demonstrated via the browser extension module.
- [x] **Stable Evaluation Logic** for robust LLM comparison.

*Built to protect. Built for the future.* 🛡️