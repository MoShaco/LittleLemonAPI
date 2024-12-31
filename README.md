Restaurant API
A simple backend API for a restaurant platform that supports user registration, authentication, authorization, and group management. Administrators can manage categories and menu items, while customers can browse them.

Features
Admin
Register, Login
Admin can create an account and login to obtain an authentication token.
View Profile
Admin can view personal profile information.
CRUD Categories
Create, Read, Update, and Delete menu categories (e.g., Appetizers, Main Dishes, Desserts).
CRUD Menu Items
Create, Read, Update, and Delete menu items.
Group Management
Admin can add other users to groups (e.g., Manager, Delivery Crew).
Customer
Register, Login
Customers can create an account and login.
View Profile
Customers can view personal profile information.
Read Menu Items
Customers can view the list of available menu items.
Read Categories
Customers can also view the categories.
Core Functionalities
Authentication: Users need to register and then log in to obtain an authentication token.
Authorization: Depending on the user’s role (Admin, Manager, Delivery Crew, Customer), they can access different endpoints with proper permissions.
CRUD Operations: Admin can manage Categories and Menu Items.
Group Management: Admin can assign users to groups (e.g., Manager, Delivery Crew, etc.).
Getting Started
These instructions will help you run the project on your local machine for development and testing purposes.
