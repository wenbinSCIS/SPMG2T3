# Documentation

## Development: Running the UI with VS Code
- Open command palette and type "open live server" and press enter (need to install [live server extension](vscode:extension/ritwickdey.LiveServer))

## Development: Running the microservices
- go to "microservice/ezrunall.py"
- edit the file's "MICROSERVICE_PATH" to your local drive's path to the "microservice" folder
```py
MICROSERVICE_PATH="C:\\Documents\\SPMG2T3\\microservice\\"
```
- in the terminal, run "python microservice/ezrunall.py" to run all simple microservices
- and in another terminal, run "python microservice/add_role.py" to run the complex microservice
```bash
# may either use 'python' or 'py' depending on how your python env is set
python microservice/ezrunall.py
python microservice/add_role.py
```

## Microservice Routes

- [add_role](./microservice/add_role.py)
  - complex microservice, uses the 'roles' and 'skills' microservices
  - adds new role to the DB, as well as attaching the skills required by the role (in another table)
  - POST -- http://127.0.0.1:5020/add_role
- [roles](./microservice/roles.py)
  - used to add, delete, update and retrieve role data from the 'roles' table
  - GET -- http://127.0.0.1:5000/roles/getAll
  - GET -- http://127.0.0.1:5000/roles/getById
  - GET -- http://127.0.0.1:5000/roles/getUnfulfilled
  - POST -- http://127.0.0.1:5000/roles/create
  - POST -- http://127.0.0.1:5000/roles/deletebyID
  - POST -- http://127.0.0.1:5000/roles/updateNamebyID
  - POST -- http://127.0.0.1:5000/roles/updateDescriptionbyID
  - POST -- http://127.0.0.1:5000/roles/updateRoleStatus
- [skills](./microservice/skills.py)
  - used to add, delete, update and retrieve skills data from the 'skills' table
  - GET  -- http://127.0.0.1:5002/getSkillbyId
  - GET  -- http://127.0.0.1:5002/getAllSkill
  - POST -- http://127.0.0.1:5002/addSkill
  - POST -- http://127.0.0.1:5002/updateskillnamebyID
  - POST -- http://127.0.0.1:5002/deleteskillsbyID
- [skills required by role (SRBR)](./microservice/skills_required_by_role.py)
  - used to update (by adding), delete and retrieve skills data (required by skills) from the 'SRBR' table
  - GET -- http://127.0.0.1:5001/getSRBRbyRoleID
  - GET -- http://127.0.0.1:5001/getByRIDSID
  - POST -- http://127.0.0.1:5001/addskillrole
  - POST -- http://127.0.0.1:5001/deletebyskillrole
- [courses](./microservice/courses.py)
  - used to retrieve course data from the 'course' table
  - GET -- http://127.0.0.1:5004/getCoursebyId
  - GET -- http://127.0.0.1:5004/courses/getAll
- [skills acquired by course (SABC)](./microservice/skills_acquired_by_course.py)
  - used to update (by adding), delete and retrieve skills data (acquired by courses) from the 'SABC' table
  - GET -- http://127.0.0.1:5003/getSABCbySkillID
  - GET -- http://127.0.0.1:5003/getSABCbyCourseID
  - POST -- http://127.0.0.1:5003/addskillcourse
  - POST -- http://127.0.0.1:5003/deletebyskillcourse
- [learning journey](./microservice/learningjourney.py)
  - used to add, delete, update and retrieve learning journey data from the 'learningjourney' table
  - GET -- http://127.0.0.1:5010/LJ/getLJByUserId
  - GET -- http://127.0.0.1:5010/LJ/updateRoleIDByLJID
  - GET -- http://127.0.0.1:5010/LJ/updateLJNameByLJID
  - GET -- http://127.0.0.1:5010/LJ/insertgetLJID
  - GET -- http://127.0.0.1:5010/LJ/getLJByLJID
  - GET -- http://127.0.0.1:5010/LJ/deleteLJbyLJID
- [learning journey courses](./microservice/learningjourneycourses.py)
  - used to add, delete, update and retrieve learning journey course data from the 'learningjourneycourses' table
  - GET -- http://127.0.0.1:5011/LJC/getLJCoursesById
  - GET -- http://127.0.0.1:5011/LJC/deleteLJCbyLJIDCID
  - GET -- http://127.0.0.1:5011/LJC/deleteAllLJCbyLJID
  - GET -- http://127.0.0.1:5011/LJC/addCourseIntoBasket
  - GET -- http://127.0.0.1:5011/LJC/checkIfCourseInLJ
