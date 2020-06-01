from app import db


class ProjectInfo(db.Model):
    __tablename__ = 'projectInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, index=True)
    attachment_id = db.Column(db.Text, index=True)


class UserNotificationSubscriptions(db.Model):
    __tablename__ = 'userNotificationSubscriptions'
    id = db.Column(db.Integer, primary_key=True)
    vk_uid = db.Column(db.Integer, index=True, nullable=False)
    email = db.Column(db.Text, index=True)

