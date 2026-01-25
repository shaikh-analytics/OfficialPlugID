# OfficialFakeID - Django E-Commerce Platform

A full-featured e-commerce application built with Python Django Framework for selling fake IDs and related products.

## Features

### Core Functionality
- **Custom User Model** - Extended user authentication with custom Account model
- **Product Management** - Categories, products with unlimited image galleries
- **Shopping Cart** - Add, increment, decrement, and remove cart items
- **Order Management** - Complete order processing workflow
- **Multiple Payment Methods** - Direct payment, Crypto payment, and Reference payment options
- **Crypto Payment Integration** - Support for cryptocurrency payments with proof upload
- **Order Tracking** - Track order status (New, Accepted, Completed, Cancelled)
- **Email Notifications** - Automated order confirmation emails
- **Admin Panel** - Comprehensive admin interface with honeypot protection

### User Features
- **User Registration & Authentication** - Complete user account system
- **Profile Management** - Edit profile, upload profile pictures, change passwords
- **Order History** - View and manage past orders
- **Personal Information Form** - Detailed personal information collection for ID creation
- **Review & Rating System** - Interactive star ratings (including half-star ratings)

### Advanced Features
- **Product Variations** - Support for different product options
- **Auto Stock Management** - Automatic inventory reduction on order completion
- **Session Management** - Auto-logout after inactivity
- **Admin Thumbnails** - Enhanced admin interface with image previews
- **CSRF Protection** - Security against cross-site request forgery

## Technology Stack

- **Framework:** Django 3.1.14
- **Database:** SQLite3 (Development) / PostgreSQL (Production Ready)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Image Processing:** Pillow
- **Configuration:** python-decouple

## Project Structure

```
fackerID/
├── accounts/           # User authentication and profile management
├── category/           # Product categories
├── store/              # Products, variations, and reviews
├── carts/              # Shopping cart functionality
├── orders/             # Order processing and payment handling
├── officalfakerid/     # Main project settings
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, Images)
├── media/              # User uploaded files
└── manage.py           # Django management script
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fackerID
   ```

2. **Create and activate virtual environment**

   Using venv:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

   Using conda:
   ```bash
   conda create -n myenv python=3.11
   conda activate myenv
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   Create a `.env` file in the root directory:
   ```bash
   cp .env-sample .env  # If .env-sample exists
   # OR create .env manually
   ```

   Add the following environment variables to `.env`:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_USE_TLS=True
   ```

   **Generate SECRET_KEY:** Use [https://djecrety.ir/](https://djecrety.ir/) to generate a secure secret key.

   **Gmail Users:** You need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

5. **Create migrations directories** (if missing)
   ```bash
   mkdir -p accounts/migrations && touch accounts/migrations/__init__.py
   mkdir -p category/migrations && touch category/migrations/__init__.py
   mkdir -p store/migrations && touch store/migrations/__init__.py
   mkdir -p carts/migrations && touch carts/migrations/__init__.py
   mkdir -p orders/migrations && touch orders/migrations/__init__.py
   ```

6. **Generate and run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to create your admin account.

8. **Collect static files** (for production)
   ```bash
   python manage.py collectstatic
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Main site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - Admin panel: [http://127.0.0.1:8000/securelogin/](http://127.0.0.1:8000/securelogin/)

## Usage Guide

### Admin Panel Setup

1. Login to admin panel using superuser credentials
2. Add product categories (Category section)
3. Add products with details and images
4. Add product variations (size, color, etc.)
5. Configure payment methods

### Customer Workflow

1. **Browse Products** - View products by category
2. **Add to Cart** - Select variations and add items to cart
3. **Checkout** - Fill in shipping and personal information
4. **Payment** - Choose payment method (Direct/Crypto/Reference)
5. **Order Confirmation** - Receive order confirmation via email
6. **Track Order** - View order status in "My Orders"

### Payment Methods

- **Direct Payment** - Traditional payment processing
- **Crypto Payment** - Cryptocurrency payment with wallet URL and proof upload
- **Reference Payment** - Payment via reference number

## Troubleshooting

### Migration Errors
If you encounter "no such table" errors:
```bash
# Ensure migrations directories exist
mkdir -p app_name/migrations && touch app_name/migrations/__init__.py

# Recreate migrations
python manage.py makemigrations app_name
python manage.py migrate app_name
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Email Not Sending
- Verify EMAIL settings in `.env`
- For Gmail, ensure you're using an App Password
- Check if "Less secure app access" is enabled (if not using App Password)

### Permission Errors
```bash
# Fix media folder permissions
chmod -R 755 media/
```

## Database Models

### Key Models
- **Account** - Custom user model with extended fields
- **Category** - Product categories
- **Product** - Product information and details
- **Variation** - Product variations (size, color, etc.)
- **Cart** - Shopping cart
- **CartItem** - Items in cart with variations
- **Order** - Order information
- **OrderProduct** - Products in an order
- **Payment** - Payment processing and tracking
- **PersonalInfo** - Customer personal information for ID creation

## Security Features

- CSRF Protection
- Admin Honeypot (fake admin panel at `/admin/`)
- Secure password hashing
- Session timeout after inactivity
- SQL injection protection via Django ORM
- XSS protection

## Development

### Project Settings
Main settings file: `officalfakerid/settings.py`

### URL Configuration
Main URL config: `officalfakerid/urls.py`

### Adding New Features
1. Create/modify models in respective app
2. Generate migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update views and templates
5. Add URL patterns
6. Test thoroughly

## Production Deployment

### Pre-deployment Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `ALLOWED_HOSTS` in settings
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure proper static file serving
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure email backend properly
- [ ] Set strong `SECRET_KEY`
- [ ] Enable security middleware
- [ ] Set up backup system
- [ ] Configure logging

### Recommended Production Stack
- **Web Server:** Nginx
- **WSGI Server:** Gunicorn
- **Database:** PostgreSQL
- **Cache:** Redis
- **Storage:** AWS S3 (for media files)
- **Hosting:** AWS, DigitalOcean, or Heroku

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is for educational purposes. Please ensure compliance with local laws and regulations regarding the use of this software.

## Support

If you encounter any issues or have questions, please open an issue in the repository.

---

Made with Python Django Framework
