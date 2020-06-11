from flask import Flask, render_template, request, redirect, url_for
from utils.db_connect import db_connect

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = False
@app.route('/menu/', methods = ['GET', 'POST'])

def menu():
    try:
        inquiry = request.args['inquiry']
    except:
        inquiry = None

    try:
        button_search = request.form['search']
    except:
        button_search = None

    if button_search == 'search':
        month = request.form['month']
        year = request.form['year'] 
        return redirect(url_for('procedure', month=month, year=year))
    
    if inquiry == '1':
        return redirect(url_for('first_request'))
    if inquiry == '2':
        return redirect(url_for('second_request'))
    if inquiry == '3':
        return redirect(url_for('third_request'))
    if inquiry == '4':
        return redirect(url_for('fourth_request'))
    if inquiry == '5':
        return redirect(url_for('fifth_request'))
    if inquiry == '6':
        return redirect(url_for('sixth_request'))
    elif inquiry == 'exit':
        return render_template('good_bye.html')
    else:
        return render_template('menu.html')

@app.route('/menu/firstRequest/', methods = ['GET', 'POST'])

def first_request():
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    _SQL = """SELECT Flight, Date_and_Time, SUM(Number_of_bonuses)
                FROM departure d JOIN (SELECT Number_of_bonuses, id_departure
                                       FROM ticket t JOIN scale s ON s.Starting_price <= t.price AND t.price <= s.Final_price) n USING (id_departure)
                GROUP BY Flight;"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Flight', 'Date_and_time', 'Number_of_bonuses']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('first_request.html', strings = res)

@app.route('/menu/secondRequest/', methods = ['GET', 'POST'])

def second_request():
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    _SQL = """SELECT Airport_1, Airport_2, MONTHNAME(Date_and_Time), Class, COUNT(*)
              FROM ticket JOIN departure USING (id_departure)
              WHERE YEAR(Date_and_Time) = 2017
              GROUP BY Airport_1, Airport_2, MONTH(Date_and_Time), Class;"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Airport_1', 'Airport_2', 'Month', 'Class', 'Quantity']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('second_request.html', strings = res)

@app.route('/menu/thirdRequest/', methods = ['GET', 'POST'])

def third_request():
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    _SQL = """SELECT passenger.*
              FROM passenger JOIN ticket USING (id_passenger)
              WHERE Price = (SELECT MAX(Price)
                             FROM ticket JOIN departure USING (id_departure)
                             WHERE Flight = "XXX");"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Id', 'Full_name', 'Birthday', 'Bonuses', 'Data_update_date', 'Passport_number']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('third_request.html', strings = res)

@app.route('/menu/fourthRequest/', methods = ['GET', 'POST'])

def fourth_request():
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    _SQL = """SELECT passenger.*
              FROM passenger LEFT JOIN ticket USING (id_passenger)
              WHERE id_ticket IS NULL;"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Id', 'Full_name', 'Birthday', 'Bonuses', 'Data_update_date', 'Passport_number']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('fourth_request.html', strings = res)

@app.route('/menu/fifthRequest/', methods = ['GET', 'POST'])

def fifth_request():
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    _SQL = """SELECT p.*
              FROM passenger p LEFT JOIN (SELECT id_passenger, id_ticket
                                          FROM ticket
                                          WHERE YEAR(Date_of_purchase) = 2014 AND MONTH(Date_of_purchase) = 3) t USING (id_passenger)
              WHERE id_ticket IS NULL;"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Id', 'Full_name', 'Birthday', 'Bonuses', 'Data_update_date', 'Passport_number']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('fifth_request.html', strings = res)

@app.route('/menu/sixthRSequest/', methods = ['GET', 'POST'])

def sixth_request():
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    _SQL = """SELECT *
              FROM pass_ticket
              WHERE count_ticket = (SELECT MAX(count_ticket)
                                    FROM pass_ticket);"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Id', 'Full_name', 'Birthday', 'Bonuses', 'Data_update_date', 'Passport_number', 'Count_ticket']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('sixth_request.html', strings = res)

@app.route('/menu/procedure/', methods = ['GET', 'POST'])

def procedure():
    month = request.args.get('month')
    year = request.args.get('year')
    conn = db_connect('root', '', '127.0.0.1', 'bonus_program')
    if conn == None:
        return render_template('failed_to_connect.html')
    cursor = conn.cursor()
    args = (month, year)
    cursor.callproc('report', args)
    conn.commit()
    _SQL = """SELECT Flight, Total_cost, Bonus_amount
              FROM bonus_program.report;"""
    cursor.execute(_SQL,)
    result = cursor.fetchall()
    if not result:
        return render_template('not_found.html')
    res = []
    schema = ['Flight', 'Total_cost', 'Bonus_amount']
    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template('report.html', strings = res)

app.run(port = 5000, debug = True)

