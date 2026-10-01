# Packaging Curriculum Overlap Detection as an Integration-Ready Service

## Technical handover memo for review

**Context:** RaiPe curriculum tool development  
**Prepared by:** Nirodha Sandaruwani Meneripitiyage Dona  
**Purpose:** Service-packaging recommendation and dev-team handover notes  
**Date:** May 2026

---

## 1. Purpose

The purpose of this memo is to explain how the completed curriculum-overlap detection implementation from the thesis proof of concept can be packaged for integration into the actual curriculum tool.

The completed thesis implementation already validates the core overlap-detection method. The next project question is how that logic can be exposed as a backend capability that the real curriculum tool can call when courses are created, edited, reviewed, or enhanced.

The guiding question for this handover is:

> How can the validated curriculum-overlap detection logic be packaged as a maintainable service or backend capability for the real curriculum tool?

---

## 2. Starting point from the thesis implementation

The thesis implementation produced an evaluated proof-of-concept workflow for curriculum overlap detection. The workflow included course-data preparation, pair generation and manual labelling, embedding benchmark comparison, threshold evaluation, error analysis, pgvector feasibility testing, final artefact generation, and a Streamlit demonstration UI.

The final selected configuration was:

| Item | Final thesis configuration |
|---|---|
| Embedding model | OpenAI `text-embedding-3-large` |
| Course representation | Enriched course text |
| Similarity metric | Cosine similarity |
| Locked threshold | `0.673784` |
| Output logic | Ranked overlap candidates for expert review |
| Embedding dimension | `3072` |

The selected configuration should be treated as the baseline for the first service-packaging discussion. The service does not need to repeat the thesis benchmark workflow during normal runtime. Its role is to apply the selected configuration to the current course data in the curriculum tool.

The thesis result also defines an important product principle: overlap detection should support expert review, not make final curriculum decisions automatically. A high similarity score can indicate possible redundancy, but it can also indicate intended reinforcement or natural progression between related courses. Therefore, the service should return ranked evidence for review rather than decide whether a course must be changed, merged, or removed.

---

## 3. Existing curriculum-tool context

The current GitLab work items show that the curriculum tool already contains several foundation pieces that are directly relevant to service packaging.

| Existing work item | Relevant point for overlap-service packaging |
|---|---|
| **Task 1.1.2: Set up PostgreSQL with pgvector extension** | pgvector is already part of the project foundation, so database-backed vector search is a practical fit rather than only a future option. |
| **Task 2.2.1: markitdown Python sidecar service** | The project already has a pattern for an isolated internal FastAPI sidecar service. An overlap-detection sidecar can follow the same architectural style. |
| **Task 2.3.2: AI SDK wiring, analysis_result table, analysis API** | The project already has an AI analysis concept, `analysis_result` persistence, output schemas, caching through `inputs_hash`, and analysis kinds including `overlap`. |
| **Task 2.4.1: Module + course tables, CRUD, immutable revisions** | The project has structured `module`, `course`, and `course_revision` tables. Every course mutation creates a new immutable revision, which is important for tying embeddings and overlap results to exact course snapshots. |
| **Task 2.4.2: AI seed-from-document, course enhancement, suggestion lifecycle** | The project has a suggestion workflow and immutable revision updates. Overlap results may later support enhancement/suggestion workflows, but the first service can remain focused on candidate detection. |
| **Task 2.4.3: Module and course UI with revisions and suggestions tabs** | The UI direction already includes course content, suggestions, and revisions. Overlap findings could later be displayed in this course-detail workflow if the team accepts the service direction. |

The strongest architectural implication is that a separate internal FastAPI-style service is already compatible with the project direction because the project already includes a Python sidecar pattern for document conversion.

---

## 4. What should be reused from the thesis implementation

The reusable part of the thesis implementation is the backend overlap-detection logic, not the notebook environment or the Streamlit UI.

| Reusable component | Service role |
|---|---|
| Enriched course-text construction | Converts structured course fields into the same text representation used by the selected thesis configuration. |
| Embedding generation | Creates 3072-dimensional embeddings using `text-embedding-3-large`. |
| Stored course embeddings | Provides the searchable reference set of existing course or course-revision vectors. |
| Cosine similarity search | Ranks existing course vectors by semantic closeness. |
| Locked threshold `0.673784` | Flags which similarity results should be treated as overlap candidates. |
| Candidate ranking | Orders results so reviewers see the strongest matches first. |
| Structured output generation | Returns JSON that the curriculum tool backend or frontend can consume. |
| pgvector retrieval logic | Supports vector search inside PostgreSQL, aligned with the existing project foundation. |

A direct mapping from the PoC logic to service logic would look like this:

| Existing PoC logic | Service version |
|---|---|
| Build enriched course text from form fields | `buildEnrichedCourseText(courseRevisionContent)` |
| Generate OpenAI embedding for submitted text | `EmbeddingService.embed(text)` |
| Search local parquet or pgvector | `VectorRepository.searchSimilarCourses(vector, teamId, topK)` |
| Apply locked threshold | `OverlapDecisionService.applyThreshold(score, threshold)` |
| Streamlit ranked result table | JSON response to the curriculum tool |
| Streamlit report/explanation text | Optional UI responsibility in the actual curriculum tool |

---

## 5. What does not need to become part of the integration

The following PoC parts are useful as thesis and demonstration artefacts, but they are not suitable as runtime components of the actual curriculum tool.

| PoC component | Integration decision |
|---|---|
| Streamlit UI | The actual curriculum tool has its own UI and workflow. |
| Jupyter notebooks | Useful for research, evaluation, and reproducibility, but not for runtime service execution. |
| Benchmark workflow | Already used to select the final configuration; not needed for every overlap check. |
| Manual labelling workflow | Useful for evaluation data, not normal production inference. |
| Threshold scanning process | The first service version can use the locked threshold. Recalibration can be a later controlled task. |
| PDF/demo report generation | Not required for backend integration; the real UI can decide how results are displayed. |

---

## 6. Recommended service architecture

The recommended direction is to package the overlap-detection logic as an internal FastAPI-style sidecar service, backed by PostgreSQL/pgvector for embedding storage and retrieval.

```text
Curriculum Tool UI
      ↓
Curriculum Tool Backend / Next.js API
      ↓
Internal Overlap Detection Service / FastAPI
      ↓
PostgreSQL + pgvector
      ↓
Ranked overlap candidates returned to the curriculum tool
```

This architecture fits the current project for four reasons.

First, the project already has PostgreSQL with pgvector, so storing course embeddings in the existing database environment is practical.

Second, the project already defines a Python FastAPI sidecar pattern through the markitdown service. An overlap-detection service could follow a similar internal-service model.

Third, the overlap logic is Python-based in the thesis implementation, while the main curriculum tool appears to be a Next.js/TypeScript application. A sidecar keeps Python ML/NLP dependencies separate from the main application.

Fourth, the real curriculum tool remains responsible for authentication, permissions, UI, course workflow, suggestions, and revision handling. The overlap service remains focused on vectorization, similarity search, and ranked candidate generation.

---

## 7. Minimal viable service scope

The first service version should be small and integration-focused.

### Included in the first service version

| Feature | Description |
|---|---|
| Health check | Confirms the service is running. |
| Active configuration endpoint | Returns active model, text variant, similarity metric, threshold, and embedding dimension. |
| One-course overlap check | Compares one course or course revision against stored course embeddings. |
| Enriched text construction | Uses the thesis representation logic for structured course fields. |
| Embedding generation | Generates an embedding for new or updated course text. |
| pgvector similarity search | Retrieves top matching course embeddings. |
| Threshold flagging | Marks candidates above `0.673784`. |
| Structured JSON response | Returns ranked candidates to the curriculum tool. |

### Not included in the first service version

| Deferred feature | Reason for deferral |
|---|---|
| New benchmark/model comparison | The thesis already selected the first baseline configuration. |
| Threshold recalibration | Should happen later when more real project data and expert feedback exist. |
| Batch reindexing UI | Useful later, but not required to prove integration. |
| Full reviewer feedback loop | Valuable future feature, but should not block the first service package. |
| Production-scale monitoring/drift detection | Important later, but first integration should establish the API and storage contract. |
| Standalone frontend | The actual curriculum tool already has UI direction under Task 2.4.3. |

---

## 8. Proposed internal API contract

The service should expose a small internal API. The exact route names can be adjusted to match project conventions, but the contract should remain explicit.

### `GET /health`

Purpose: service health check.

Example response:

```json
{
  "status": "ok",
  "service": "curriculum-overlap-service",
  "version": "0.1.0"
}
```

### `GET /config`

Purpose: expose the active overlap-detection configuration.

Example response:

```json
{
  "embedding_model": "openai_text-embedding-3-large",
  "text_variant": "enriched",
  "similarity_metric": "cosine",
  "threshold": 0.673784,
  "embedding_dimension": 3072
}
```

### `POST /overlap/check`

Purpose: compare one course revision against the stored reference courses and return ranked overlap candidates.

Example request:

```json
{
  "team_id": "team-uuid",
  "course_id": "course-uuid",
  "course_revision_id": "course-revision-uuid",
  "top_k": 10
}
```

The service can either retrieve the course-revision content from the database or receive the current course content directly from the curriculum backend. The cleaner first option is to use the revision ID, because Task 2.4.1 already makes course revisions immutable.

Example response:

```json
{
  "query": {
    "course_id": "course-uuid",
    "course_revision_id": "course-revision-uuid"
  },
  "configuration": {
    "embedding_model": "openai_text-embedding-3-large",
    "text_variant": "enriched",
    "similarity_metric": "cosine",
    "threshold": 0.673784,
    "embedding_dimension": 3072
  },
  "matches": [
    {
      "rank": 1,
      "matched_course_id": "matched-course-uuid",
      "matched_course_revision_id": "matched-revision-uuid",
      "course_code": "TT00CE05",
      "course_title": "Data Analytics Project",
      "similarity_score": 0.7214,
      "above_threshold": true,
      "interpretation": "Potential overlap candidate"
    }
  ]
}
```

A raw similarity score alone is not enough for curriculum review. Each response should include rank, score, threshold status, course identifiers, and configuration metadata. This makes the result auditable and easier to display in the real tool.

---

## 9. Recommended database additions

The current project already has `course`, `course_revision`, and `analysis_result` concepts. Therefore, the overlap service should integrate with those structures instead of duplicating course data.

### 9.1 Recommended new table: `course_embedding`

A dedicated `course_embedding` table is recommended because embeddings should be tied to immutable course revisions, not only to the mutable `course` row.

Suggested shape:

| Column | Purpose |
|---|---|
| `id uuid PK` | Embedding row identifier. |
| `team_id uuid FK` | Supports team-scoped filtering and permissions. |
| `course_id uuid FK` | Links to the course. |
| `course_revision_id uuid FK` | Links to the exact immutable revision that was embedded. |
| `embedding vector(3072)` | pgvector embedding column. |
| `embedding_text text` | Text actually embedded, useful for audit/debugging. |
| `embedding_text_hash text` | Detects whether the embedded representation changed. |
| `model text` | Example: `openai_text-embedding-3-large`. |
| `text_variant text` | Example: `enriched`. |
| `similarity_metric text` | Example: `cosine`. |
| `embedding_dimension int` | Expected value: `3072`. |
| `status text/enum` | Example: `pending`, `ready`, `failed`. |
| `generated_at timestamptz` | Timestamp for embedding generation. |
| `error text nullable` | Failure details if embedding generation fails. |

Recommended unique constraint:

```text
unique(course_revision_id, model, text_variant)
```

Recommended indexes:

```text
index(team_id)
index(course_id)
index(course_revision_id)
HNSW or IVFFlat index on embedding, depending on pgvector/project preference
```

This table is the most important database addition because it prevents stale or ambiguous embeddings. When a course changes, Task 2.4.1 creates a new revision. The overlap system can then generate a new embedding for that revision without overwriting the old revision’s embedding.

### 9.2 Store overlap results: reuse or extend existing analysis storage

The project already plans an `analysis_result` table in Task 2.3.2 with `kind` values including `overlap`. That table can potentially store overlap-check runs, but the current 2.3.2 shape is mainly designed for LLM-based document/framework analysis. It includes framework references and input document IDs, while the vector-overlap service mainly works with course revisions and embeddings.

There are two possible approaches.

#### Option A: Extend `analysis_result` for vector overlap runs

This keeps all AI/analysis history in one table.

Possible adjustments:

| Adjustment | Reason |
|---|---|
| Allow `kind='overlap'` without a framework reference | Vector overlap detection does not always need a framework. |
| Add or use `input_course_ids` more directly | Overlap checks are course/revision-based, not only document-based. |
| Store configuration metadata in `output` or explicit fields | Model, text variant, threshold, metric, top-k, and candidate count should be auditable. |
| Store the checked `course_revision_id` | Results must be tied to the exact revision that was checked. |

This option is clean if the team wants one unified analysis history.

#### Option B: Add overlap-specific result tables

This avoids changing the existing `analysis_result` contract from Task 2.3.2.

Suggested tables:

```text
course_overlap_run
course_overlap_candidate
```

Possible `course_overlap_run` fields:

| Column | Purpose |
|---|---|
| `id uuid PK` | Run identifier. |
| `team_id uuid FK` | Team scope. |
| `query_course_id uuid FK` | Course being checked. |
| `query_course_revision_id uuid FK` | Exact revision checked. |
| `model text` | Embedding model used. |
| `text_variant text` | Text representation used. |
| `similarity_metric text` | Similarity metric used. |
| `threshold numeric` | Threshold used. |
| `top_k int` | Number of requested matches. |
| `status enum` | `pending`, `running`, `ready`, `failed`. |
| `requested_by uuid FK` | User who requested the check. |
| `requested_at timestamptz` | Request time. |
| `completed_at timestamptz nullable` | Completion time. |
| `error text nullable` | Failure message. |

Possible `course_overlap_candidate` fields:

| Column | Purpose |
|---|---|
| `id uuid PK` | Candidate identifier. |
| `run_id uuid FK` | Parent overlap run. |
| `matched_course_id uuid FK` | Matched course. |
| `matched_course_revision_id uuid FK` | Matched course revision. |
| `rank int` | Candidate rank. |
| `similarity_score numeric` | Cosine similarity score. |
| `above_threshold bool` | Whether score is at or above `0.673784`. |
| `interpretation text` | Short label such as `Potential overlap candidate`. |

This option is safer if the team wants to keep the existing 2.3.2 `analysis_result` schema unchanged.

### 9.3 Recommendation

The recommended database direction is:

1. Add `course_embedding` because embedding storage is required for efficient pgvector retrieval.
2. Discuss whether overlap run results should extend `analysis_result` or use dedicated `course_overlap_run` and `course_overlap_candidate` tables.
3. Keep all overlap records linked to `course_revision_id`, not only `course_id`, because the course model is revision-based.

---

## 10. Integration with current course and revision workflow

Task 2.4.1 defines immutable course revisions. This is important for overlap detection because the result should always be traceable to the exact course content that was checked.

Suggested flow:

```text
1. User creates or edits a course.
2. Course API writes a new course_revision.
3. Overlap service builds enriched text from that course_revision content.
4. Service generates or updates the embedding for that revision.
5. Embedding is stored in course_embedding.
6. User or backend requests overlap check for the current revision.
7. Service searches pgvector for nearest course embeddings in the same team/programme scope.
8. Service returns ranked candidates with threshold status.
9. Curriculum tool displays the results for expert review.
```

This flow avoids a common problem: comparing a new course against old or stale vectors. Because the embedding belongs to the revision, the service can always identify which version of the course was used.

---

## 11. Relationship to existing AI analysis and suggestion tasks

The overlap service should be positioned carefully next to the existing AI tasks.

Task 2.3.2 already defines an AI analysis API with `kind='overlap'`, but that task appears to focus on LLM-generated findings and suggestions grounded in documents/frameworks. The thesis overlap detection is different: it is a vector-similarity retrieval service using embeddings, cosine similarity, and a locked threshold.

Task 2.4.2 already defines course enhancement and suggestions. The overlap service does not need to replace that. It can support it later by giving the system better evidence about similar existing courses.

A clean separation would be:

| Capability | Primary responsibility |
|---|---|
| LLM analysis / suggestions | Existing 2.3.2 and 2.4.2 direction. |
| Course CRUD and revisions | Existing 2.4.1 direction. |
| UI tabs for content, suggestions, revisions | Existing 2.4.3 direction. |
| Vector-based course overlap detection | New overlap service or new task under Epic 2. |

---

## 12. Recommended new backlog story

A suitable new story could be added under Epic 2 because it depends on course data, course revisions, pgvector, and AI/backend integration.

### Proposed story name

**Story 2.5: Vector-based course overlap detection service**

### Goal

Package the thesis overlap-detection logic as an internal backend capability that compares a course revision against existing course embeddings and returns ranked overlap candidates for expert review.

### Suggested tasks

| Task | Purpose |
|---|---|
| **Task 2.5.1: Course embedding storage and enriched text builder** | Add `course_embedding`, implement enriched text construction from `course_revision.content`, generate/store embeddings for course revisions. |
| **Task 2.5.2: Internal FastAPI overlap sidecar service** | Create an internal service similar to the markitdown sidecar, with `/health`, `/config`, and `/overlap/check`. |
| **Task 2.5.3: Curriculum backend integration for overlap checks** | Add a backend route that authorizes the user, calls the overlap service, and returns results to the app. |
| **Task 2.5.4: Overlap result persistence** | Decide whether to extend `analysis_result` or add `course_overlap_run` and `course_overlap_candidate`. |
| **Task 2.5.5: Course UI integration for overlap results** | Optional first UI: show ranked overlap candidates on the course detail page, possibly as a new tab or section. |

### MVP acceptance idea

The minimal acceptable first version could be:

```text
Given an existing course revision,
when an authorized user requests an overlap check,
then the system returns the top similar courses in the same team/programme scope,
including rank, similarity score, threshold status, matched course identity, and configuration metadata.
```

---

## 13. Open decisions for Teemu and the dev team

| Decision | Why it matters |
|---|---|
| Should the overlap logic be an internal FastAPI sidecar? | Fits the thesis implementation and the existing markitdown sidecar pattern, but still needs team approval. |
| Should the sidecar access PostgreSQL directly, or should the Next.js backend pass course content/results? | Determines service boundaries and database ownership. |
| Should overlap runs be stored in `analysis_result` or in dedicated overlap tables? | Affects schema design and future UI/history features. |
| Should embeddings be generated automatically on every new course revision or only on demand? | Affects cost, freshness, and user experience. |
| Is OpenAI embedding use acceptable for real project data? | Important for privacy, governance, and cost. |
| Is an open-source embedding fallback required? | Useful if external API use is limited later. |
| Should overlap candidates be shown in the course detail UI, suggestions tab, or a separate overlap section? | Affects frontend scope and user workflow. |
| Should results be limited to the same team/programme, organization-wide, or configurable scope? | Affects search filtering and interpretation. |

---

## 14. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Stale embeddings after course edits | Link embeddings to immutable `course_revision_id` and generate a new embedding for each changed revision. |
| External API governance concern | Confirm OpenAI use before production data is sent; consider open-source fallback later. |
| Cost from repeated embedding generation | Cache embeddings per revision and text hash. Generate only when the embedded text changes. |
| Over-reliance on similarity score | UI should frame results as review candidates, not final decisions. |
| Threshold becomes less suitable when dataset grows | Store threshold metadata and plan later recalibration with real reviewer feedback. |
| Schema overlap with existing `analysis_result` | Decide early whether to extend `analysis_result` or create dedicated overlap result tables. |
| Service boundary ambiguity | Keep authorization in the curriculum backend; keep vector logic in the overlap service. |

---

## 15. Recommended next discussion

The recommended next discussion with Teemu and the dev team should decide five points:

1. Whether to add **Story 2.5: Vector-based course overlap detection service**.
2. Whether the overlap service should follow the same internal FastAPI sidecar pattern as the markitdown service.
3. Whether `course_embedding` should be added as a new table linked to `course_revision`.
4. Whether overlap-check results should extend `analysis_result` or use dedicated overlap result tables.
5. Whether OpenAI `text-embedding-3-large` is acceptable for real project data in the first implementation.

---

## 16. Conclusion

The thesis PoC provides a validated baseline for curriculum-overlap detection. The most suitable next step is to package the reusable logic as an integration-ready backend capability for the curriculum tool.

Because the project already has PostgreSQL with pgvector and an internal Python/FastAPI sidecar pattern, the recommended direction is an internal overlap-detection service backed by pgvector. The service should use the thesis configuration as its first baseline: OpenAI `text-embedding-3-large`, enriched course text, cosine similarity, and threshold `0.673784`.

The most important database addition is a `course_embedding` table tied to immutable `course_revision` records. For overlap-result history, the dev team should decide whether to extend the existing `analysis_result` model or add overlap-specific result tables.

The service should remain human-centred. Its role is to surface ranked overlap candidates and support expert curriculum review, not to make automatic curriculum decisions.

---

## References and evidence base

- Thesis implementation and report: validated overlap-detection configuration, threshold selection, pgvector feasibility test, and Streamlit proof-of-concept.
- GitLab work items: project foundation, pgvector setup, markitdown FastAPI sidecar, AI analysis API, course/revision schema, suggestion lifecycle, and course UI direction.
- Research notes: FastAPI service packaging, pgvector integration, ML API contracts, embedding versioning, threshold management, monitoring, and educational AI/human-in-the-loop design.
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks.
- Murrugarra-Llerena, J., Alva-Manchego, F., & Murrugarra-Llerena, N. (2022). Improving embeddings representations for comparing higher education curricula.
- Malkov, Y. A., & Yashunin, D. A. (2020). Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs.
- Zablith, F., & Azad, B. (2021). Reconciling instructors’ and students’ course overlap perspectives via linked data visualization.
- Cadamuro, G., & Gruppo, M. (2023). A distribution-based threshold for determining sentence similarity.
