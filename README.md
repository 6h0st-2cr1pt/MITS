Missing Item Recovery System (MITS)

A comprehensive desktop application for managing and tracking lost and found items, built with Python and Tkinter.

## Overview

The Missing Item Recovery System (MITS) is a user-friendly desktop application designed to help organizations and institutions manage lost and found items efficiently. The system provides features for item registration, tracking, claiming, and user management.

## Features

- **User Authentication**
  - Secure login and signup system
  - Role-based access control
  - Password encryption

- **Dashboard**
  - Overview of system statistics
  - Quick access to main features
  - User-friendly interface

- **Item Management**
  - Register missing items
  - Track recovered items
  - Process claim requests
  - Item status tracking

- **User Management**
  - User registration
  - Role management
  - User profile management

- **Rewards System**
  - Track user contributions
  - Reward points system
  - Recognition for helpful users

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd MITS
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- Python 3.x
- tkinter
- ttkbootstrap
- bcrypt
- shutil

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The application will start with a splash screen, followed by the login interface.

3. New users can create an account through the signup interface.

4. After logging in, users can access various features through the dashboard.

## Database

The application uses SQLite as its database system. The database file (`item_recovery.db`) is automatically created and initialized when the application is first run.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the license included in the repository.

## Support

For support, please open an issue in the repository or contact the development team.
