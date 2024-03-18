For the task, we consider 3 inputs, as detailed below:

student_info.csv
id_student = numeric; unique identifier for each student in the course
gender = character; M = "male", F = "female"
highest_education = character; “Some Graduate”, “Some Higher Education”, “High School + Advanced Placement”, “High School”, “No Formal Quals” (Categories ordered from highest documented education level attained to lowest documented education level attained)
disability = character; Y = "yes", N = "no"
final_result = character; "Fail", "Pass"

quizzes_tests.csv
id_student = numeric; unique identifier for each student in the course
assignment_name = character; name of graded assignment (Quiz 1-7, Test 1-6, Final Exam)
due_date = numeric; date assignment was due (indexed as count in days from start of course, i.e., day 0)
weight = numeric; weight multiplied by score when generating final grade (weight * score / 100)
date_submitted = numeric; date student submitted assigned (indexed as count in days from start of course, i.e., day 0, NaN means students did not submit assignment)
score = numeric; score student earned on assignment (0 means students did not submit assignment)

learning_resources.csv
id_student = numeric; unique identifier for each student in the course
activity_type = character; overarching label for learning activity students can access (“course_homepage”, “course_page”, “forum”, ‘resource”, “wiki”)
activity_id = numeric; unique identifier for specific learning activity student accessed within overacting activity_type
date = numeric; date student accessed specific acitivity_id (indexed as count in days from start of course, i.e., day 0)
sum_click = numeric; count of clicks for activity_id on date

In a particular course, we aim to apply predictive models to predict those students who are likely to fail the course.
To feed these models, we generate continuous variables from the quizzes_tests and learning_resources files.

We use two predictive models, logistic regression and random forest, and then proceed to plot the distribution of probabilistic predictions.

The required libraries are:

- pandas 2.0.3
- matplotlib 3.3.0
- scikit-learn 1.0.2
