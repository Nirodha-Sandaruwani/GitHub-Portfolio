**PHASE 5 – EVALUATION SUMMARY (USED CAR PRICE PREDICTION)**



This phase evaluates the performance of all models developed in Phase 4. The results were reviewed using both quantitative metrics (R², MAE, RMSE) and qualitative observations such as stability of predictions, behaviour across price ranges, residual patterns, and feature importance consistency. The evaluation confirms that tree-based ensemble models are the most reliable and practical solution for predicting used car prices.




**1. Evaluation of Obtained Results**



Random Forest (tuned) delivered the best performance with the highest R² (0.946 on log price) and the lowest errors. LightGBM and CatBoost followed closely with strong accuracy and stable predictions. XGBoost performed well even without tuning, showing robust defaults. MLP neural networks achieved moderate performance, while linear models performed poorly due to the dataset’s nonlinear relationships. Residual analysis shows tree models provide consistent, unbiased predictions, while neural networks show higher error variance on high-priced vehicles.





**2. Analysis and Comparison of Models**



Tree-based models captured complex patterns effectively and achieved the lowest errors. Neural networks were flexible but sensitive to scaling and required more tuning. Linear models were interpretable but not suitable for complex price patterns. Feature importance across models consistently highlighted horsepower, torque, year, and mileage as the strongest predictors, confirming domain expectations.





**3. Review of the Modeling Process**



The modeling pipeline was implemented correctly with consistent preprocessing, log transformation, and evaluation. Predictions were validated in both log and original price units. Residuals and feature importance were checked for logical correctness. The process confirms no major errors in training or evaluation, and the log-transformed target significantly improved prediction stability.





**4. Decisions for Next Phases**



Next steps include extending hyperparameter tuning (especially for XGBoost, CatBoost, and neural networks), experimenting with stacking/ensembling, and improving feature engineering. Additional features such as regional demand, trim level, or maintenance history could further enhance performance. Cross-validation should be added for more reliable accuracy estimates. Weighted metrics or custom loss functions may be used to prioritize performance on expensive cars.





**5. Additional Evaluation Insights**



Machine learning tree-based methods worked best overall, providing high accuracy, robustness, and interpretability. Neural networks performed moderately but were limited by data size and tuning. Linear models failed to capture nonlinear relationships. Further improvements may focus on tuning, engineered features, and addressing rare high-priced vehicles, which remain the largest source of prediction error.

