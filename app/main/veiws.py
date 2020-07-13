from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PitchForm,CommentForm
from flask_login import login_required,current_user
from .. import db,photos
from ..models import User,Pitch,Comment,UpVote,DownVote
import markdown2



# Views
@main.route('/')
def index():
    pitch = Pitch.query.filter_by().all()
    business = Pitch.query.filter_by(category='business').all()
    job = Pitch.query.filter_by(category='job').all()
    interview = Pitch.query.filter_by(category='interview').all()
    
    title = 'Welcome to to your one minute'
    return render_template('index.html',title = title,pitch=pitch,business = business, job = job, interview = interview)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

    return render_template('profile/update.html',form =form)   


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/pitch/new',methods = ['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        description = form.description.data
        new_pitch = Pitch(category= category,title =title, description= description, user= current_user)
        new_pitch.save_pitch()
        db.session.add(new_pitch)
        db.session.commit()
        return redirect(url_for('.index'))
        
    return render_template('new_pitch.html',pitchform = form)


# @main.route('/pitch/new/<int:id>')
# def single_pitch(id):
#     pitch = Pitch.query.get(id)
         

#     return render_template('pitches.html', pitch=pitch)  


@main.route('/comment/new/<int:pitch_id>',methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    # all_comments = Comment.query.filter_by(pitch_id= pitch_id).all()
    if form.validate_on_submit():
        description = form.description.data
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(description= description, pitch_id= pitch_id,user_id= current_user)
        # new_comment.save_comment()
        # db.session.add(new_comment)
        # db.session.commit()

        return redirect(url_for('main.comment', pitch_id = pitch_id))

    return render_template('comment.html',form = form,pitch= pitch)  


@main.route('/pitches/upvote/<int:pitch_id>',methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitches = Pitch.query.all()
    user = current_user
    upvotes = UpVote.query.filter_by(pitch_id= pitch_id,upvote= 1)
    
    return redirect(url_for('main.index'))


@main.route('/pitches/downvote/<int:pitch_id>',methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitches = Pitch.query.get(pitch_id)
    user = current_user
    downvotes = DownVote.query.filter_by(pitch_id= pitch_id, downvote= 1)
    
    return redirect(url_for('main.index'))