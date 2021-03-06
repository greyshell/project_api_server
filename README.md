# Powerful Python Project

### Develop a API Server
1. The Game Plan => done
   - install and set up pycharm and pyenv
2. Development Set-up => done
   - create the foundation, virtual env using pyenv, git branch
3. The First Endpoint => done
4. Creating & Fetching A Task => done
5. Batches of Tasks => done
6. Application Structure: Refactoring & Organizing => done
7. Using the Database => done
8. Fleshing out the API => done
9. Writing A Decorator: A Tiny Huge Detail => done
10. The Final Executable => done

### Test the API using curl

```
# get all the tasks
curl http://127.0.0.1:5000/tasks/    

# create a task
curl -X PUT -d '{"summary": "Get almond milk", "description": "vanilla flavor"}' http://127.0.0.1/tasks/1/    

# get the task details based on the task id
curl -I http://127.0.0.1:5000/tasks/1          

# modify a task based on the task id
curl -X PUT -d '{"summary": "Get almond milk", "description": "vanilla flavor"}' http://127.0.0.1:5000/tasks/1/

# delete a task based on the task id
curl -X DELETE http://127.0.0.1:5000/tasks/1/   

# check the status code of a deleted task
curl -I http://127.0.0.1:5000/tasks/1/
```