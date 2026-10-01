# AI vs Human Text Classification

A deep learning benchmark for classifying text as **human-written** or **AI-generated** using multiple neural network architectures.

The project covers data preparation, text preprocessing, model development, evaluation, and comparative analysis of accuracy and training efficiency.

---

## Project Overview

The original dataset contained **487,235 text samples** with two classes:

- Human-written: 305,797
- AI-generated: 181,438

After preprocessing and filtering invalid short texts, the cleaned dataset contained **487,225 samples**.

For model benchmarking, a reproducible subset of **10,000 samples** was used:

- Human-written: 6,325
- AI-generated: 3,675
- Training set: 8,000
- Test set: 2,000

---

## Workflow

```text
Raw Text Dataset
      ↓
Text Cleaning
      ↓
Invalid / Short Text Filtering
      ↓
10K Benchmark Subset
      ↓
Tokenization + Padding
      ↓
Deep Learning Models
      ↓
Accuracy + Confusion Matrix
      ↓
Training-Time Comparison
```

---

## Text Processing

The benchmark uses:

- cleaned text as the model input
- binary target: `0 = Human`, `1 = AI`
- vocabulary limit: **20,000 words**
- sequence length: **256 tokens**
- embedding dimension: **64**
- stratified 80/20 train-test split

---

## Models Evaluated

Five deep learning architectures were compared:

- Bidirectional LSTM
- 1D CNN
- Bidirectional GRU
- FastText-like shallow network
- CNN + GRU hybrid

---

## Results

| Model | Test Accuracy | Training Time |
|---|---:|---:|
| **FastText-like** | **98.25%** | **23.46 s** |
| CNN | 97.75% | 33.50 s |
| CNN + GRU Hybrid | 97.65% | 203.53 s |
| BiLSTM | 97.25% | 417.96 s |
| BiGRU | 95.20% | 1114.68 s |

The **FastText-like model** achieved the highest test accuracy while also requiring the least training time in this benchmark.

Its architecture consists of:

```text
Embedding
    ↓
Global Average Pooling
    ↓
Dense Layer
    ↓
Dropout
    ↓
Sigmoid Output
```

This result shows that a relatively simple architecture can perform competitively for this dataset without the computational cost of recurrent models.

---

## Evaluation

Each model was evaluated using:

- test accuracy
- confusion matrix
- validation accuracy
- validation loss
- training time

The final analysis compares both predictive performance and computational efficiency rather than accuracy alone.

---

## Technologies

```text
Python
Pandas
NumPy
TensorFlow
Keras
Scikit-learn
Matplotlib
Jupyter Notebook
```

---

## Repository Structure

```text
ai-vs-human-text-classification/
├── 01_data_preparation.ipynb
├── 02-deep_learning_model.ipynb
├── 03_analysis.ipynb
├── data/
└── README.md
```

---

## Reproducibility

The project uses a fixed random seed for sampling and train-test splitting.

The model notebook also stores benchmark artifacts, including:

- model accuracy
- training time
- training histories
- confusion matrices

These artifacts are reused in the analysis notebook for consistent visual comparison.

---

## Limitations

The reported results apply to the dataset and preprocessing pipeline used in this project.

AI-text detection performance may change significantly across:

- different language models
- writing domains
- text lengths
- edited or mixed-authorship text
- future generations of AI systems

The classifier should therefore be treated as an experimental benchmark rather than a universal AI-content detector.