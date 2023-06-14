from flask import Flask, render_template, request, jsonify
import complexdemo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text_A = request.form['input_text']
    output = complexdemo.convert_java_to_python(input_text_A)
    print(output)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
