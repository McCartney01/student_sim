from src.student_profile import StudentProfile
from src.sbs import behavior_prediction, solution_simulation
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

student_list_2 = [
    "java_u344869639",
    "java_u520480375",
    "java_u861445290",
    "java_u866594486",
    "java_u897853321",
]

student_list_3 = [
    "c++_u337018543",
    "c++_u500376440",
    "c++_u505122009",
    "c++_u644002104",
    "c++_u851044959",
]


def simulation(student, test_index):
    acc, score1, description = behavior_prediction(student, test_index)
    score2, answer = solution_simulation(student, test_index, description)

    return acc, score1, score2, student


def main(student_list, model):
    student_mapping = {}
    for student_id in student_list:
        this_student = StudentProfile(student_id=student_id, model=model)
        this_student.prototype_construction()
        student_mapping[student_id] = this_student
    
    futures, results = [], []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for student_id in student_list:
            student = student_mapping[student_id]
            for i in range(len(student.test)):
                futures.append(executor.submit(lambda p: simulation(*p), [student, i]))

        for job in as_completed(futures):
            acc, score1, score2, student = job.result(timeout=None)
            results.append([acc, score1, score2])

    results = np.array(results)
    print("Acc: ", results[:, 0].mean())
    print("Score1: ", results[:, 1].mean())
    print("Score2: ", results[:, 2].mean())

if __name__ == "__main__":
    for model in ["llama", "claude", "3.5", "4o"]:
        main(student_list=student_list_2, model=model)
    for model in ["llama", "claude", "3.5", "4o"]:
        main(student_list=student_list_3, model=model)