from sqlalchemy import Column, bindparam,create_engine,Integer,String, literal_column, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#create Base class 
base_class=declarative_base()

#Establish connection
#replace with your user_name,password,host,port and data base name
engine=create_engine("mysql+pymysql://user_name:password@host:port/db_name")

#Model class
#the model class should have one primary key attribute
#other wise it will give an error
class Student(base_class):
    __tablename__="student"
    student_id=Column(Integer,primary_key=True)
    student_name=Column(String(50))
    gender=Column(String(10))
    phone_number=Column(Integer)
    branch=Column(String(10))

#create_all method will create a table in database named with student 
base_class.metadata.create_all(engine)

#creating session
Session=sessionmaker(bind=engine)
session=Session()

#creating Instance of Student class

sudnt1=Student(student_name="Alice",gender="Male",phone_number=123456789,branch="ECE")
sudnt2=Student(student_name="Kohli",gender="Male",phone_number=123456789,branch="CSE")
sudnt3=Student(student_name="Bob",gender="Male",phone_number=123456789,branch="CSE")
sudnt4=Student(student_name="Dhoni",gender="Male",phone_number=123456789,branch="ECE")

#adding Instance to session(adding data to table)

session.add(sudnt1)
session.add(sudnt2)
session.add(sudnt3)
session.add(sudnt4)

#committing changes

session.commit()



# creating branch_param with value equal to CSE
branch_param = bindparam("branch_param", value="CSE")

# creating the query to select the student details
# whose branch column matches with the brach_param value
query = session.query(Student).filter(branch_param == Student.branch)

# executing the query
result = query.all()

print("Bind Param Output")
print("____________________")
for row in result:
    # print(row) it print refference of row object
    print(row.student_id, row.student_name, row.phone_number, row.branch)
    print(row.student_id, row.student_name, row.phone_number, row.branch)



#creating the query to select the student details 
# whose branch is ECE 
query=session.query(Student).filter(literal_column("branch")=="ECE")

#executing the query
result=query.all()

print("literal_column output")
print("____________________")

for row in result:
    #print(row) it print refference of object
    print(row.student_id,row.student_name,row.phone_number,row.branch)

#closing the connection
session.close()



# creating the query to select the student details
# whose branch is ECE
query = session.query(Student).filter(getattr(Student, "branch") == "ECE")

# executing the query
result = query.all()

print("getattr output")
print("____________________")

for row in result:
    # print(row) it print refference of object
    print(row.student_id, row.student_name, row.phone_number, row.branch)

session.close()



#updating using bindparam() and literal column
#bind param 
phone_param=bindparam("phone_param",987654321)


updateQuery=update(Student).\
      where(literal_column("student_id")% 2 == 0).\
      values(phone_number=phone_param)

session.execute(updateQuery)

#commit is mendatory without this method data wont be updated
session.commit()


print("student data")
res=session.query(Student)
for s in res:
    print(s.student_id,s.student_name,s.phone_number)




#closing connection
session.close()