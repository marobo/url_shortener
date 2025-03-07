# URL Shortener

A Django-based URL shortener application that allows you to create short URLs and generate QR codes.

## Features

- Create short URLs from long URLs
- Generate QR codes for shortened URLs
- Custom URL aliases support
- List and manage all shortened URLs
- Responsive design with Bootstrap 5
- Dark mode interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url_shortener.git
cd url_shortener
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

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Visit http://127.0.0.1:8000/ in your browser.

## Usage

1. Enter a long URL on the home page
2. Optionally provide a custom alias
3. Get your shortened URL and QR code
4. View all your shortened URLs in the URL List page

## Technologies Used

- Django 4.2
- Bootstrap 5
- QR Code generation
- Python 3.x

## License

This project is licensed under the MIT License - see the LICENSE file for details. 