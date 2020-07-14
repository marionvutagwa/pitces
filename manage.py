from app import create_app,db
from flask_script import Manager,Server
from app.models import User,Role,Pitch,Comment,UpVote,DownVote
from  flask_migrate import Migrate, MigrateCommand


# Creating app instance
app = create_app('production')

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User , Role = Role,Pitch = pitches,Comment=comments,UpVote= upvote,DownVote=downvote)
    
if __name__ == '__main__':
    manager.run()