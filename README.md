# Modeling-the-Regional-Spread-of-COVID-19-in-Central-and-Eastern-Europe-Using-Diebold-Yilmaz-indexes

Overview

This project investigates the spatiotemporal dynamics of COVID-19 transmission in Central and Eastern Europe, with a particular focus on Hungary. The COVID-19 pandemic, since its outbreak in 2019, has had profound economic, social, health, cultural, technological, and societal impacts worldwide. The virus reached the region in multiple waves, resulting in periods of high case numbers and periods of relative calm, which allowed societies more freedom of movement.

This study aims to model and analyze how the virus spread both within and between countries, uncovering the underlying mechanisms driving its propagation.

Objectives

The main research objectives of this project are:

To determine the extent to which countries operated as open or closed systems in terms of case transmission.

To analyze intra-country transmission directions across different regions.

To explore inter-country connections and the potential social or economic factors underlying these links.

Methodology

A network-based approach is used to capture the complex interactions between regions.

Countries are divided into NUTS2-level regions, providing a standardized territorial framework across Europe.

Data preprocessing ensures a consistent panel dataset for analysis.

Statistical and econometric methods applied include:

VAR (Vector Autoregression) models

Impulse Response Functions

Forecast Error Variance Decomposition

Diebold-Yilmaz indices are employed to quantify information flow and network connectivity between regions.

Results

Key findings of the analysis include:

A robust network structure exists among regions in Hungary, Austria, Slovakia, and Poland, showing stable information flow with patterns varying across pandemic waves.

Pandemic waves, mobility restrictions, and infection dynamics are strongly interconnected: strict measures significantly reduce network connectivity, while easing restrictions leads to stronger cross-border transmission.

Major urban centers (e.g., Budapest, Vienna, Warsaw, Kraków) act as primary transmission hubs due to concentrated mobility, economic activity, and interpersonal interactions.

Less intuitive patterns were observed, such as Western Transdanubia (Hungary) and Opolskie (Poland) consistently acting as key receiver regions due to their location in major transport hubs.

Temporal shifts in transmission directionality were detected during the fourth wave, highlighting the dynamic nature of the pandemic and the importance of spatiotemporal network analysis.

Significance

This project contributes to a better understanding of regional pandemic transmission mechanisms. The applied methodology is suitable for analyzing future outbreaks, mobility patterns, or economic shocks. The results provide insights for:

Epidemiological preparedness and intervention planning

Cross-border coordination

Decision-support systems for policymakers

The findings also lay the groundwork for further research, particularly on temporal network instability, deeper integration of mobility patterns, and higher-resolution spatial models.

Technologies

Python / R for data analysis

VAR modeling and econometric analysis

Network analysis using Diebold-Yilmaz indices

Data visualization with Matplotlib, Seaborn, or Plotly
