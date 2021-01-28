from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/')
def base():
    return render_template('index.html')

# Test client
# curl -i -H "Content-Type: text/plain" -X  POST http://localhost:5000/command-obj --data-raw "{'type': '12','codes': ['410b847', '410e21d', '410b847']}"
@app.route('/command-obj', methods=['POST'])
def commandObj():
    data = request.get_json()
    print("json object %s " % data )
    print("Procesing ...")
    return 'ok'