# Tea Shop

A Django-based e-commerce platform for selling premium teas.

## Features

- Product catalog with categories
- Shopping cart functionality
- User authentication and profiles
- Order management
- razorpay payment integration
- Responsive design

## Prerequisites

- Python 3.8+
- PostgreSQL
- razorpay account (for payments)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tea-shop.git
cd tea-shop
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your_django_secret_key
DATABASE_URL=postgres://username:password@localhost:5432/tea_shop_db
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Create the database:
```bash
createdb tea_shop_db
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Populate the database with initial data:
```bash
python manage.py populate_db
```

9. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the admin interface at `http://localhost:8000/admin`
2. Browse products at `http://localhost:8000/products`
3. Create an account at `http://localhost:8000/accounts/register`
4. Add products to cart and proceed to checkout

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django
- Bootstrap
- Razorpay
- PostgreSQL 