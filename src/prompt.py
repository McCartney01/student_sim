NEW_PROMPTS = {}

NEW_PROMPTS["get_library"] = """Question:
{question}


Description:
{desc}


Student Program:
{program}


Error Description:
{error_desc}"""


NEW_PROMPTS["summarize_kc"] = """-Goal-
You are tasked with evaluating a student’s understanding of a specific concept based on several descriptions derived from their past problem-solving records. Each description corresponds to a specific question and is categorized as either:
	•	Good: Demonstrates correct understanding or application of the concept.
	•	Bad: Indicates misunderstanding or errors in applying the concept.

Each description includes detailed text explaining the student’s performance on that question. Your goal is to provide an overall evaluation based on both Good and Bad descriptions.

-Steps-:
Based on the input descriptions, provide:
1.	A Score (1-5):
	•	1: No understanding; critical misconceptions.
	•	2: Poor understanding; partial grasp but significant issues.
	•	3: Moderate understanding; grasp of core concepts but notable errors.
	•	4: Good understanding; minor mistakes.
	•	5: Excellent understanding; strong grasp and correct application.
The score should consider the frequency and severity of Good and Bad descriptions, as well as the details they convey.
2.	A Written Evaluation:
Provide a single, comprehensive paragraph summarizing the student’s overall performance. This should include their strengths and weaknesses in a balanced manner, without separating them explicitly or including suggestions.

-Output Format-
Score: (you score)

Evaluation: (your evaluation)

-Real Data-
Knowledge Point: {kc_name}

There are {good_cnt} positive descriptions, {bad_cnt} negative descriptions.
Descriptions:
{desc}
"""

NEW_PROMPTS["retrieve"] = """Question:
{question}


Description:
{desc}"""

NEW_PROMPTS["generate_error_desc"] = """-Goal-
Background:
You are tasked with predicting whether a student will make mistakes on a new {subject} programming problem. The input includes:
1.	Student’s Understanding: A summary of the student’s grasp of relevant concepts, including their overall strengths and weaknesses.
2.	Historical Case Study: A {subject} problem the student has previously attempted, which serves as a reference. This case study includes:
	•	Problem statement.
	•	Concepts the problem tests.
	•	Student’s code.
	•	Error analysis of the student’s submission, detailing the mistakes and their nature.
3.	New Problem: A {subject} problem that the student has not yet attempted.

The historical case study provides additional context about the student’s problem-solving patterns, common mistakes, and conceptual gaps, which must be considered along with their general understanding.

-Steps-
1.	Error Prediction: Analyze the student’s understanding and historical case study to predict whether the student is likely to make mistakes on the new problem.
	•	Compare the concepts tested in the new problem with the student’s strengths, weaknesses, and past errors.
	•	Use the historical case study to identify recurring patterns or tendencies in the student’s approach to problem-solving.
Simply output 'Yes' or 'No'
2.	Error Description: Provide an error description similar to the style of the historical case.
	•	Use the style of error descriptions from the historical case study as a reference.
	•	Ensure that the error descriptions are related to the new problem.

-Output Format-
Error Prediction: (Yes/No)

Error Description: (Your detailed analysis)

-Real Data-
Student's Understanding:
{summarize_kc} 

Historical Case Study:
{case}

New Problem:
{problem}:

Output:
"""

NEW_PROMPTS["eval_error_desc"] = """You are given a {subject} programming question, a student's answer code, and an analysis of errors found in the code. Then, I will provide a new error analysis. Your task is to evaluate the new analysis and determine how accurate and reasonable it is and how closely it matches the original error analysis. Please assign a score from 1 to 5, where:

•	1: The new analysis is completely unreasonable and unrelated to the actual error.
•	2: The new analysis attempts to describe the error but fails significantly or introduces unrelated issues.
•	3: The new analysis somewhat aligns with the actual error, but there are noticeable inaccuracies or omissions.
•	4: The new analysis is mostly accurate and aligns well with the actual error, with only minor differences or slight deviations.
•	5: The new analysis is fully accurate, natural, and matches the actual error explanation closely.

Additionally, please provide a brief explanation within 3 sentences justifying your score, focusing on the accuracy, relevance, and clarity of the new analysis in comparison to the original.

Format your output as (Score | Explanation), such as (5 | The new analysis is fully accurate). Do not output any other words.

-Real Data-
Question:
{question}

Student's answer code:
{gt_code}

Error Analysis:
{error_desc}

New Error Analysis:
{new_error_desc}

Output:
"""


NEW_PROMPTS['generate_initial_code'] = """Given a {subject} programming problem, please write a piece of code to solve it in the style of a {subject} beginner. Do not include comments in the code. Use the following example as a reference. Directly output your code.

-Example-
Question:
{eg_question}

Code:
{eg_code}

-Real Data-
Question:
{question}

Code:
"""

NEW_PROMPTS['evaluate_1'] = """Given a {subject} programming question, a solution code, along with an error description. For each error in the error description, you need to analyze whether the solution code naturally replicates the error.

Question:
{question}

Code:
{code}

Error Description:
{error_desc}
"""

NEW_PROMPTS['evaluate_2'] = """Based on your analysis, rate a score about whether the code aligns with the error description. The score is ranged from 0 to 1, higher score indicates that the code better and more naturally replicates the errors mentioned in the error description. Then give a explanation within 3 sentences.

Output format: (Score | Explanation). For example, (0.1 | The code does not replicate any errors mentioned in the description), or (0.9 | The code successfully reproduces all the errors in the description).
"""

NEW_PROMPTS['refine'] = """Imagine there is a code generator designed to simulate a specific student solving {subject} programming problems. The code generator has access to the student’s past {subject} code as a reference for their coding style. Additionally, it only knows the descriptions of errors present in the student’s current solution but does not have access to the student’s actual solution code. Based on this information, the code generator pretends to be the student and writes code to complete the problem.

However, the quality of the code generated by the code generator may not be enough. The code might not accurately reflect and replicate the errors described in the error descriptions, or it might not align with the coding style observed in the student’s past code. You will be given an evaluation about the quality of the generated code.

Your task is to revise the generated code based on the provided feedback, ensuring it better meets the requirements. Specifically, the revised code should more accurately replicate the errors described in the error feedback and align more closely with the coding style observed in the student’s past work.

Directly output your revised code without any words or explanations!!

-Real Data-
Student's Past Code:
{eg_code}

New Programming Problem:
{question}

Error Descriptions:
{error_desc}

Code From Generator:
{code}

Evaluation:
{evaluation}

Your Revised Code:
"""

NEW_PROMPTS["eval_code"] = """You are given a {subject} programming question, a student's answer code, and an analysis of errors found in the code. Then, I will provide a new code. Your task is to evaluate the new code and determine how well it reproduces the described errors. Please assign a score from 1 to 5, where:

•	1: The new code does not reproduce the described errors at all.
•	2: The new code attempts to reproduce some the described errors but fails significantly.
•	3: The new code somewhat reproduces some described errors but with significant differences.
•	4: The new code reproduces most the described errors well, with a little differences.
•	5: The new code fully and naturally reproduces the described errors.

Additionally, please provide a brief explanation within 3 sentences justifying your score, focusing on how closely the new code matches the nature of the described error.

Format your output as (Score | Explanation), such as (5 | The new code successfully reproduces the described errors). Do not output any other words.

-Real Data-
Question:
{question}

Student's answer code:
{gt_code}

Error Analysis:
{error_desc}

New Code:
{code}

Output:
"""