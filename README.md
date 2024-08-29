# Delay-allowed Differentially Private Data Stream Release

## About

This repository supports the paper "Delay-allowed Differentially Private Data Stream Release". 

It supports the following features:

- Publishing differentially private data streams while allowing for delays.
- Optimizing the noise sensitivity of the data streams.

It has the following benefits: 

- Modularity: each algorithmic module can be independently invoked.
-  Testability: a testing module is provided, enabling the code testable.

 This code is used to publish privacy-preserving data streams in scenarios with low requirements for data timeliness. Users can control the length of the publishing delay by setting the delay\_time parameter. Two types of publishing strategies: Group-based and Order-based strategies have been proposed. Please refer to the detailed analysis in the paper for the algorithm selection in practical tasks.

### Structure of this Repository

![orgianzer](https://github.com/XiaochenLi-w/Stream-release-with-delay-time/blob/ae/organization.png)

```
data_release
.
├─data
│      COVID19_DEATH.csv
│      footmart.csv
│      ILINet.csv
│      unemployment.csv
│
├─estimator
│      est_compall.py
│      est_delaylength.py
│      est_group.py
│      est_order.py
│      est_sensitivity.py
│
├─methods
│      bucOrder.py
│      common_tools.py
│      compOrder.py
│      continuous.py
│      discontinuous.py
│      naive.py
│      sensitivity_calc.py
│
└─other_competitor
        adapub.py
        DPI_DEMO_script.py
        est_other.py
```

### Prerequisites

This project is made with Python. The following open source packages are used in this project:

- `numpy`
-  `math`
-  `random`
-  `os`
-  ` sys`
-  `matplotlib`
- `scikit-learn` 

### Evaluation

To verify all experimental results presented in the paper, please refer to the Evaluation section in ‘ndss_ae_appendix.pdf’. It will provide the detailed steps to ensure a comprehensive validation of the experiments.

- Compare Delay-allowed Approaches with Baseline Methods:

To evaluate all the proposed method, set

```
est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time)
```

 Simply run:

```
python ./data_release/estimator/est_compall.py
```
The results and the graphs will be directly output to the screen.

- Evaluate Effectiveness of Data Sensitivity Truncation:

To use the sensitivity truncation mechanism, you can set the parameter `Flag=1`, `interval`  refers to the number of data batches between updates, `num_`  is specifically used by CompOrder as the length of each data batch.
```
est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time, flag = 1, interval_ = 5, num_ = 100)
```

Simply run:

```
python ./data_release/estimator/est_sensitivity.py
```

- Evaluate the Impact of the Delay Length:

Simply run:

```
python ./data_release/estimator/est_delaylength.py
```

- Evaluate the Impact of the Bucket Size:

Simply run:

```
python ./data_release/estimator/est_order.py
```

- Evaluate the Impact of the Threshold:

Simply run:

```
python ./data_release/estimator/est_group.py
```

> [!NOTE]
>
> The file paths in the code are set according to the Windows system. If testing on other systems, you may need to modify the dataset file reading paths accordingly.

- Evaluate the SOTA method: Adapub and DPI.

For Adapub, simply run:

```
python ./data_release/other_competitor/est_other.py
```

For DPI, first run:

```
pip install wheel scipy scikit-learn
```

Then, run:

```
python ./data_release/other_competitor/DPI_DEMO_script.py
```

> [!NOTE]
>
> The code for this part comes from the open source libraries of papers “DPI: https://github.com/ShuyaFeng/DPI” and “Adapub: https://dbresearch.uni-salzburg.at/projects/dpbench/”.

## Functionality

This code includes five main data stream publishing algorithms, which can support future research for invocation and expansion.

- [PeGaSus](https://dl.acm.org/doi/abs/10.1145/3133956.3134102) - `data_release.methods.continuous.pegasus_nodelay`

  ```
  ##Input##
  # data stream: ex, domain size: domain_low, domain_high, 
  # privacy strength: eps, threshold: tau
  # Sensitivity Reduce/Non-Reduce: flag=1/0, 
  # Number of windows in update interval: interval_, Number of timestamps within a window: num_
  ##Output##
  # Noisy version of the data stream
  
  pegasus_delay(ex, domain_low, domain_high, eps, tau, flag = 0, interval_ = 5, num_ = 100)
  ```

- Continuous Grouping Method - `data_release.methods.continuous.reduce_noise_continuous`

  ```
  ##Input##
  # data stream: ex, domain size: domain_low, domain_high, 
  # privacy strength: eps, threshold: tau, Delay time: delay_time
  # Sensitivity Reduce/Non-Reduce: flag=1/0, 
  # Number of windows in update interval: interval_
  ##Output##
  # Noisy version of the data stream
  
  reduce_noise_continuous(ex, domain_low, domain_high, eps, tau, delay_time, flag = 0, interval_ = 5)
  ```

- Discontinuous Grouping Method - `data_release.methods.discontinuous.discontin_reduce`

  ```
  ##Input##
  # data stream: ex, domain size: domain_low, domain_high, 
  # privacy strength: eps, threshold: tau, Delay time: delay_time
  # Sensitivity Reduce/Non-Reduce: flag=1/0, 
  # Number of windows in update interval: interval_
  ##Output##
  # Noisy version of the data stream
  
  discontin_reduce(ex, domain_low, domain_high, eps, delay_time, tau, flag = 0, interval_ = 5)
  ```

- CompOrder Method - `data_release.methods.compOrder.comporder`

  ```
  ##Input##
  # data stream: ex, domain size: domain_low, domain_high, 
  # privacy strength: eps, Delay time: delay_time,
  # Sensitivity Reduce/Non-Reduce: flag=1/0, 
  # Number of windows in update interval: interval_, Number of timestamps within a window: num_
  ##Output##
  # Noisy version of the data stream
  
  comporder(ex, domain_low, domain_high, eps, delay_time, flag = 0, interval_ = 5, num_ = 100)
  ```

- BucOrder Method - `data_release.methods.bucOrder.order_advance`

  ```
  ##Input##
  # data stream: ex, domain size: domain_low, domain_high, 
  # privacy strength: eps, Delay time: delay_time, Size of each Bucket: buc_size,
  # Sensitivity Reduce/Non-Reduce: flag=1/0, 
  # Number of windows in update interval: interval_
  ##Output##
  # Noisy version of the data stream
  
  order_advance(ex, domain_low, domain_high, eps, delay_time, buc_size, flag = 0, interval_ = 5)
  ```

### LICENSE

MIT License
