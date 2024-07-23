# Delay-allowed Differentially Private Data Stream Release

This repository supports the paper "Delay-allowed Differentially Private Data Stream Release", and we will attach the link after the paper is officially published. This code is used to publish privacy-preserving data streams in scenarios with low requirements for data timeliness. Users can control the length of the publishing delay by setting the delay\_time parameter. Two types of publishing strategies: Group-based and Order-based strategies have been proposed. Please refer to the detailed analysis in the paper for the algorithm selection in practical tasks.

### Structure of this Repository

![orgianzer](.\organization.png)

The ‘data_delease’ file contains four folders.

- ‘./data’ contains all the datasets used for testing;
- ‘./methods’ includes all the methods proposed in the paper, as well as the implementation of the baseline methods;
- ‘./estimator’ contains test code for evaluating all methods;
-  ‘./other_competetor’ includes two SOTA (DPI and Adapub) source code under other privacy settings.

### Environment

Tested Python version: 3.11.4 and 3.10.8

`numpy`, `math`, `random`, `os`, ` sys`,  and `matplotlib` libraries are required for our source code.

### Evaluation

==To verify all experimental results presented in the paper, please refer to the Evaluation section in ‘ndss_ae_appendix.pdf’. This section will provide the detailed steps to ensure a comprehensive validation of the experiments.==

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
