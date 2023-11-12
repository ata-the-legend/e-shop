# E-commerce Project

This is an e-commerce project built with Python Django. It provides a platform for online shopping and includes features such as product browsing, shopping cart management, user authentication, and order processing.

## Requirements

To run this project, you will need:

- Python 3.9 or higher
- Other dependencies listed in the requirements.txt file

## Technologies Used

- Django: The web framework used to build the application.
- Celery: A distributed task queue system used for asynchronous processing of tasks.
- Arvan Cloud Storages: A cloud storage service used for storing and serving static files and media uploads.
- RabbitMQ: A message broker used for celery.
- Docker: A containerization platform used for packaging the application and its dependencies.
- Redis: An in-memory data structure store used for caching and session management.

## Features

- Product browsing: Users can browse the product catalog and view detailed information about each product.
- Shopping cart management: Users can add products to the shopping cart, update quantities, and remove items.
- User authentication: Users can register, log in, and log out. Authenticated users have access to additional features such as order history and saved addresses.
- Order processing: Users can proceed to checkout, enter shipping and payment information, and place orders.
- Admin interface: Admin users can manage products, categories, and orders through the Django admin interface.
- Asynchronous tasks: Celery is used to handle asynchronous tasks such as sending order confirmation emails and processing background tasks.
- Static files and media storage: Arvan Cloud Storages is used to store and serve static files and media uploads for the application.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ecommerce-project.git
2. Change into the project directory:

   ```
   cd ecommerce-project
4. Create and activate a virtual environment:

    ```
    python3 -m venv env
    source env/bin/activate
4. Install the project dependencies:

    ```
    pip install -r requirements.txt
5. Set up the database:

    ```
    python manage.py migrate
6. Start the development server:

    ```
    python manage.py runserver
7. Open your web browser and visit <http://localhost:8000> to access the application.

## Usage

Browse the product catalog and view detailed product information.
Add products to the shopping cart and manage the cart items.
Proceed to checkout and place orders.
Authenticate as a registered user to access additional features such as order history and saved addresses.
Admin users can manage products, categories, and orders through the Django admin interface.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
