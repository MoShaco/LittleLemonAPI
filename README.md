# LittleLemon Restaurant API

#### **Video Demo:** [Click here to watch](https://youtu.be/fCnruR74F3Y)

---

## Description

The **LittleLemon Restaurant API** is a backend system for a restaurant platform. It provides robust functionality for user registration, authentication, authorization, and group management. The platform allows administrators to manage menu categories and menu items, while customers can browse the menu. The API uses role-based access control to ensure secure and efficient operations tailored to specific user roles.

This project is designed to streamline restaurant management tasks by enabling admins to organize menu items, manage categories, and oversee user groups like Managers and Delivery Crew. For customers, it offers an easy way to browse menu options. By leveraging Django REST Framework (DRF) and libraries like Djoser for authentication, this API ensures security and a seamless user experience.

---

## Features

### **Admin Functionalities:**
1. **Register and Login:**
   - Admins can register and log in to the system, obtaining an authentication token using the Djoser library for secure token-based authentication.

2. **Profile Information:**
   - Admins can view their personal profile details, including username and email.

3. **CRUD Categories:**
   - Admins can create new categories to organize menu items (e.g., Appetizers, Main Dishes, Desserts).
   - Admins can read a list of existing categories to see how the menu is structured.
   - Admins can update categories, modifying names or descriptions as needed.
   - Admins can delete categories to remove outdated or unnecessary classifications.

4. **CRUD Menu Items:**
   - Admins can create new menu items, specifying attributes like name, description, price, and category.
   - Admins can read a list of menu items, filtering them by category or searching by name.
   - Admins can update menu items to modify details like price, availability, or description.
   - Admins can delete menu items that are no longer available or needed.

5. **Group Management:**
   - Admins can assign users to specific groups, such as Manager or Delivery Crew, granting them appropriate permissions for their roles.

### **Customer Functionalities:**
1. **Register and Login:**
   - Customers can register and log in to browse the menu and view categories. Authentication ensures customer data security and a personalized experience.

2. **Profile Information:**
   - Customers can view their profile details, including personal information like name and contact details.

3. **View Menu Items and Categories:**
   - Customers can browse the list of available menu items and categories, viewing detailed descriptions and prices.

---

## Core Functionalities

1. **Authentication:**
   - The API uses the Djoser library for token-based authentication, ensuring secure login and user data management. Tokens are generated upon login and are required for accessing user-specific endpoints.

2. **Authorization:**
   - Role-based access control ensures users only have access to features appropriate to their role. For example, customers can view menu items, while admins can manage categories and assign roles.

3. **CRUD Operations:**
   - The API supports full CRUD functionality for categories and menu items, enabling efficient management of restaurant data.

4. **Group Management:**
   - Admins can assign users to predefined groups like Manager or Delivery Crew, enabling tailored access to API endpoints based on their responsibilities.

---

## How to Run

### **1. Prerequisites:**
   - Python 3.x installed on your system.
   - pip and pipenv for managing dependencies.

### **2. Setup Instructions:**

1. Clone the Repository:
   git clone https://github.com/MoShaco/LittleLemonAPI
   cd LittleLemonAPI

2. Install pipenv
    pip install pipenv

3- Install Dependencies
    pipenv install

4- Activate it
    pipenv shell


5- Run database migrations
    python manage.py migrate

6- Run server
    python manage.py runserver

