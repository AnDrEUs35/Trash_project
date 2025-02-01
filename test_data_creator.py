import json
from random import randint

path = '/workspaces/Trash_project/test_data.json'
data = {
    "satellites":[
    ],
    
    "trashes":[
    ],
    
    "user_data":[
    {"time": 30,
    "trashes_on": True,
    "satellites_on": False
    }
    ]
        
}


for i in range(randint(1, 100)):
    data['satellites'].append({"vel": [randint(1, 10), randint(1, 10), randint(1, 10)], "coords": [randint(1, 500), randint(1, 500), randint(1, 500)]})
    data['trashes'].append({"vel": [randint(1, 10), randint(1, 10), randint(1, 10)], "coords": [randint(1, 500), randint(1, 500), randint(1, 500)]})

with open(path, 'w') as file:
    json.dump(data, file, indent=2)