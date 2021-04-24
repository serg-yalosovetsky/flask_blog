from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import forms
import logging
import service
NO_TITLE = 'Title is required'
HT = '.html'
user_id = -10



app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
    
app.config['SECRET_KEY'] = 'my super hyper secret key'



def get_post(post_id):
    post = service.select_one('posts', post_id)
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    posts = service.select_all('posts')
    return render_template('index.html', posts=posts)

@app.route('/')
def index_login(user):
    posts = service.select_all('posts')
    
    return render_template('index.html', posts=posts, user=user)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        
        # flash(f'login for user {form.username.data}, remember me {form.remember_me.data}')

        name= form.username.data
        passw = form.password.data
        email = form.email.data
        if not email or not passw:
            flash(NO_TITLE)
        else:
            
            user_name = service.check_pass(email, passw)
            if user_name is None:
                user_name = ''
                flash('bad credentionals')

                return render_template(url_for('login') + HT,form=form)
            # for u in user_name:
            user_name = service.get_user(email)
            flash(f'hi {user_name["name"]} #{user_name["id"]}!')
            user_id = user_name['id']
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        form = forms.LoginForm()
        # flash(f'login for user {form.username.data}, remember me {form.remember_me.data}')
        app.logger.error(request)
        
        # name = request.form['fullname']
        name= form.username.data
        passw = form.password.data
        email = form.email.data
        # name= passw= email =''
        if not email or not passw or not name:
            flash(NO_TITLE)
        else:
            service.create_user(name, passw, email)
            user_name = service.get_user(email)
            flash(f'user {user_name["name"]} #{user_name["id"]} created')
            user_id = user_name['id']
            return redirect(url_for('index'))
        
    return render_template('login.html', form=form)



@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create(user_id=user_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash(NO_TITLE)
        else:
            service.create_post(title, content, user_id)
            
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title:
            flash(NO_TITLE)
        else:
            service.update_posts(title, content, id)
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):

    post = get_post(id)
    service.delete_post(id)
    flash(f'{post["title"]} was successfuly deleted!')
    return redirect(url_for('index'))