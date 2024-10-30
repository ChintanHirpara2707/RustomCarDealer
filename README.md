# Car Dealership Website

## Overview

This project is a Car Dealership website built using the Django framework and MySQL database. The application serves as a platform for users to browse, search, and filter various car listings while allowing dealership administrators to manage inventory and sales efficiently.

## Features

### Customer Site
- **Browse Cars**: Users can view all available car listings with details such as make, model, year, price, and more.
- **Search & Filter**: Users can search for cars based on specific criteria (e.g., make, model, price range).
- **Car Details**: Detailed view of each car, including images and specifications.
- **User Registration & Login**: Customers can create accounts to save favorite cars and manage their profiles.

### Admin Site
- **Dashboard**: An overview of current inventory and sales statistics.
- **Manage Listings**: Admins can add, edit, or delete car listings from the inventory.
- **Sales Management**: Track sales and manage customer orders.
- **User Management**: Admins can manage user accounts and permissions.

## Technologies Used

- **Django**: Web framework for building the application.
- **MySQL**: Database for storing car listings and user information.
- **HTML/CSS**: For front-end design.
- **JavaScript**: For interactivity and dynamic content.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ChintanHirpara2707/RustomCarDealer.git

2. **Navigate to the Project Directory**:
   ```bash
   cd RustomCarDealer
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**:
   - Ensure MySQL is running and create a database for the project.
   - Update the database settings in `settings.py`.

5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:8000/` for the customer site.
   - Access the admin site at `http://127.0.0.1:8000/adm/`.
   - Access the Django admin site at `http://127.0.0.1:8000/admin/`.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Django Community**: For the framework and extensive resources.
- **MySQL**: For reliable database management.
- **All Contributors**: For their support and improvements to the project.

---
```
