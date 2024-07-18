# Delay-allowed Differentially Private Data Stream Release

Tested Python version: 3.11.4 and 3.10.8

`numpy`, `math` , ``random`, `os`, ` sys`,  and `matplotlib` libraries are required.

==To verify all experimental results presented in the paper, please refer to the Evaluation section in ‘ndss_ae_appendix.pdf’. This section will provide the detailed steps to ensure a comprehensive validation of the experiments.==


### Evaluation

- Compare Delay-allowed Approaches with Baseline Methods:

To evaluate all the proposed method, set

```
est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time)
```

 Simply run:

```
python ./release/est_compall.py
```
The results and the graphs will be directly output to the screen.

- Evaluate Effectiveness of Data Sensitivity Truncation:

To use the sensitivity truncation mechanism, you can set the parameter `Flag=1`, `interval`  refers to the number of data batches between updates, `num_`  is specifically used by CompOrder as the length of each data batch.
```
est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time, flag = 1, interval_ = 5, num_ = 100)
```

Simply run:

```
python ./release/est_sensitivity.py
```

- Evaluate the Impact of the Delay Length:

Simply run:

```
python ./release/est_delaylength.py
```

- Evaluate the Impact of the Bucket Size:

Simply run:

```
python ./release/est_order.py
```

- Evaluate the Impact of the Threshold:

Simply run:

```
python ./release/est_group.py
```
