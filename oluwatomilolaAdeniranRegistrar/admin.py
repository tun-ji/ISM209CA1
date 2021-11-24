from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import models  # our custom defined models

#create a Blueprint variable named admin_page.
admin_page = Blueprint('admin_page', __name__, template_folder='templates/admin')

def logged_in():
    if 'username' not in session or 'admin' not in session['userroles']:
        return False
    else:
        return True


@admin_page.route("/admin/")
def admin():
    if not logged_in():
        return redirect(url_for('login', next='/admin/'))
    # username in session and user has admin role, continue
    return render_template('index.html', title="ADMIN", information="Here you can register customers. Click on what you would like to do")


@admin_page.route("/admin/customers/")
def customers():
    if not logged_in():
        return redirect(url_for('login', next='/admin/customers/'))

    # username in session, continue
    # get our registered products from the database
    customers = models.Customers.query.all()
    information = request.args.get('information', 'Here you can register customers')
    css = request.args.get('css', 'normal')
    return render_template('customers.html', title="Register Customers", information=information, css=css, customers=customers)


@admin_page.route("/admin/customers/add-customers/", methods=['POST','GET'])
def process_customer_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue

    if request.method != 'POST':
        # return to products-and-services.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new products'
        return render_template('customers.html', title="REGISTER CUSTOMERS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent from the form.
    Fname = request.form['First_name']
    Sname = request.form['Surname']
    Dob = request.form['Date_of_Birth']
    Radd = request.form['Residential_address']
    Nity = request.form['Nationality']
    Nid = request.form['National_Identification_Number']

    # let's write to the database
    try:
        customer = models.Customers(First_name=Fname, Surname=Sname, Date_of_Birth=Dob, Residential_address=Radd, Nationality=Nity, National_Identification_Number=Nid)
        models.db.session.add(customer)
        models.db.session.commit()
    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('customers.html', title="REGISTER CUSTOMERS", information=error, css="error")
    # no error, continue
    return redirect(url_for('admin_page.customers', information="Add successful", css="success"))


@admin_page.route("/admin/customers/edit/<int:id>/", methods=['POST', 'GET'])
def customers_edit(id):
    # check database for the product to edit
    customer = models.Customers.query.filter_by(id=id).first()
    # send to the edit form
    return render_template('customer-edit.html', customer=customer)


@admin_page.route("/admin/customers/process-customer-edit/<int:id>/", methods=['POST', 'GET'])
def process_customer_edit(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/customers/'))
    # username in session and admin in role, continue
    if request.method != 'POST':
        # redirect to signup form. Only POST method is allowed
        error = 'Please use the form to edit customers'
        return render_template('customers.html', title="REGISTER CUSTOMERS", information=error, css="error")
    # No problem so far, get the request object and the parameters sent.
    Fname = request.form['First_name']
    Sname = request.form['Surname']
    Dob = request.form['Date_of_Birth']
    Radd = request.form['Residential_address']
    Nity = request.form['Nationality']
    Nid = request.form['National_Identification_Number']
    # let's update the database
    try:
        # Get the existing data from database as object
        customer = models.Customers.query.filter_by(id=id).first()
        # Update the fields
        customer.First_name = Fname
        customer.Surname = Sname
        customer.Date_of_Birth = Dob
        customer.Residential_Address = Radd
        customer.Nationality = Nity
        customer.National_Identification_Number = Nid
        # commit
        models.db.session.commit()
    except Exception as e:
        error = 'Could not update customer. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.customers', information="Update not successful", css="error"))
    return redirect(url_for('admin_page.customers', information="Update successful", css="success"))


@admin_page.route("/admin/customers/delete/<int:id>/", methods=['POST', 'GET'])
def customer_delete(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/customers/'))
        # username in session and admin role, continue
        # No problem so far
        # let's update the database
    try:
        # Get the existing data from database as object
        customer = models.Customers.query.filter_by(id=id).first()
        # Delete the record
        models.db.session.delete(customer)
        # commit
        models.db.session.commit()
    except Exception as e:
        error = 'Could not delete customer. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.customers', information="Delete not successful", css="error"))
    return redirect(url_for('admin_page.customers', information="Delete successful", css="success"))

