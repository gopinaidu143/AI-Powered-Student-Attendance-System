import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



cred = credentials.Certificate("faceattendancerealtime-50d48-firebase-adminsdk-dqvrs-34b6851fed.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-50d48-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")

data =  {
    "312654":
        {
            "name": "Hassan",
            "Major": "AI",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year" : 4,
            "last_attendance_time": "2024-03-29 00:54:32"
        },
"852741":
        {
            "name": "Emaly",
            "Major": "AI",
            "starting_year": 2018,
            "total_attendance": 6,
            "standing": "B",
            "year" : 6,
            "last_attendance_time": "2024-03-29 00:54:32"
        },
"963852":
        {
            "name": "ELon Musk",
            "Major": "Electronics",
            "starting_year": 2011,
            "total_attendance": 14,
            "standing": "B",
            "year" : 3,
            "last_attendance_time": "2024-03-29 00:54:32"
        },

"42602":
        {
            "name": " Gopi Naidu",
            "Major": "AI",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year" : 4,
            "last_attendance_time": "2024-03-29 00:54:32"
        },
"42663":
        {
            "name": " Jayendra",
            "Major": "AI",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year" : 4,
            "last_attendance_time": "2024-03-29 00:54:32"
        }

}

for key,value in data.items():
    ref.child(key).set(value)