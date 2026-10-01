# Phase 6 Deployment Plan

This phase explains how the final used car price prediction model will be deployed, monitored, and maintained in a real operational environment. The purpose of the deployment plan is to ensure that the model can be used reliably by its intended users and that its performance remains stable over time.

## 6.1 Plan and Implement Deployment

Based on the results from previous phases, the Random Forest model (log-transformed target) will be deployed as the final predictive system. The deployment process includes packaging the model, preparing the environment, and making the prediction service available to end users.

### Deployment Steps

1.  **Select a Production Platform**
    The model will be hosted on a cloud-based virtual machine such as
    **AWS EC2**, **Azure VM**, or **Google Cloud**, or alternatively on
    a **local institutional server** provided by the university.

2.  **Prepare the Model Files**

    -   Export the trained model into a file format such as `.pkl` or
        `.joblib`.
    -   Collect all dependencies in a `requirements.txt` file.
    -   Save preprocessing steps (scaling, encoding) if used.

3.  **Create the Prediction Service (API)**
    A lightweight API will be implemented using **Flask** or
    **FastAPI**.
    This API will expose a `/predict` endpoint that accepts user input
    and returns the predicted price.

4.  **Upload to the Production Server**
    Deployment can be done using SSH, GitHub, or cloud deployment
    tools.
    After uploading, the environment will be created and the API
    launched.

5.  **Testing Deployment**
    Test cases will be executed to verify prediction accuracy, API
    performance, system stability, and error handling.

## 6.2 Plan Monitoring

Monitoring ensures long-term stability of the prediction system.

### Monitoring Components

-   **Model performance tracking**
-   **System monitoring** (CPU, memory, response time)
-   **Logging** of prediction requests and system events
-   **Alerts** for failures or abnormal patterns

## 6.3 Plan Maintenance

Maintenance ensures the system stays accurate and functional as market
conditions change.

### Maintenance Tasks

-   Updating the model when new data becomes available
-   Periodic retraining to improve prediction accuracy
-   Updating software dependencies and libraries
-   Refining the user interface if needed
-   Documenting every update and maintaining version control

## 6.4 Produce a Final Report

A final project report will be created and delivered to the client and
stakeholders. It will include: 

- Project goals
- Data preparation
- Model training and comparison
- Final chosen model
- Deployment process
- Limitations
- Recommendations and future improvements

## 6.5 Review the Project

The project will be reviewed to assess whether goals were met and
identify lessons learned.

### Review Points

-   Model performance
-   Tool effectiveness
-   Challenges encountered
-   Improvement areas
-   Feedback from users or supervisors

# Additional Questions

### 1. What production service platform will be used?

A cloud-based virtual machine or institutional server supporting Python.

### 2. How to upload a model to a production server?

Upload via GitHub, SSH, or cloud tools, then install dependencies and
run the API.

### 3. How to upload new data to the production server?

Using SFTP, a web form, or automated pipelines.

### 4. What kind of user interface will be needed?

A simple web-based interface for entering car details and receiving
predictions.

### 5. Who will use the model?

Students, researchers, car dealers, or technical staff who need price
predictions without coding knowledge.
