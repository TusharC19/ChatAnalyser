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

The application identifies useful information hidden inside conversations using Google Gemini.

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

Instead, it first filters potentially useful messages using a **rule-based candidate detection system**.

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

Submission of report file and presentation
Type: deadline
Deadline: 1st
Confidence: 0.95
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

This makes the AI output **verifiable and grounded in the original conversation**.

---

## 🧹 5. Action Deduplication

The system prevents repeated actions from unnecessarily appearing multiple times.

For example:

```text
Task:
Fill out the assignment form

Request:
Fill out the assignment form
```

These can represent the same practical action.

ChatAnalyser normalizes action text and removes duplicate results while preserving the highest-confidence result and its original source.

---

## 🔍 6. Ask Your Conversation

Users can search their WhatsApp conversation using natural language.

Example:

```text
When do I need to submit the assignment?
```

The system combines:

```text
Semantic Similarity
        +
Keyword Matching
        +
AI Relevance
        ↓
Relevant Conversation
```

The result can show:

- Relevant message
- AI interpretation
- Task
- Deadline
- Priority
- Confidence
- Evidence
- Original conversation context

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

The exported WhatsApp `.txt` file is converted into a structured Pandas DataFrame.

Each message contains information such as:

```text
message_id
date
time
user
message
```

---

## 2️⃣ Candidate Filtering

Instead of sending the complete conversation to Gemini, ChatAnalyser first identifies potentially important messages.

The candidate filter looks for patterns related to:

- Actions
- Requests
- Deadlines
- Decisions
- Questions

Example from testing:

```text
Total messages:     1048
Candidate messages: 44
```

This reduces unnecessary AI processing.

---

## 3️⃣ Context Extraction

For each candidate message, surrounding messages are included.

Default context:

```text
2 previous messages
        +
Current message
        +
2 next messages
```

This helps the AI understand conversational context.

---

## 4️⃣ Gemini AI Extraction

Gemini converts the conversation context into structured information.

The extraction schema contains:

```text
message_id
is_important
type
task
deadline
priority
confidence
evidence
```

Supported types:

```text
task
request
deadline
decision
information
none
```

---

## 5️⃣ Validation

AI-generated results are validated before being displayed.

Validation checks include:

- Valid message ID
- Supported type
- Valid priority
- Valid confidence
- Evidence availability
- Evidence consistency with the original conversation

The system avoids blindly displaying unsupported AI results.

---

## 6️⃣ Deduplication

Similar actions are normalized and duplicate results are removed.

The highest-confidence result is retained so its:

```text
Message ID
Evidence
Original context
```

remain available.

---

## 7️⃣ Semantic Search

Conversation messages are converted into embeddings using:

```text
all-MiniLM-L6-v2
```

FAISS is used for efficient similarity search.

The ranking combines:

```text
60% Semantic Similarity
25% Keyword Matching
15% AI Relevance
```

This allows natural-language queries even when the exact words do not appear in the original message.

---

# 🛠️ Tech Stack

## Frontend / Interface

- Streamlit

## Programming

- Python

## Data Processing

- Pandas
- NumPy
- Matplotlib
- Seaborn

## AI / NLP

- Google Gemini API
- `google-genai`
- Sentence Transformers
- Pydantic

## Semantic Search

- FAISS
- `all-MiniLM-L6-v2`

## Configuration

- Python environment variables
- `.env`

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

## 1️⃣ Clone the repository

```bash
git clone https://github.com/TusharC19/ChatAnalyser.git
cd ChatAnalyser
```

## 2️⃣ Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If the AI/search dependencies are not already included:

```bash
pip install google-genai sentence-transformers faiss-cpu pydantic
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

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📱 How to Use

## Step 1 — Export WhatsApp Chat

Export a WhatsApp conversation as a `.txt` file.

For best results, export the chat **without media**.

---

## Step 2 — Upload the Chat

Upload the `.txt` file using the sidebar.

---

## Step 3 — Select Analysis Scope

Choose:

```text
Overall
```

or select a specific participant.

---

## Step 4 — Explore Chat Analytics

View:

- Message statistics
- Activity timelines
- Most active users
- Word frequency
- WordCloud
- Emoji analysis
- Activity heatmaps

---

## Step 5 — Run AI Analysis

Click:

```text
🔍 Analyze Conversation with AI
```

The system will identify useful information from the conversation.

---

## Step 6 — Explore the Action Dashboard

Review:

```text
🎯 Tasks
🙋 Requests
📅 Deadlines
🤝 Decisions
```

Use the filters to find specific types of actions or priorities.

---

## Step 7 — Verify AI Results

Click:

```text
🔎 View source
```

to see:

- Evidence
- Original message
- Surrounding context
- Message ID

---

## Step 8 — Ask Your Conversation

Enter a natural-language question.

Examples:

```text
When do I need to submit the assignment?
```

```text
What tasks do I need to complete?
```

```text
What did someone ask me to send?
```

```text
What did we decide about the project?
```

---

# 🧪 Testing

The AI pipeline has been tested on a WhatsApp conversation containing:

```text
Total messages: 1048
Candidate messages: 44
AI results: 44
```

The generated results contain:

```text
message_id
date
user
message
candidate_score
candidate_reason
is_important
type
task
deadline
priority
confidence
evidence
```

### Example extracted result

```text
Message ID:
849

Type:
deadline

Task:
Submit assignment

Deadline:
tomorrow

Priority:
high

Confidence:
0.95

Evidence:
"waise kal submit krne bola the sir"
```

---

# 🎯 Real-World Use Cases

## 👨‍🎓 Student Groups

Useful for finding:

- Assignment deadlines
- Tasks
- Questions to solve
- Notes/resources people promised to send
- Exam-related information
- Project decisions

---

## 👨‍💻 Project Teams

Useful for finding:

- Assigned tasks
- Requests between teammates
- Submission deadlines
- Project decisions
- Important discussions

---

## 🏢 Organization / Event Groups

Useful for finding:

- Responsibilities
- Pending actions
- Important dates
- Decisions
- Resource requests

---

# 💡 What Makes ChatAnalyser Different?

Traditional WhatsApp chat analyzers primarily answer:

> **"What happened in this conversation?"**

ChatAnalyser aims to answer:

> **"What useful information can I take from this conversation?"**

It combines:

```text
Chat Analytics
      +
Rule-Based Candidate Filtering
      +
Context-Aware AI Extraction
      +
Evidence Validation
      +
Action Deduplication
      +
Action Dashboard
      +
Semantic Search
```

The result is a prototype for **conversation intelligence**, rather than just a chat visualization tool.

---

# ⚠️ Current Limitations

ChatAnalyser is an AI-assisted system, so extraction quality can depend on the conversation.

Current limitations include:

- Ambiguous messages can be difficult to classify.
- Task vs request classification may sometimes overlap.
- Informal Hinglish and abbreviations can affect extraction.
- Expressions such as `kal`, `1st`, or `7 baje` may require context.
- Semantic search depends on the embedding model.
- AI analysis requires a configured Gemini API.
- The current application works with exported WhatsApp `.txt` conversations rather than real-time WhatsApp messages.

---

# 🔮 Future Improvements

Potential future improvements include:

- Better Task vs Request classification
- Improved Hinglish and multilingual understanding
- Better date/time normalization
- User-specific task assignment
- Calendar export for deadlines
- Custom priority settings
- More advanced semantic retrieval
- Conversation summarization
- Quantitative extraction evaluation
- Real-time chat ingestion
- Hosted deployment

---

# 🔐 Privacy & Security

ChatAnalyser may process private conversation data.

Users should:

- Keep API keys inside `.env`
- Never commit API keys to GitHub
- Avoid uploading sensitive conversations to external AI services unless they understand the privacy implications
- Only analyze conversations they are authorized to use

---

# 🤝 Contributing

Contributions and suggestions are welcome.

To contribute:

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

**Tushar**

B.Tech — Computer Science & Engineering  
National Institute of Technology Raipur

Competitive Programmer | MERN Developer | AI/ML Enthusiast

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub!