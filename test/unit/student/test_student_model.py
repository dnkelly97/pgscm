import pytest
from student.models import Student

@pytest.mark.django_db
def test_student_create():
   test_student = Student(
       email="tester@uiowa.edu",
       first_name="First",
       last_name="Last",
       school_year = Student.YearInSchool.SENIOR,
       research_interests=["testing","more testing"],
       degree = "testing degree",
       university = "university of testing",
       gpa = 4.0,
       ethnicity=Student.Ethnicity.MULTI,
       gender=Student.Gender.OTHER,
       country="US",
       us_citizenship=True,
       first_generation=False,
       military=False
   )

   assert test_student.email == "tester@uiowa.edu"
   assert test_student.first_name == "First"
   assert test_student.last_name == "Last"
   assert test_student.school_year.value=="SR"
   assert test_student.school_year.label=="Senior"
   assert test_student.research_interests == ["testing","more testing"]
   assert test_student.degree == "testing degree"
   assert test_student.university == "university of testing"
   assert test_student.gpa == 4.0
   assert test_student.ethnicity.value == "M"
   assert test_student.ethnicity.label == "Multiracial"
   assert test_student.gender.value == "O"
   assert test_student.gender.label == "Other"
   assert test_student.country.name == "United States of America"
   assert test_student.us_citizenship==True
   assert test_student.first_generation==False
   assert test_student.military==False

