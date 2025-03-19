import math
from flask import Flask, render_template, request

app = Flask(__name__)

def pack_cuts(required_cuts, piece_length=1500):
    """
    Pack cuts into pieces of fixed length (default 1500mm) using a greedy algorithm.
    Each cut is a tuple (label, length).
    Returns a list of bins where each bin is a dict with keys:
      - 'remaining': remaining mm in the piece
      - 'cuts': list of cuts (tuples) assigned to that piece
    """
    bins = []
    # Sort cuts descending by length for a better packing order
    for cut in sorted(required_cuts, key=lambda x: x[1], reverse=True):
        placed = False
        for b in bins:
            if b['remaining'] >= cut[1]:
                b['cuts'].append(cut)
                b['remaining'] -= cut[1]
                placed = True
                break
        if not placed:
            # Start a new bin/piece
            new_bin = {'remaining': piece_length - cut[1], 'cuts': [cut]}
            bins.append(new_bin)
    return bins

@app.route('/')
def index():
    return render_template('index.html', output={})

@app.route('/calculate', methods=['POST'])
def calculate():
    width = float(request.form['width'])
    height = float(request.form['height'])
    depth = float(request.form['depth'])

    # Calculate total required extrusion (in mm) for display
    angle_joiner_extrusion = int((width + height + depth) * 4)
    hybrid_joiner_extrusion = int((width + depth) * 2)

    # Build lists of required cuts for each extrusion type.
    # For angle joiner: 4 edges of width, height, and depth each.
    angle_cuts = (
        [('Width', int(width))] * 4 +
        [('Height', int(height))] * 4 +
        [('Depth', int(depth))] * 4
    )
    # For hybrid joiner: 2 edges of width and 2 edges of depth.
    hybrid_cuts = (
        [('Width', int(width))] * 2 +
        [('Depth', int(depth))] * 2
    )

    # Pack the required cuts into 1.5m (1500mm) pieces.
    angle_bins = pack_cuts(angle_cuts, piece_length=1500)
    hybrid_bins = pack_cuts(hybrid_cuts, piece_length=1500)

    output = {
        'angle_joiner_extrusion': angle_joiner_extrusion,
        'hybrid_joiner_extrusion': hybrid_joiner_extrusion,
        'angle_pieces': len(angle_bins),
        'hybrid_pieces': len(hybrid_bins),
        'angle_cut_list': angle_bins,
        'hybrid_cut_list': hybrid_bins,
        'width': int(width),
        'height': int(height),
        'depth': int(depth)
    }

    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51337, debug=True, threaded=True)
