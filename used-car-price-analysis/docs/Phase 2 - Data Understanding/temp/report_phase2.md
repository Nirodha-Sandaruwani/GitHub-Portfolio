# Phase 2 – Data Understanding

## 1. Introduction

This stage focuses on developing a deep understanding of the data collected at the commencement of the project.

This involves the identification of data formats, content, and structure; preliminary exploration; visualization of patterns; quality checks; and the identification of possible complementary data sources.

This dataset consists of listings for used cars, compiled from an online automotive marketplace. Each record in the dataset corresponds to one car listing, describing its features, history, and market information.

## 2. Data Collection

### 2.1 Data Sources and Formats

- Primary source: CSV file (structured tabular format)

- Size: 3,000,040 rows × ~66 columns

- Formats used

| **Data Type**            | **Attributes**                           |
| ------------------------ | ---------------------------------------- |
| **Numeric (int, float)** | price, mileage, fuel economy, horsepower |
| **Categorical (object)** | make, model, color, transmission         |
| **Boolean (True/False)** | accident history, certification status   |
| **Text (string)**        | description, options, dealer name        |
| **Geographical (float)** | latitude, longitude                      |
| **Datetime (string)**    | (to be converted in next phase)          |

Due to its large size and high number of columns, the dataset was processed using Polars for efficient handling and analysis.


### 2.2 Key Identifiers

Each vehicle entry is uniquely identified using important reference fields, including:

- VIN (Vehicle Identification Number) – primary unique identifier

- Brand & Model – vehicle make and specific model

- Manufacturing Year – year of production

These identifiers help detect duplicates, track individual vehicles, and support grouping and analysis.

## 3. Description of the Data

### 3.1 Data Structure Overview

The dataset contains hundreds of thousands of vehicle records with 66+ attributes per entry.
It includes a mix of numerical and categorical variables, where most columns (~70%) are categorical.

The data structure consists of the following key groups:

- Vehicle identification (VIN, brand, model, year)

- Technical specifications (engine size, power, fuel type, transmission)

- Usage details (mileage, condition, inspection status)

- Market information (price, currency, seller type, location)

- Environmental data (emission class, fuel consumption)

| Category           | Example Columns                                                     | Description                 |
| ------------------ | ------------------------------------------------------------------- | --------------------------- |
| Identification     | `vin`, `listing_id`                                                 | Unique identifiers          |
| Vehicle Details    | `make_name`, `model_name`, `year`, `trim_name`, `body_type`         | Descriptive information     |
| Performance        | `engine_cylinders`, `horsepower`, `torque`, `engine_displacement`   | Engine and power data       |
| Fuel Economy       | `city_fuel_economy`, `highway_fuel_economy`, `combine_fuel_economy` | Efficiency indicators       |
| Market & Condition | `price`, `mileage`, `daysonmarket`, `owner_count`                   | Listing and usage info      |
| Certification      | `is_new`, `is_certified`, `is_cpo`, `has_accidents`, `theft_title`  | Vehicle history             |
| Dealer Information | `sp_name`, `city`, `dealer_zip`, `latitude`, `longitude`            | Seller location and details |
| Truck-Specific     | `bed_height`, `bed_length`, `cabin`                                 | Applies only to pickups     |
| Text Fields        | `description`, `major_options`, `main_picture_url`                  | Unstructured text or links  |

### 3.2 Variable Categories

The dataset attributes are grouped as follows:

| Category           | Example Columns                                                     | Description                 |
| ------------------ | ------------------------------------------------------------------- | --------------------------- |
| Identification     | `vin`, `listing_id`                                                 | Unique identifiers          |
| Vehicle Details    | `make_name`, `model_name`, `year`, `trim_name`, `body_type`         | Descriptive information     |
| Performance        | `engine_cylinders`, `horsepower`, `torque`, `engine_displacement`   | Engine and power data       |
| Fuel Economy       | `city_fuel_economy`, `highway_fuel_economy`, `combine_fuel_economy` | Efficiency indicators       |
| Market & Condition | `price`, `mileage`, `daysonmarket`, `owner_count`                   | Listing and usage info      |
| Certification      | `is_new`, `is_certified`, `is_cpo`, `has_accidents`, `theft_title`  | Vehicle history             |
| Dealer Information | `sp_name`, `city`, `dealer_zip`, `latitude`, `longitude`            | Seller location and details |
| Truck-Specific     | `bed_height`, `bed_length`, `cabin`                                 | Applies only to pickups     |
| Text Fields        | `description`, `major_options`, `main_picture_url`                  | Unstructured text or links  |

### 3.3 Missing Values & Data Types

The dataset contains both numerical and categorical (string-based) features, including a small number of boolean and date values.
Since the data comes from real-world listings, several columns contain missing values, particularly in optional or vehicle-specific fields (example : truck measurements, seller details, and fuel economy).

Common observations:

- Numerical columns: price, mileage, engine specifications, fuel economy → may include missing or zero values.

- Categorical columns: body type, trim, fuel type, seller location → may contain missing or inconsistent labels.

- Truck specific fields: bed_length, bed_height, cabin → often missing for non-truck vehicles.

- Text fields: description, major_options → unstructured content, may contain nulls.

- Identifiers: VIN and listing_id are mostly complete as they are required fields.

Data types include:

| Data Type                 | Example Columns                                         |
| ------------------------- | ------------------------------------------------------- |
| String (Categorical/Text) | `make_name`, `body_type`, `city`, `description`         |
| Integer/Float (Numerical) | `price`, `mileage`, `horsepower`, `engine_displacement` |
| Boolean                   | `is_new`, `has_accidents`, `theft_title`                |
| Date                      | `listed_date`, `inspection_valid_until`                 |

Handling missing values and validating data types are essential steps before analysis and modeling.

## 4. Data Exploration and Visualization

### 4.1 Basic Statistical Analysis

Basic statistics were computed to understand the distribution and range of key numerical variables.

Key insights include:

- Price and mileage show high variance, indicating a wide range of vehicle conditions and market values.

- Engine power, displacement, and fuel economy values vary by vehicle type and model year.

- Some numerical fields contain extreme values or zeros, requiring validation or outlier handling.

- Categorical attributes show high cardinality, especially in model_name, trim, and city, which affects grouping and analysis.

Descriptive statistical measures used:

- Mean, median, min, max, standard deviation for numerical fields

- Value counts and frequency distribution for categorical fields

These statistics help identify data spread, anomalies, and features that may need cleaning or transformation.

### 4.2 Data Visualizations

4.2 Data Visualizations

Several visualizations were created to explore patterns and relationships within the dataset:

- **Correlation Heatmap (numeric features)**
Reveals meaningful relationships among numerical variables. Strong correlations exist between:

    - engine_displacement and horsepower
        
    - Fuel economy fields (city, highway, combined MPG)

- **Histograms (all numeric columns)**
Show that many numerical attributes (e.g., price, mileage) are right-skewed with noticeable outliers.

- **Distribution of Bed Type**
Confirms that truck-specific fields (e.g., bed) are missing for most vehicles, demonstrating that these features are not generalizable across all listings.

- **Top 10 Most Common Car Brands**
A bar chart shows the dominance of a few manufacturers, indicating high class imbalance in the make_name feature.

- **Price vs. Year (Scatter Plot)**
Shows a general trend of higher prices for newer vehicles, though there are large variations within the same model year.

- **Horsepower vs. Engine Displacement (Regression Plot)**
Displays a clear positive linear relationship, confirming expected mechanical behavior: larger engines produce more power.

These visualizations help identify variable distributions, outliers, correlations, and feature imbalance—critical insights for later data cleaning and model training.

### 4.3 Grouping and Aggregation Analysis

Data was grouped at different levels to extract meaningful business insights such as pricing behavior, demand trends, and vehicle value impact factors.

| **Grouping Level**                                                | **Example Use Case**                                | **Business Insight / Benefit**                              |
| ----------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------- |
| **Manufacturer / Make (`make_name`)**                             | Compare price differences (e.g., Toyota vs BMW)     | Identify brands with higher resale value or faster sales    |
| **Vehicle Type (`body_type`)**                                    | Compare SUVs, sedans, trucks                        | Helps understand high-demand categories and inventory focus |
| **Fuel Type (`fuel_type`)**                                       | Electric vs Hybrid vs Gas vs Diesel                 | Detect eco-trends and fuel impact on price performance      |
| **Transmission (`transmission`)**                                 | Automatic vs Manual preference                      | Understand buyer demand and resale probability              |
| **Geographic Location (`city`, `dealer_zip`)**                    | Compare prices by region                            | Support region-based pricing and demand strategies          |
| **Vehicle History (`has_accidents`, `salvage`, `frame_damaged`)** | Impact of damage on price or selling duration       | Improve valuation models using risk history signals         |
| **Year & Mileage (`year`, `mileage`)**                            | Depreciation and aging analysis                     | Track price drop patterns and resale timing                 |
| **Dealer (`sp_name`, `sp_id`)**                                   | Compare franchise vs independent seller performance | Identify high-performing sellers for partnership insights   |

Grouping enables:

- Market trend discovery (brand, fuel, body type demand)

- Pricing strategy improvements (location, mileage, condition impact)

- Dealer performance benchmarking

- Better feature selection for predictive modeling

## 5. Data Quality Assessment

### 5.1 Completeness

5.1 Completeness

Data completeness was evaluated across all key attributes. Most identifier fields (vin, listing_id) are nearly complete, ensuring reliable record tracking. However, missing values are common in:

- Vehicle-specific attributes (e.g., bed_length, bed_height, cabin) → only relevant for trucks

- Fuel and performance fields (e.g., fuel_economy, horsepower)

- Condition or history attributes (accident, damage flags)

- Unstructured text (description, major_options)

Summary:

- Core fields are mostly complete 

- Optional and vehicle-specific features have high missing rates 

- Missing data handling will be required before modeling

### 5.2 Consistency and Format Issues

- Some numeric columns include text units, example : "36 in" → should be converted to numeric.

- Date columns (listed_date) are stored as strings and require conversion using pd.to_datetime().

- Categorical values like color or body type have inconsistent capitalization ("Black" vs "black").

### 5.3 Outliers and Anomalies

- Outliers detected: in price, mileage, daysonmarket.

These will be addressed using percentile trimming or robust scaling in Phase 3.

### 5.4 Duplicates

- Duplicate rows exist, mainly from repeated listings or same VIN entries.

Deduplicate using drop_duplicates() or drop_duplicates(subset=['vin']) to keep unique vehicles.


## 6. Visualization Tools Used

| Tool                            | Purpose                                        |
| ------------------------------- | ---------------------------------------------- |
| **Pandas**                      | Quick statistical summaries and grouping       |
| **Matplotlib**                  | Custom histograms and boxplots                 |
| **Seaborn**                     | Correlation heatmaps and pairplots             |

Each tool allows dynamic visualization of data patterns and helps identify quality issues before modeling.

## 7. Integration with Other Data Sources

| Data Source                            | Type                    | Connection Method              | Benefit                                  |
| -------------------------------------- | ----------------------- | ------------------------------ | ---------------------------------------- |
| **Fuel price dataset (API or CSV)**    | External                | Merge by `date` or `region`    | Enables cost-per-km analysis             |
| **Geographic / City income data**      | Public dataset          | Join by `city` or `dealer_zip` | Helps explain regional price differences |
| **Vehicle recall / accident database** | External API            | Join by `vin`                  | Adds safety or reliability factors       |
| **Weather / Climate data**             | API (e.g., OpenWeather) | Merge by location and date     | Context for listing activity or demand   |


## 8. Summary of Findings

| Aspect                      | Observation                                                           |
| --------------------------- | --------------------------------------------------------------------- |
| **Data completeness**       | Good overall; some fields missing or empty                            |
| **Data consistency**        | Mostly consistent; unit conversion needed                             |
| **Data quality issues**     | Missing fuel economy, formatting errors, outliers                     |
| **Relationships**           | Strong correlations between engine size, horsepower, and fuel economy |
| **Grouping insights**       | Price and days-on-market vary significantly by make and region        |
| **Visualization tools**     | Pandas, Seaborn, Matplotlib                       |
| **Additional data sources** | Fuel, region, and recall datasets can enrich analysis                 |


## 9. Conclusion

This phase provided a comprehensive understanding of the dataset. The dataset provides strong signals for modeling vehicle resale price and sales trends.

We identified the data’s structure, quality, relationships, and limitations while producing descriptive statistics and visualizations.

Key takeaways:

- The dataset is reliable and diverse, with rich vehicle and market information.

- Missing and inconsistent data require cleaning before modeling.

- Grouping and correlation analyses reveal meaningful relationships between variables.

- Opportunities exist to integrate complementary data sources for deeper insights.

The dataset is now ready for Phase 3: Data Preparation, where missing values, outliers, and formatting issues will be addressed before modeling and analysis.