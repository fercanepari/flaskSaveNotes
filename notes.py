from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

import json


app = Flask("NotesAPI")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('uploadDate', type=int, required=False)


with open('notes.json', 'r') as f:
    notes = json.load(f)

def write_changes_to_file():
    global notes
    notes = {k: v for k, v in sorted(notes.items(), key=lambda note: note[1]['uploadDate'])}
    with open('notes.json', 'w') as f:
        json.dump(notes, f)

class Note(Resource):
    
    def get(self, note_id): 
        if note_id == "all":
            return notes
        if note_id not in notes:
            abort(404, message=f"Nota {note_id} no existe")
        return notes[note_id]
    
    def put(self, note_id):
        args = parser.parse_args()
        new_note = {'title': args['title'],
                    'uploadDate': args['uploadDate']}
        notes[note_id] = new_note
        write_changes_to_file()
        return {note_id: notes[note_id]}, 201
    
    def delete(self, note_id):
        if note_id not in notes:
            abort(404, message=f"Nota {note_id} no existe")
        del notes[note_id] 
        write_changes_to_file()
        return "", 204

class NoteSchedule(Resource):
    
    def get(self):
        return notes
    
    def post(self):
        args = parser.parse_args()
        new_note = {'title': args['title'],
                    'uploadDate': args['uploadDate']}
        note_id = max(int(v.lstrip('note')) for v in notes.keys()) + 1
        note_id = f"note{note_id}"
        notes[note_id] = new_note
        write_changes_to_file()
        return notes[note_id], 201    
    
#api.add_resource(Note, '/')
api.add_resource(Note, '/notes/<note_id>')
api.add_resource(NoteSchedule, '/notes')


if __name__ == '__main__':
    app.run()
