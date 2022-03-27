from flask import Flask, render_template, request, redirect, url_for
from dbworker import DbWorker

app = Flask(__name__)
db = DbWorker()

@app.route('/')
def home():
    data = []
    busy = request.args.get('busy')
    min_capacity = request.args.get('min_capacity')
    rec_id = request.args.get('rec_id')

    try:
        rec_id = int(rec_id)
    except:
        pass

    if busy == 'true':
        data = db.get_all_transport_by_busy_and_capacity(1, min_capacity if min_capacity else 0)
    elif busy == 'false':
        data = db.get_all_transport_by_busy_and_capacity(0, min_capacity if min_capacity else 0)
    elif min_capacity:
        data = db.get_all_transport_by_capacity(min_capacity)
    else:
        data = db.get_all_transport()

    return render_template('home.html', transport=data, busy=busy, min_capacity=min_capacity, rec_id=rec_id)

@app.route('/reserve-car/<id>')
def reserve_car(id):
    db.reserve_car_by_id(id)
    return redirect(url_for('home'))

@app.route('/unreserve-car/<id>')
def unreserve_car(id):
    db.unreserve_car_by_id(id)
    return redirect(url_for('home'))

@app.route('/delete-car/<id>')
def delete_car(id):
    db.delete_car_by_id(id)
    return redirect(url_for('home'))

@app.route('/select-type', methods=('GET', 'POST'))
def select_type():
    if request.method == 'GET':
        _types = db.get_all_types()
        print(_types)
        return render_template('select-type.html', types=_types)

    print(request.form['type_id'])
    return redirect(url_for('add_car', type_id=request.form['type_id']))

@app.route('/add-request', methods=('GET', 'POST'))
def add_request():
    if request.method == 'GET':
        return render_template('add-request.html')

    print(request.form)

    rec_id = db.get_matching_car_id(float(request.form['length']), float(request.form['width']), float(request.form['height']), float(request.form["weight"]))

    return redirect(url_for('home', rec_id=rec_id if rec_id else -1))

@app.route('/add-car/<type_id>', methods=('GET', 'POST'))
def add_car(type_id):
    
    if request.method == 'POST':
        print(f'Adding car: {request.form}')
        _type = db.get_type_by_id(type_id)

        if _type.minLength <= float(request.form['length']) <= _type.maxLength \
        and _type.minWidth <= float(request.form['width']) <= _type.maxWidth \
        and _type.minHeight <= float(request.form['height']) <= _type.maxHeight:
            db.add_car(type_id, 
                    request.form['name'], 
                    request.form['length'], 
                    request.form['width'], 
                    request.form['height'])
            return redirect(url_for('home'))
        
        types = db.get_all_types()
        return render_template('add-car.html', types=types, error='Выбранные габариты не укладываются в габариты выбранного типа')

    # GET

    _type = db.get_type_by_id(type_id)
    return render_template('add-car.html', _type=_type)

