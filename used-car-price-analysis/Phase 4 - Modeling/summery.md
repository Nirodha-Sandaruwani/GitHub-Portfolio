## Phase 4 Modeling Report: Used Car Price Prediction

### 1. Summary

In this phase, we built models to predict used car prices. We started with simple methods like Linear Regression, then tested stronger models like Random Forest, LightGBM, XGBoost, and neural networks.
One key step was trying both raw prices and log-transformed prices as the target.
We found that log-transforming prices helped models handle the wide range of car prices much better, especially reducing big errors on expensive cars.

---

### Why Regression?

We used regression because we are predicting real price values (like $21,500), not categories or labels. This makes it a regression problem, where the goal is to estimate continuous numbers, which fits perfectly with used car prices.

---

### 2. Approach

* **Data Split**: We used an 80/20 train-test split to compare models fairly.

* **Preprocessing**: StandardScaler was applied to help models like Linear Regression and neural networks perform better.

* **Target Options**:

  * First, we predicted **price** directly.
  * Then, we predicted **log(price)** to fix the skew in the data.

* **Models Used**:

  * Simple: Linear Regression, Ridge
  * Tree-Based: Random Forest, Gradient Boosting, LightGBM, XGBoost, CatBoost
  * Deep Learning: MLP (sklearn) and a custom Keras model

* **Tuning**: We tuned a few key parameters (like tree depth, learning rate) on samples to improve performance without long training times.

---

### 3. Key Results and Observations

| Model                     | R² (Price) | MAE (Price) | RMSE (Price) | R² (Log) | MAE (Log) | RMSE (Log) |
|--------------------------|------------|-------------|--------------|----------|-----------|-------------|
| Random Forest (tuned)    | 0.8761     | 2462.82     | 6468.29      | 0.9456   | 2441.82   | 5823.26     |
| Random Forest (untuned)  | 0.8707     | 2478.66     | 6607.94      | 0.9438   | 2444.88   | 5807.27     |
| LightGBM (tuned)         | 0.8899     | 2806.33     | 6097.13      | 0.9421   | 2655.48   | 6095.34     |
| LightGBM (untuned)       | 0.8640     | 3383.00     | 6778.05      | 0.9204   | 3251.39   | 7215.27     |
| XGBoost (untuned)        | 0.8724     | 3101.79     | 6563.31      | 0.9313   | 2968.26   | 6725.43     |
| XGBoost (tuned)          | 0.8598     | 3335.38     | 6881.08      | 0.9213   | 3223.93   | 7180.59     |
| CatBoost (tuned)         | 0.8805     | 3016.79     | 6351.90      | 0.9350   | 2850.10   | 6492.39     |
| CatBoost (untuned)       | 0.8485     | 3603.90     | 7151.63      | 0.9140   | 3411.67   | 7547.14     |
| Gradient Boosting (tuned)| 0.8030     | 4303.43     | 8156.27      | -        | -         | -           |
| Gradient Boosting        | 0.8336     | 3811.91     | 7495.90      | -        | -         | -           |
| MLP Regressor (sklearn)  | 0.7762     | 4299.22     | 8693.29      | 0.8870   | 3774.78   | 8664.56     |
| MLP Regressor (tuned)    | 0.7762     | 4299.22     | 8693.29      | 0.8870   | 3774.78   | 8664.56     |
| Keras Deep Learning      | 0.7401     | 4569.04     | 9367.70      | -        | -         | -           |
| Ridge (tuned)            | 0.5352     | 7007.61     | 12528.33     | -        | -         | -           |
| Linear Regression        | 0.5352     | 7007.77     | 12528.34     | -        | -         | -           |

We didn’t apply log transformation to some models (like Ridge, Gradient Boosting, and Keras) either because their performance was already weak on raw prices or to save time by focusing only on the top-performing models.

#### A. Linear vs. Non-Linear

* **Linear Models (like Linear Regression and Ridge)** struggled.

  * R² was only around 0.53 and average errors were over $7,000.
  * These models missed complex patterns, especially failed on expensive cars.

* **Tree Models (like Random Forest, LightGBM, XGBoost)** did much better.

  * They captured interactions between features like year, mileage, and engine size.
  * Errors dropped significantly, many models predicted within ~$2,500–3,000.

* **Neural Networks** did better than linear models but worse than trees.

  * MLP reached R² ~0.77; Keras was lower (~0.74).
  * Limited training and tuning likely held them back.

#### B. Effect of Log Transformation

* Changing the target to **log(price)** helped a lot.

  * It made the data more balanced, helped models learn better.
  * Big pricing errors (especially for luxury cars) became smaller.

* **Before Log**: Best model had R² ~0.89 (LightGBM tuned)

* **After Log**: Best R² improved to ~0.94 (Random Forest tuned)

* **MAE dropped** from ~$2,800 to ~$2,400

* It helped all top models perform better.

Why the Best Model Changed:
Before log transformation, the data was very skewed, a few luxury cars had extremely high prices, which made it harder for some models to generalize. LightGBM handled this better at first. But after applying log(price), the data became more balanced and consistent. This allowed Random Forest, which benefits from evenly distributed patterns, to perform even better and overtake LightGBM in accuracy.


