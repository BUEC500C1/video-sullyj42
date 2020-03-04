# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# if __name__ == "__main__":
#     app.run()
from twittervideo import twitter_queue_video
from flask import Flask, render_template, request, redirect

twitterhandles = []  # Empty list of twitter handles to add
# create the application object
app = Flask(__name__)

@app.route('/')
def hello_world():
    author = "Jeremiah Sullivan"
    name = "Twitter Video"
    return render_template('index.html', author=author, name=name)


@app.route('/signup', methods = ['POST'])
def signup():
    handle = request.form['twitterhandle']
    print("A new twitter handle was added: " + handle)
    twitterhandles.append(handle)
    outvid = twitter_queue_video.makequeue(username=handle)  # Make this into a queue
    print(f'Recieved processed video at: {outvid}')
    return redirect('/queueinfo')

@app.route('/queueinfo')
def queueinfo():
    return render_template('twitterhandles.html', twitterhandles=twitterhandles)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
