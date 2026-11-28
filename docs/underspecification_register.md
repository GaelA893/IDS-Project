# Underspecification Register

| ID | Category | Component | Description in Paper | Ambiguity / What Was Missing | Our Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **UR-01** | Architecture | Output Layer Autoencoder | Output autoencoder aggregates RMSE from ensemble. | Learning rate η and momentum during online updates. | Use author default lr = 0.1. |
| **UR-02** | Data | Packet Preprocessing & Features | 115 damped incremental statistics (100 1D + 15 2D) over 5 temporal windows. | Paper mentions 115 features in §IV-B but notes n=198 in §V-C runtime tests. | Standardize on 115 features, exactly matching the provided CSV datasets. |
| **UR-03** | Threshold | Anomaly Cutoff (θ) | "θ is set to max RMSE observed during clean grace period." | Some implementations use μ + 3σ instead of strict max. | Calculate and compare both strict max and μ + 3σ. |
| **UR-04** | Training | Training Grace Period ($N_{train}$) & Splits | "Trained on the first million packets" (§V-A); benign grace period before execution. | Mirai total capture is only 764,137 packets, and attack starts at pkt 121,621 (1M is impossible and would train on attacks). | Train Mirai on first 55,000 packets; train SYN DoS and ARP MitM on first 1,000,000 packets. Verified 100% clean via PR #27. |
| **UR-05** | Hardware | Throughput / Timing | Benchmarked on Raspberry Pi and Core i7. | Python 2.7 vs 3.x and C-extension compilation. | Benchmark on standardized machine; separate accuracy from throughput. |

