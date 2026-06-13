from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user
)

from config import Config

from models import db

from models.user import User
from models.product import Product
from models.employee import Employee
from models.assignment import Assignment
from models.log import Log
from datetime import date


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Ana Sayfa
@app.route("/")
def home():
    return redirect(url_for("login"))


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:

            login_user(user)

            return redirect(url_for("dashboard"))

        flash("Email veya şifre yanlış.")

    return render_template("auth/login.html")


# Dashboard

@app.route("/dashboard")
@login_required
def dashboard():

    total_products = Product.query.count()

    total_employees = Employee.query.count()

    assigned_products = Assignment.query.filter_by(
        status="Aktif"
    ).count()

    stock_products = total_products - assigned_products

    return render_template(
        "dashboard/dashboard.html",
        total_products=total_products,
        total_employees=total_employees,
        assigned_products=assigned_products,
        stock_products=stock_products
    )




# Logout
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))

@app.route("/products")
@login_required
def products():

    products = Product.query.all()

    return render_template(
        "products/products.html",
        products=products
    )

@app.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        product = Product(

            name=request.form.get("name"),

            category=request.form.get("category"),

            brand=request.form.get("brand"),

            model=request.form.get("model"),

            serial_no=request.form.get("serial_no"),

            stock=request.form.get("stock")
        )

        db.session.add(product)

        db.session.commit()

        flash("Ürün başarıyla eklendi.")

        return redirect(url_for("products"))

    return render_template(
        "products/add_product.html"
    )

@app.route("/products/delete/<int:id>")
@login_required
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    flash("Ürün silindi.")

    return redirect(url_for("products"))


@app.route("/products/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form.get("name")
        product.category = request.form.get("category")
        product.brand = request.form.get("brand")
        product.model = request.form.get("model")
        product.serial_no = request.form.get("serial_no")
        product.stock = request.form.get("stock")

        db.session.commit()

        flash("Ürün güncellendi.")

        return redirect(url_for("products"))

    return render_template(
        "products/edit_product.html",
        product=product
    )

@app.route("/employees")
@login_required
def employees():

    employees = Employee.query.all()

    return render_template(
        "employees/employees.html",
        employees=employees
    )


@app.route("/employees/add", methods=["GET", "POST"])
@login_required
def add_employee():

    if request.method == "POST":

        employee = Employee(

            fullname=request.form.get("fullname"),

            department=request.form.get("department"),

            phone=request.form.get("phone"),

            email=request.form.get("email")
        )

        db.session.add(employee)

        db.session.commit()

        flash("Personel eklendi.")

        return redirect(url_for("employees"))

    return render_template(
        "employees/add_employee.html"
    )


@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_employee(id):

    employee = Employee.query.get_or_404(id)

    if request.method == "POST":

        employee.fullname = request.form.get("fullname")
        employee.department = request.form.get("department")
        employee.phone = request.form.get("phone")
        employee.email = request.form.get("email")

        db.session.commit()

        flash("Personel güncellendi.")

        return redirect(url_for("employees"))

    return render_template(
        "employees/edit_employee.html",
        employee=employee
    )


@app.route("/employees/delete/<int:id>")
@login_required
def delete_employee(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)

    db.session.commit()

    flash("Personel silindi.")

    return redirect(url_for("employees"))

@app.route("/assignments")
@login_required
def assignments():

    assignments = Assignment.query.all()

    return render_template(
        "assignments/assignments.html",
        assignments=assignments
    )

@app.route("/assignments/add", methods=["GET", "POST"])
@login_required
def add_assignment():

    products = Product.query.all()
    employees = Employee.query.all()

    if request.method == "POST":

        product_id = request.form.get("product_id")
        employee_id = request.form.get("employee_id")

        product = Product.query.get(product_id)

        # ❗ STOK KONTROL
        if product.stock <= 0:
            flash("Stok yok!")
            return redirect(url_for("assignments"))

        assignment = Assignment(
            product_id=product_id,
            employee_id=employee_id,
            assigned_date=request.form.get("assigned_date"),
            status="Aktif"
        )

        # 🔻 STOK DÜŞÜR
        product.stock -= 1

        db.session.add(assignment)
        db.session.commit()

        flash("Zimmet verildi.")

        return redirect(url_for("assignments"))

    return render_template(
        "assignments/add_assignment.html",
        products=products,
        employees=employees
    )


@app.route("/assignments/return/<int:id>")
@login_required
def return_assignment(id):

    assignment = Assignment.query.get_or_404(id)

    if assignment.status == "Aktif":

        product = Product.query.get(assignment.product_id)

        # 🔺 stok geri ekle
        product.stock += 1

        assignment.status = "İade Edildi"

        db.session.commit()

        flash("Ürün iade alındı.")

    return redirect(url_for("assignments"))


# Tabloları oluştur
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)