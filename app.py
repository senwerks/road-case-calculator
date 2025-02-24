from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    width = float(request.form['width'])
    height = float(request.form['height'])
    depth = float(request.form['depth'])

    angle_joiner_extrusion = int((width + height + depth) * 4)
    hybrid_joiner_extrusion = int((width + depth) * 2)

    output = {
        'angle_joiner_extrusion': angle_joiner_extrusion,
        'hybrid_joiner_extrusion': hybrid_joiner_extrusion,
        'width': int(width),
        'height': int(height),
        'depth': int(depth)
    }

    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51337, debug=True, threaded=True)
