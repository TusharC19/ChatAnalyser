# 💬 WhatsApp Chat Analyzer

A **Streamlit-based WhatsApp Chat Analyzer** that extracts insights from chat data such as sentiment, most active users, word frequency, and timelines.

---

## 🚀 Features

* 📊 **User Activity Analysis**
* 😊 **Sentiment Analysis**
* 🕒 **Timeline Analysis (daily/monthly)**
* 🔥 **Most Common Words**
* ☁️ **WordCloud Visualization**
* 📈 **Interactive Charts using Streamlit**
* 🧹 Hinglish stopword removal support

---

## 📂 Project Structure

```
WHATSAPP_CHAT_ANALYZER_PYCHARM/
│── app.py              # Main Streamlit app
│── main.py             # Entry logic (if used separately)
│── helper.py           # Analysis & visualization functions
│── preprocessor.py     # Chat cleaning & preprocessing
│── stop_hinglish.txt   # Custom stopwords
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
│── LICENSE
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/ChatAnalyser.git
cd ChatAnalyser
```

### 2️⃣ Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📊 How to Use

1. Export WhatsApp chat (without media)
2. Upload `.txt` file in the app
3. View:

   * Most active users
   * Message timeline
   * Word analysis
   * Sentiment insights

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Libraries:** pandas, matplotlib, seaborn, wordcloud, nltk

---

## 📌 Future Improvements

* 🤖 Advanced ML sentiment model
* 🌍 Multi-language support
* 📊 Dashboard improvements
* ☁️ Online chat upload support

---

## 🤝 Contributing

Feel free to fork and contribute to this project!

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Tushar
BTech CSE | NIT Raipur
Competitive Programmer | MERN Developer

---
