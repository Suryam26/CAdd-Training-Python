# Imports
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


# Configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    department = db.relationship('Departments', cascade="all,delete", back_populates='manager', lazy='dynamic')

    def __repr__(self):
        return f"Employee('{self.id}', '{self.name}')"

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    manager = db.relationship('Employee')

    def __repr__(self):
        return f"Department('{self.id}', '{self.name}')"


# Routes
@app.route('/emp', methods=['POST', 'GET'])
def emp():
    if request.method == 'POST':
        name = request.form['name']
        employee=Employee(name=name)
        try:
            print("done")
            db.session.add(employee)
            db.session.commit()
            return redirect('/emp')
        except:
            return "Problem adding employee!"
    else:
        employee = Employee.query.order_by(Employee.id).all()
        return render_template('emp.html', employee=employee)


@app.route('/dep', methods=['POST', 'GET'])
def dep():
    if request.method == 'POST':
        name = request.form['name']
        manager_id = request.form['manager_id']
        emp = Employee.query.get_or_404(manager_id)
        department=Departments(name=name, manager=emp)
        try:
            db.session.add(department)
            db.session.commit()
            return redirect('/dep')
        except:
            return "Problem adding department!"
    else:
        emp = Employee.query.order_by(Employee.id).all()
        department=Departments.query.order_by(Departments.id).all()
        return render_template('dep.html', department=department, emp=emp)


@app.route('/update/<int:id>', methods = ["POST", "GET"])
def update(id):
    emp = Employee.query.get_or_404(id)
    if request.method == 'POST':
        emp.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/emp")
        except:
            return "Cannot update employee Info!!!"

    else:
        return render_template("update.html", emp = emp)


@app.route('/delete/emp/<int:id>')  
def delete_emp(id):
    e_del=Employee.query.get_or_404(id)
    try:
        db.session.delete(e_del)
        db.session.commit()
        return redirect('/emp')
    except:
        return "Problem in deleting data!!!"


@app.route('/delete/dep/<int:id>')  
def delete_dep(id):
    d_del=Departments.query.get_or_404(id)
    try:
        db.session.delete(d_del)
        db.session.commit()
        return redirect('/dep')
    except:
        return "Problem in deleting data!!!"


# Main 
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')