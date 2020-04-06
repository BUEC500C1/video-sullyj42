# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# if __name__ == "__main__":
#     app.run()
from twittervideo import twitter_queue_video
from flask import Flask, render_template, request, redirect, send_file

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
    numpages = int(request.form['numpages'])
    numtweets = int(request.form['numtweets'])
    photos = bool(request.form.get('photos'))
    print(f'A new twitter handle was added: { handle}, pages: {numpages}, ')
    twitterhandles.append(handle)
    try:
        outvid = twitter_queue_video.makequeue(username=handle,
                                               pages=numpages,
                                               workphotos=photos,
                                               tweetcount=numtweets)  # Make this into a queue
    except Exception as e:
        print(f'Could not process twitter feed')
        print(f'Message: {e}')
        return render_template('index.html', author="Try again", name='Invalid Parameters')
    else:
        print(f'Recieved processed video at: {outvid}')
        #return redirect('/queueinfo')  # Write this later
        return send_file(outvid, as_attachment=True)


@app.route('/queueinfo')
def queueinfo():
    return render_template('twitterhandles.html', twitterhandles=twitterhandles)

# start the server with the 'run()' method
if __name__ == '__main__':
    print('Starting Flask App')
    app.run(host='0.0.0.0')

