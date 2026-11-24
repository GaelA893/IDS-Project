# Underspecification Register

| ID | Category | Component | Description in Paper | Ambiguity / What Was Missing | Our Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **UR-01** | Architecture | Output Layer Autoencoder | Output autoencoder aggregates RMSE from ensemble. | Learning rate η and momentum during online updates. | Use author default lr = 0.1. |
| **UR-02** | Data | Packet Preprocessing | 100 damped incremental statistics over 5 windows. | Timestamp precision and out-of-order handling. | Use pre-extracted CSV features from authors. |
| **UR-03** | Threshold | Anomaly Cutoff (θ) | "θ is set to max RMSE observed during clean grace period." | Some implementations use μ + 3σ instead of strict max. | Calculate and compare both strict max and μ + 3σ. |
| **UR-04** | Training | Grace Period (m) | m = 50,000 packets clean traffic. | Whether first 50k packets are strictly benign in all attacks. | Validate first 50k labels in CSV are all 0. |
| **UR-05** | Hardware | Throughput / Timing | Benchmarked on Raspberry Pi and Core i7. | Python 2.7 vs 3.x and C-extension compilation. | Benchmark on standardized machine; separate accuracy from throughput. |
