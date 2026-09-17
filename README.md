# 💬 ChatAnalyser — AI-Powered Conversation Intelligence

A **Streamlit-based WhatsApp Conversation Intelligence platform** that transforms unstructured WhatsApp conversations into useful, actionable information.

Unlike traditional chat analyzers that only show statistics, ChatAnalyser uses **AI, context extraction, evidence validation, and semantic search** to identify:

- 🎯 Tasks
- 🙋 Requests
- 📅 Deadlines
- 🤝 Decisions
- 🔴 Priority
- 🔎 Evidence from the original conversation

It also allows users to **ask questions about their conversation using natural language**.

---

## 🚀 Why ChatAnalyser?

Important information in WhatsApp groups is often buried among hundreds or thousands of casual messages.

For example:

> "Aaj raat ko degunga, waise kal submit krne bola the sir"

A traditional chat analyzer would treat this as just another message.

ChatAnalyser can identify:

```text
Task       → Submit assignment
Deadline   → Tomorrow
Priority   → High
Evidence   → "waise kal submit krne bola the sir"
```

This turns an unstructured conversation into **actionable intelligence**.

---

# ✨ Features

## 📊 1. WhatsApp Chat Analytics

The original chat-analysis functionality is preserved.

- 📩 Total messages
- 📝 Total words
- 📎 Media shared
- 🔗 Links shared
- 📅 Monthly timeline
- 📆 Daily timeline
- 🔥 Most active day
- 📈 Most active month
- 🗓️ Weekly activity heatmap
- 👥 Most active users
- ☁️ WordCloud visualization
- 🔤 Most common words
- 😀 Emoji analysis

---

## 🧠 2. AI Conversation Intelligence

The application identifies useful information hidden inside conversations using the Google Gemini API.

The AI extracts:

- 🎯 Tasks
- 🙋 Requests
- 📅 Deadlines
- 🤝 Decisions
- ⭐ Importance
- 🔴 Priority
- 📊 Confidence score
- 📌 Evidence

The system does not send every message directly to the LLM.

Instead, it first filters potentially useful messages using a **rule-based candidate detection system**, then batches the remaining candidates for API calls.

---

## 🎯 3. Action Dashboard

Extracted information is organized into an actionable dashboard.

### Available filters

**Filter by type**

- All
- Tasks
- Requests
- Deadlines
- Decisions

**Filter by priority**

- All
- High
- Medium
- Low

Example:

```text
🎯 Action Dashboard

🔴 High Priority

Submit assignment
Type: deadline
Deadline: tomorrow
Confidence: 1.0
```

---

## 🔎 4. Evidence & Source Traceability

Every extracted action can be traced back to the original WhatsApp message.

The source viewer displays:

- 📌 AI evidence
- 💬 Original message
- 💭 Surrounding conversation context
- 🆔 Message ID

Example:

```text
Extracted Action:
Submit assignment

Deadline:
Tomorrow

Evidence:
"waise kal submit krne bola the sir"

Source:
Message 849
```

This makes the AI output **verifiable and grounded in the original conversation**, rather than a black-box claim.

---

## 🧹 5. Action Deduplication

The system prevents repeated actions from unnecessarily appearing multiple times.

For example, "Fill out the assignment form" appearing as both a task and a request from different messages can represent the same practical action.

ChatAnalyser normalizes action text and removes duplicate results while preserving the highest-confidence result and its original source.

---

## 🔍 6. Ask Your Conversation

Users can search their WhatsApp conversation using natural language, e.g. *"When do I need to submit the assignment?"*

The system combines:

```text
Semantic Similarity (60%)
        +
Keyword Matching (25%)
        +
AI Relevance (15%)
        ↓
Ranked Conversation Results
```

The result can show the relevant message, AI interpretation (task/deadline/priority/confidence), evidence, and original conversation context.

---

# 🏗️ System Architecture

```text
                 WhatsApp TXT Export
                         │
                         ▼
                ┌─────────────────┐
                │  Preprocessing  │
                │    + Parsing    │
                └────────┬────────┘
                         │
                         ▼
                  Pandas DataFrame
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       Chat Analytics          Candidate Filtering
                                     │
                                     ▼
                              Context Extraction
                                     │
                                     ▼
                              Gemini AI Extraction
                                     │
                                     ▼
                           Validation + Evidence
                                     │
                                     ▼
                              AI Results DataFrame
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
             Action Dashboard                  Semantic Search
                    │                                 │
                    └────────────────┬────────────────┘
                                     ▼
                              Streamlit Interface
```

---

# 🔄 AI Processing Pipeline

## 1️⃣ WhatsApp Preprocessing

The exported WhatsApp `.txt` file is converted into a structured Pandas DataFrame with fields such as `message_id`, `date`, `time`, `user`, and `message`.

## 2️⃣ Candidate Filtering

Instead of sending the complete conversation to Gemini, ChatAnalyser first identifies potentially important messages using pattern-based detection for actions, requests, deadlines, decisions, and questions (including Hinglish indicators).

Example from development testing:

```text
Total messages:     1048
Candidate messages: 44
```

This reduces unnecessary AI processing and API cost.

## 3️⃣ Context Extraction

For each candidate message, surrounding messages are included — by default, 2 previous messages, the current message, and 2 next messages — to help the AI understand conversational context.

## 4️⃣ Gemini AI Extraction

Candidate messages (with context) are sent to Gemini in batches. The extraction schema returns structured fields: `message_id`, `is_important`, `type`, `task`, `deadline`, `priority`, `confidence`, `evidence`.

Supported types: `task`, `request`, `deadline`, `decision`, `information`, `none`.

## 5️⃣ Validation

AI-generated results are validated before being displayed — checking message ID validity, supported type, valid priority/confidence values, and evidence consistency against the original conversation. Unsupported results are not blindly shown.

## 6️⃣ Deduplication

Similar actions are normalized and duplicate results are removed, retaining the highest-confidence result along with its message ID and original context.

## 7️⃣ Semantic Search

Conversation messages are embedded using `all-MiniLM-L6-v2`, with FAISS used for similarity search. Rankings combine semantic similarity, keyword matching, and AI relevance to support natural-language queries even when exact wording doesn't match the source message.

---

# 🛠️ Tech Stack

**Frontend / Interface:** Streamlit
**Programming:** Python
**Data Processing:** Pandas, NumPy, Matplotlib, Seaborn
**AI / NLP:** Google Gemini API, `google-genai`, Sentence Transformers
**Semantic Search:** FAISS, `all-MiniLM-L6-v2`
**Configuration:** Python environment variables, `.env`

---

# 📂 Project Structure

```text
ChatAnalyser/
│
├── app.py
├── preprocessor.py
├── helper.py
│
├── ai/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── candidate_filter.py
│   ├── context.py
│   ├── extractor.py
│   ├── pipeline.py
│   ├── postprocessor.py
│   └── semantic_search.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/TusharC19/ChatAnalyser.git
cd ChatAnalyser
```

### 2️⃣ Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If the AI/search dependencies are not already included:

```bash
pip install google-genai sentence-transformers faiss-cpu
```

---

# 🔑 Gemini API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Make sure `.env` is included in `.gitignore`:

```text
.env
__pycache__/
*.pyc
```

**Never commit your API key to GitHub.**

---

# ▶️ Running the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📱 How to Use

1. **Export WhatsApp Chat** — export a conversation as `.txt` (without media, for best results).
2. **Upload the Chat** — upload the `.txt` file via the sidebar.
3. **Select Analysis Scope** — choose "Overall" or a specific participant.
4. **Explore Chat Analytics** — message stats, timelines, active users, word frequency, WordCloud, emoji analysis, activity heatmaps.
5. **Run AI Analysis** — click "🔍 Analyze Conversation with AI" to extract tasks, requests, deadlines, and decisions.
6. **Explore the Action Dashboard** — filter extracted actions by type and priority.
7. **Verify AI Results** — click "🔎 View source" to see evidence, original message, and surrounding context.
8. **Ask Your Conversation** — enter natural-language questions like *"When do I need to submit the assignment?"*

---

# 🧪 Testing

The AI pipeline has been tested on a WhatsApp conversation containing:

```text
Total messages: 1048
Candidate messages: 44
AI results: 44
```

### Example extracted result

```text
Message ID:  849
Type:        deadline
Task:        Submit assignment
Deadline:    tomorrow
Priority:    high
Confidence:  0.95
Evidence:    "waise kal submit krne bola the sir"
```

> Note: this reflects development testing on one sample dataset, not a formal accuracy benchmark across multiple conversations.

---

# 🎯 Real-World Use Cases

- **Student Groups** — assignment deadlines, tasks, resources, project decisions
- **Project Teams** — assigned tasks, requests, submission deadlines, decisions
- **Organization / Event Groups** — responsibilities, pending actions, important dates

---

# 💡 What Makes ChatAnalyser Different?

Traditional WhatsApp chat analyzers primarily answer: **"What happened in this conversation?"**

ChatAnalyser aims to answer: **"What useful information can I take from this conversation?"**

It combines chat analytics, rule-based candidate filtering, context-aware AI extraction, evidence validation, action deduplication, an action dashboard, and semantic search — a prototype for **conversation intelligence**, rather than just a chat visualization tool.

---

# ⚠️ Current Limitations

- Ambiguous messages can be difficult to classify; task vs. request classification may sometimes overlap.
- Informal Hinglish and abbreviations can affect extraction accuracy.
- Relative time expressions (`kal`, `1st`, `7 baje`) may require conversational context to resolve correctly.
- Semantic search quality depends on the embedding model used.
- AI analysis requires a configured Gemini API key and is subject to its rate limits/quotas.
- Works with exported WhatsApp `.txt` conversations, not real-time WhatsApp messages.
- Not a replacement for a full task-management or calendar application.

---

# 🔮 Future Improvements

- Better task vs. request classification
- Improved Hinglish and multilingual understanding
- Better date/time normalization
- User-specific task assignment
- Calendar export for deadlines
- Custom priority settings
- More advanced semantic retrieval
- Conversation summarization
- Real-time chat ingestion
- Hosted deployment

---

# 🔐 Privacy & Security

ChatAnalyser may process private conversation data. Users should:

- Keep API keys inside `.env` and never commit them to GitHub
- Understand that candidate message context is sent to the Gemini API for processing — this is not a fully local/offline pipeline
- Avoid uploading sensitive conversations unless they understand this
- Only analyze conversations they are authorized to use

---

# 🤝 Contributing

Contributions and suggestions are welcome.

```bash
git fork
git clone <your-fork>
git checkout -b feature/your-feature
```

Make your changes and submit a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Tushar Chaturvedi**
B.Tech — Computer Science & Engineering, National Institute of Technology Raipur

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub!