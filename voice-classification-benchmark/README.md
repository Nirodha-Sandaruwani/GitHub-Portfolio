# Voice Classification Benchmark

A supervised machine learning benchmark for classifying voice samples from acoustic features and comparing the performance of several classical classification methods.

The project focuses on preprocessing, feature analysis, model comparison, dimensionality reduction, confusion-matrix evaluation, and ROC/AUC analysis.

---

## Project Overview

The source dataset contained **3,168 voice samples** with **20 numerical acoustic features** and a balanced binary label distribution:

- 1,584 male-labelled samples
- 1,584 female-labelled samples

Preprocessing included:

- duplicate removal
- missing-value checks
- label normalization
- Z-score outlier filtering
- numerical feature scaling
- stratified train-test splitting

After preprocessing, the working dataset contained **2,795 samples**.

---

## Dataset Features

The dataset contains acoustic measurements including:

```text
meanfreq
sd
median
Q25
Q75
IQR
skew
kurt
sp.ent
sfm
mode
centroid
meanfun
minfun
maxfun
meandom
mindom
maxdom
dfrange
modindx
```

The final train-test split contained:

- Training samples: **2,236**
- Test samples: **559**
- Features: **20**

---

## Workflow

```text
Voice Feature Dataset
        ↓
Data Cleaning
        ↓
Outlier Removal
        ↓
Feature Scaling
        ↓
Train-Test Split
        ↓
Multiple Classifiers
        ↓
Accuracy + Confusion Matrix
        ↓
Feature Importance + ROC/AUC
```

---

## Models Evaluated

The benchmark compares:

- Decision Tree
- Support Vector Machine
- k-Nearest Neighbors
- Gaussian Naive Bayes
- Random Forest
- PCA + Random Forest

---

## Main Evaluation Results

| Classifier | Accuracy |
|---|---:|
| **Random Forest** | **98.75%** |
| SVM | 98.21% |
| kNN | 98.03% |
| Decision Tree | 96.60% |
| PCA + Random Forest | 94.63% |
| Gaussian Naive Bayes | 92.49% |

Random Forest achieved the strongest accuracy in the main evaluation run.

---

## Feature Analysis

Random Forest feature importance identified the strongest predictors as:

1. **`meanfun`** — mean fundamental frequency
2. **`IQR`** — interquartile range of voice frequency
3. **`Q25`**
4. **`sd`**
5. **`sp.ent`**

The two strongest features, `meanfun` and `IQR`, were also used for visual exploration of class separation.

---

## PCA Experiment

Principal Component Analysis was evaluated together with Random Forest.

The PCA-based configuration achieved **94.63% accuracy**, lower than Random Forest using the original feature space. In this experiment, dimensionality reduction therefore did not improve classification performance.

---

## Evaluation

The models were compared using:

- accuracy
- confusion matrices
- classification reports
- feature importance
- ROC curves
- AUC
- two-feature visualizations

This provides both predictive and interpretability-oriented comparison across different learning methods.

---

## Technologies

```text
Python
Pandas
NumPy
Scikit-learn
Matplotlib
Jupyter Notebook
```

---

## Repository Structure

```text
voice-classification-benchmark/
├── voice_classification.ipynb
└── README.md
```

---

## Limitations

This project is an educational machine learning benchmark based on the acoustic features and binary labels supplied by the source dataset.

The results should not be interpreted as a general-purpose system for determining a person's gender or identity from voice. Performance may change across recording conditions, languages, microphones, speakers, and populations not represented in the dataset.
