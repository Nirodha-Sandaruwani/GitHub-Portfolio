# AI Curriculum Review System

An applied AI proof of concept for detecting possible curriculum overlap between university courses using semantic embeddings and vector similarity search.

The project was developed in the context of JAMK University of Applied Sciences and formed the implementation basis of my Bachelor’s thesis:

**Vector Similarity Search for Curriculum Overlap Detection: Embedding Models and Threshold Optimization**

The goal is to support curriculum experts by identifying potentially overlapping courses and reducing the amount of manual course-by-course comparison.

---

## Project Overview

Curriculum review becomes increasingly difficult as the number of courses grows and similar educational content is described using different wording.

Traditional keyword matching can miss these relationships because two courses may cover similar topics without using exactly the same words.

This project explores semantic similarity as a solution.

The workflow converts course descriptions into vector embeddings, compares them using similarity measures, applies an evaluated threshold, and returns possible overlap candidates for expert review.

The system is designed as a **decision-support tool**, not as an automated curriculum decision-maker.

---

## System Workflow

```text
Course Data
    ↓
Course Text Preparation
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