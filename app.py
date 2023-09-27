from flask import Flask, render_template, request, redirect
from mp import list, start
app = Flask(__name__)
UPLOAD_FOLDER = '/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

docs = []
@app.route('/', methods=("GET","POST"))
def main():
    if request.method == "POST":
        doc1 = request.files.get("doc1")
        doc2 = request.files.get("doc2")
        docs.append(doc1.read())
        docs.append(doc2.read())
    return render_template('main.html' , list=list)

@app.route('/plagcheck/', methods=['GET'])
def check():
    start(docs)
    docs.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)