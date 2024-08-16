# PetStore Web Application

This project is a web application designed for managing and selling pet products to end users. It provides core functionalities for browsing products, handling orders, and managing user accounts. The application is designed to be user-friendly and efficient, allowing pet owners to easily purchase products for their pets.

## Features

- **`Product Management`**: Manage a catalog of pet products, including adding, updating, and removing product listings.
- **`Order Processing`**: Handle customer orders, including order creation, updating, and tracking.
- **`User Authentication`**: Secure user login and registration with encrypted passwords.
- **`RESTful API`**: Expose key functionalities through a RESTful API, enabling easy integration with front-end applications or other services.
- **`Responsive design`**: Access the application from any device with a responsive design that adjusts to various screen sizes.
  
## Installation

1. **Clone the Repository**:

    ```bash
    git clone <URL-of-the-repository>
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd petstore-web-application
    ```

3. **Install Dependencies**:

    Make sure you have Python and pip installed. Then install the dependencies with:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:

   Start the development server with:

    ```bash
    py manage.py runserver
    ```

    The application will start on port 8000 by default.

## Configuration

- **Access Credentials**: Use the following credentials to access the application:

    - Username: admin
    - Password: mauricio123
  
- **Environment Variables**: Configure environment variables for database connections, API keys, and other settings. Create a `.env` file in the root directory and set the necessary variables.

    Example:

    ```env
    DATABASE_URL=your_database_url
    PORT=8000
    ```

## Usage

- **API Endpoints**:

    - **GET /products**: Retrieve the list of products available for purchase.
    - **POST /products**: Add a new product to the catalog.
    - **PUT /products/{id}**: Update product details.
    - **DELETE /products/{id}**: Remove a product from the catalog.
    - **POST /orders**: Create a new order.
    - **GET /orders/{id}**: Get details of an order.

- **Authentication**: Use JWT tokens for secure access. Include the token in the `Authorization` header of your requests.

## Testing

- **Unit Tests**: Run unit tests using Python's testing framework:

    ```bash
    pytest
    ```

- **Integration Tests**: Ensure all components work together as expected. Refer to the `test` directory for integration test scripts.

## Contributing

1. **Fork the Repository**: Create a personal copy of the repository by forking it on GitHub.
2. **Create a Branch**: Make a new branch for your changes:

    ```bash
    git checkout -b feature/your-feature
    ```

3. **Make Changes**: Implement your changes and test them.
4. **Submit a Pull Request**: Push your branch and create a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
