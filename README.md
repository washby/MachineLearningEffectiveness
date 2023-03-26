# MachineLearningEffectiveness
Python scripts used in the dissertation for measuring the effectiveness of machine learning algorithms on predicting collegiate-level course outcomes.

## Contents
### CanvasSystem

- AbstractCanvasObject - The abstract class other items use for inheritance to reduce code repetition
- CanvasConnection - The class used to read a university's config.json file and establish a connection and pull the data.
- Course - A course object to hold data for each course to be able to transition easily between json, csv, and sql code.
- Enrollment - An enrollment object to hold data for each enrollment in a course  to be able to transition easily between json, csv, and sql code.
- Term - A term object to hold data for each term  to be able to transition easily between json, csv, and sql code.

### GatherDataFromUniversity
Handles the workflow of pulling the desired terms based on date range, then the courses in each of those terms. Then from the courses, the needed enrollments are pulled to know the students in each course. Then the data for each enrollment is pulled and put into CSV files to be checked by a system admin before pushing to the database.
