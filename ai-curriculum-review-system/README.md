# AI Curriculum Review System

An applied AI proof of concept for detecting potential curriculum overlap between university courses using semantic embeddings and vector similarity search.

Developed in the context of JAMK University of Applied Sciences and used as the implementation basis of the Bachelor’s thesis:

**Vector Similarity Search for Curriculum Overlap Detection: Embedding Models and Threshold Optimization**

The system is designed as a **decision-support tool** for curriculum experts, not as an automated curriculum decision-maker.

---

## Live Demo

**Streamlit demo:** `ADD_YOUR_STREAMLIT_DEMO_URL_HERE`

The demo lets a user submit a proposed course, generate its semantic embedding, compare it against the stored JAMK ICT course set, and review ranked similarity results.

---

## System Workflow

```text
Course Data
    ↓
Text Preparation
    ↓
Embedding Generation
    ↓
Vector Similarity Search
    ↓
Similarity Threshold
    ↓
Ranked Overlap Candidates
    ↓
Expert Review
```

---

## Final Configuration

- **Embedding model:** OpenAI `text-embedding-3-large`
- **Text representation:** Enriched
- **Similarity metric:** Cosine similarity
- **Threshold rule:** Maximum F1
- **Locked threshold:** `0.673784`
- **Development AP:** `0.9392`
- **Development ROC-AUC:** `0.9947`

The public demo uses locally stored final embeddings. The project also includes work toward PostgreSQL + pgvector retrieval.

---

## Demo Use

1. Open the Streamlit application.
2. Enter a proposed course.
3. Click **Run similarity review**.
4. Review the top similarity score, flagged courses, ranked matches, course comparison, and downloadable report.

---

## Test Case 1 — Expected Overlap

This test case is based on the real **Data Networks (TT00CD70)** course in the dataset.

### Course code

```text
TEST-NET-01
```

### Course name

```text
Network Infrastructure and Internet Protocols
```

### Objective

```text
The student understands the structure of computer networks and layered network architectures.
The student can explain common Internet and local area network protocols.
The student can design a local area network using routers, switches, workstations and servers.
The student understands IPv4 and IPv6 addressing, subnetting and routing principles.
The student can configure network devices and troubleshoot common connectivity problems.
```

### Content

```text
Network architecture and layered communication models.
Ethernet switching and network segmentation.
Virtual LANs and Spanning Tree.
IPv4 and IPv6 addressing and subnetting.
Static routing, OSPF and BGP.
TCP and UDP.
DHCP, ARP, DNS, HTTP and SSH.
Network cabling and wireless networking.
Router and switch configuration.
Network troubleshooting and configuration management.
```

### Learning outcomes

```text
The student can explain key network protocols and layered architectures.
The student can create an IP addressing and subnetting plan.
The student can configure switches and routers for a small network.
The student can analyse common network connectivity problems.
```

### Prerequisites

```text
Linux Basics
```

### Knowledge and understanding

```text
The student understands network architectures, communication protocols, Ethernet switching, routing and IP-based networking.
```

### Engineering practice

```text
The student can design, configure and troubleshoot a small network using switches, routers and end devices.
```

**Expected result:** `Data Networks (TT00CD70)` should appear among the strongest matches and is expected to be treated as a potential overlap candidate.

---

## Test Case 2 — Expected Low Overlap

### Course code

```text
TEST-PHOTO-01
```

### Course name

```text
Creative Photography and Visual Storytelling
```

### Objective

```text
The student understands basic principles of photography and visual storytelling.
The student can use composition, lighting and perspective to communicate visual ideas.
The student can plan and produce a small photographic story.
The student can evaluate visual work and explain creative choices.
```

### Content

```text
Photographic composition.
Natural and artificial lighting.
Camera exposure and image capture.
Perspective and visual balance.
Portrait and environmental photography.
Colour and visual mood.
Basic image editing.
Visual storytelling and photographic sequencing.
Portfolio preparation and peer critique.
```

### Learning outcomes

```text
The student can apply composition and lighting principles in photography.
The student can create a coherent short photographic story.
The student can evaluate photographs and explain visual decisions.
```

### Prerequisites

```text
No previous photography experience required
```

### Knowledge and understanding

```text
The student understands basic principles of photographic composition, lighting and visual communication.
```

### Applying technology to practice

```text
The student can use a camera and basic image-editing tools to produce photographic work.
```

### Communication and teamwork

```text
The student can present visual work and provide constructive feedback during group critique sessions.
```

**Expected result:** the strongest similarity score should remain below the overlap threshold, with no meaningful curriculum overlap expected against the current ICT-focused course set.

---

## Dataset and Prototype

The prototype contains:

- 50 JAMK ICT courses
- 3,072-dimensional final embeddings
- 1,225 pairwise course comparisons
- structured curriculum fields including objectives, competences, learning outcomes, content and prerequisites

---

## Technologies

**AI & Data:** Python, Pandas, NumPy, Scikit-learn, OpenAI Embeddings, Sentence Transformers, TF-IDF, BM25  
**Vector Search:** PostgreSQL, pgvector, Parquet  
**Application:** Streamlit, Plotly, ReportLab  
**Engineering:** Git, GitHub, Jupyter Notebook, Docker

---

## Repository Structure

```text
ai-curriculum-review-system/
├── app-pgvector/
│   ├── streamlit_app.py
│   └── requirements.txt
├── data/
│   ├── courses_clean.csv
│   └── final_embeddings.parquet
├── experiments/
├── notebooks/
├── reports/
│   └── tables/
│       └── thresholds/
│           └── final_threshold_recommendation.csv
├── next-step/
├── README.md
└── requirements.txt
```

---

## Local Run

```bash
git clone https://github.com/Nirodha-Sandaruwani/GitHub-Portfolio.git
cd GitHub-Portfolio/ai-curriculum-review-system
pip install -r app-pgvector/requirements.txt
streamlit run app-pgvector/streamlit_app.py
```

Set the following environment variables before running:

```text
OPENAI_API_KEY=your_openai_api_key
USE_PGVECTOR=false
```

Do not commit API keys or `.env` files.

---

## Limitations

This is a proof of concept based on a bounded ICT curriculum dataset. Similarity results support expert review and should not be interpreted as automatic decisions about course duplication, removal or curriculum quality.