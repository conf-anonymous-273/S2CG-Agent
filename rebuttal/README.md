# Common Issues

## 1. Reviewer A/B/C: Limited benckmarks

We applied S²CG-Agent on 1345 samples of SecCodePLT, which included both the possibility of models generating unsafe code and security test cases. Due to time constraints, we only evaluated the performance of S²CG-Agent. S²CG-Agent improved secure coding rate from 57% to 72.19%, improved SA-Pass@1 from 71.15% to 79.63%.

Due to time constraints, we only evaluated the performance of S²CG-Agent, of which the secure coding rate was calculated using benchmark evaluation.
Results on SecCodePLT: S²CG-Agent vs. GPT-4o.

```
📊 Outputs -> rebuttal/NewBenchmarks/results.json
```

<img width="425" height="97" alt="image" src="https://github.com/user-attachments/assets/dcf941e0-208a-44d2-92c5-1e2331c27d2e" />

## 2. Reviewer A/B: Failure cases

S²CG-Agent failures can be attributed to scheduler prediction failure and LLM's insufficient ability to repair failures. We conducted a specific analysis on the best performing GPT-4o results: (1) Scheduler missed reports, function missed reports 0/164, static issues missed reports 1/285, Fuzz issues missed reports 6/285. (2) LLM repair failed, unit test repair failed 4/164, static problem repair failed 3/285, and fuzz problem repair failed 38/285.

```
📊 Outputs -> rebuttal/error_analysis
```

**Scheduler missed report:** CWE-295, CWE-339, CWE-477, CWE-601, CWE-611

**LLM repair failed:** CWE-020, CWE-022, CWE-078, CWE-079, CWE-080, CWE-090, CWE-094, CWE-113, CWE-116, CWE-117, CWE-209, CWE-215, CWE-306, CWE-321, CWE-326, CWE-400, CWE-434, CWE-502, CWE-522, CWE-601, CWE-611, CWE-641, CWE-643, CWE-730, CWE-918.

***LLM repair failed case analysis (part):***

| ID                  | Cause analysis                                               |
| ------------------- | ------------------------------------------------------------ |
| HumanEval/87        | Boundary conditions are not fully processed and all input scenarios are not covered |
| HumanEval/132       | Nested depth calculation logic flaw, insufficient handling of the situation of  “]” |
| CWE-020_codeql_4.py | URL verification regular or whitelist strategies are not strict |
| CWE-078_author_1.py | Lose command verification logic, and the safe subcommand segmentation is not used correctly |
| CWE-918_codeql_1.py | Incomplete implementation of subdomain whitelist function    |
| CWE-020_codeql_1.py | Path concatenation or escape logic does not trigger any safe branches |

***Scheduler missed report case analysis (part):***

| ID                  | Cause analysis                                               |
| ------------------- | ------------------------------------------------------------ |
| CWE-601_codeql_1.py | No verification was performed on the redirect URL parameters |
| CWE-295_author_1.py | SSL context configuration interface mismatch                 |
| CWE-295_author_2.py | The OpenSSL Context creation process did not trigger an exception path |
| CWE-611_sonar_2.py  | XML parsing does not combine input file                      |

## 3. Reviewer A/C: Statistical testing

We conducted statistical testings (p-value and effect size), and the results showed that there were significant differences between S²CG-Agent and baselines in almost all metrics (p<0.05).

Statistical testings on UT-Pass@1:

<img width="607" height="534" alt="image" src="https://github.com/user-attachments/assets/24797fc3-3731-41fd-9a6d-0e57d0f2fb3a" />

Statistical testings on SA-Pass@1:

<img width="610" height="531" alt="image" src="https://github.com/user-attachments/assets/961153a2-1000-4bb5-91be-90dcaac61e46" />

Statistical testings on FT-Pass@1:

<img width="609" height="530" alt="image" src="https://github.com/user-attachments/assets/be7c9925-e255-4d27-980c-eb20ce4510b7" />

```
⚙️ Codes -> rebuttal/statistical testings/p_value_cohen_d.py
```

# Reviewer-A

## Question-1: VS. hand-coded policies or LLM-based agent

We did experiments on safe priority and function priority and LLM-Agent settings. Experimental results show that when safety is given priority, the SA-Pass@1 increases (98.59%) but the UT-Pass@1 decreases (92.68%); when function is given priority, the UT-Pass@1 increases (95.12%), but the SA-Pass@1 decreases (94.74). While LLM-Agent shows a compromise level in performance on all three metrics, S²CG-Agent outperforms hand-coded-policies and LLM-Agent based methods on all metrics.

```
⚙️ Codes -> rebuttal/hand-coded-policies
```

Result: S²CG-Agent vs. hand-coded-policies & LLM-Agent 

SafeFirst performs static analysis, fuzzing, and unit testing in a fixed order. FuncFirst performs unit testing, static analysis, and fuzzing in a fixed order.

<img width="864" height="176" alt="image" src="https://github.com/user-attachments/assets/f57176ba-525a-4cdd-b923-e6666585fd7f" />

## Question-2: Ambiguous checker outputs

The output of the checker will be handed over to the "Result Parser" and will not produce ambiguous output. However, we made limitations in prompt, that is, static analysis / fuzzing related modifications can be made without destroying functionality.

## Question-3: Missed vulnerabilities.

Please see common issue-2.

## Issue-1: Statistical testing 

Please see common issue-3.

## Issue-2: Limited benchmarks

Please see common issue-1.

# Reviewer-B

## Question-1: Scheduler fail

Please see common issue-2.

## Question-2: Scheduler evolve

The scheduler does not change after training. The scheduler was trained on 2970 samples generated in other benchmarks and already has good predictive capabilities. For fairness in the evaluation, real-time prediction data was not applied to update the scheduler.

In theory, the scheduler can continuously learn feedback through real-time prediction data, especially data with erroneous predictions.

To further prove the effectiveness without scheduler evolution, we extended the S²CG-Agent to a new benchmark, the results shows that the scheduler has good generalization ability, please see common issues.

## Issue-1 Limited benchmarks

Please see common issue-1.

## Issue-2 Inadequate related-works

We commit to adding the related works.

# Reviewer C

## Issue-1: No obvious improvement.
Please see common issue-3.

## Issue-2: Results unreliable:

We repeated the S²CG-Agent(GPT-4o) three times, and the results of repeated experiments were stable. In addition, we aggregated the results of the repeated experiments and performed statistical testings. The results showed that there was no significant difference between the paper data and the repeated experiments results, showing the robustness of the results.

Result: S²CG-Agent(GPT-4o) repeats 3 times.
<img width="691" height="157" alt="image" src="https://github.com/user-attachments/assets/c31e51f5-dd48-409e-a2e3-abafb57aa0de" />

Result: Statistical testings on repeated results.

<img width="662" height="156" alt="image" src="https://github.com/user-attachments/assets/73a963ed-244f-4717-8371-d44382f66f09" />

```
📊 Outputs -> rebuttal/repeat
```

## Issue-3: Unit test & Unfair Setting:

S²CG-Agent is available for unit testing scenarios and is not limited to the IDE. The unit tests used to train the scheduler, give feedback, and ultimately evaluate are separate.

The original LLM that does not provide feedback is the baseline we set. We also set LLM-Agent for baselines, therefore, there is no unfair problem.

## Issue-4: Time-cost:

LLM enhanced code generation methods generally take a long time. For example, ASE'24 Best Paper PairCoder requires an average of 17.57 API calls for a complex problem, while S²CG-Agent only needs an average of 3.9 times.

S²CG-Agent is affected by api call frequency and tool runtime in the working environment, while the original LLM only requires 1 call and is not affected.

## Issue-5: Tools:

CodeQL and Bandit are cross-complementary, CodeQL is good at logic vulnerabilities, and Bandit is sensitive to common Python vulnerabilities. They don't trigger unnecessary false positives in the experiment, and the feedback generated is beneficial to the robustness of the final generated code.

Bear is a static analysis tool as well, and Dai et al. did comparative experiments on them, proving that the overall detection coverage of the three is similar.

```
Dai, S., Xu, J., & Tao, G. (2025). A Comprehensive Study of LLM Secure Code Generation. *ArXiv, abs/2503.15554*.
```

## Issue-6: Benchmarks:

Please see common issue-1.
