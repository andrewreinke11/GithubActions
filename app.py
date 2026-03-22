from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Game state
stuff = 0
upgrades = [
    {"name": "click", "initialCost": 10, "currentCost": 10, "costMultiplier": 1.2, "power": 1, "powerMultiplier": 5},
    {"name": "autoClick", "initialCost": 100, "currentCost": 100, "costMultiplier": 1.5, "power": 0, "powerMultiplier": 4}
]

def buy_upgrade(upgrade_index: int):
    global stuff
    if stuff >= upgrades[upgrade_index]['currentCost']:
        stuff -= upgrades[upgrade_index]['currentCost']
        upgrades[upgrade_index]['currentCost'] *= upgrades[upgrade_index]['costMultiplier']
        upgrades[upgrade_index]['power'] += upgrades[upgrade_index]['powerMultiplier']
        return True
    return False

def click():
    global stuff
    stuff += upgrades[0]['power']

def do_next_second():
    global stuff
    stuff += upgrades[0]['power'] * upgrades[1]['power']


def has_won():
    return stuff >= 1000000

@app.route('/won')
def check_won():
    return jsonify({"won": has_won(), "stuff": stuff})

@app.route('/')
def index():
    return render_template('index.html', stuff=stuff, upgrades=upgrades)

@app.route('/click', methods=['POST'])
def handle_click():
    click()
    return jsonify({'stuff': stuff})

@app.route('/buy/<int:upgrade_id>', methods=['POST'])
def handle_buy(upgrade_id):
    if 0 <= upgrade_id < len(upgrades):
        success = buy_upgrade(upgrade_id)
        return jsonify({'success': success, 'stuff': stuff, 'upgrades': upgrades})
    return jsonify({'success': False})

@app.route('/auto_click', methods=['POST'])
def handle_auto_click():
    do_next_second()
    return jsonify({'stuff': stuff})

@app.route('/status')
def get_status():
    return jsonify({'stuff': stuff, 'upgrades': upgrades})

if __name__ == '__main__':
    app.run(debug=True)