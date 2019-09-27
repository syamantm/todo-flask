from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(500), index=False, unique=False)
    done = db.Column(db.Boolean, index=False, unique=False, default=False)

    def __repr__(self):
        return '<Task {}>'.format(self.title)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done
        }