# Django Project

## Steps to Run Locally

### 1. Set Up a Virtual Environment

Before installing any dependencies, it's a best practice to isolate your project dependencies using a virtual environment. This will prevent conflicts between packages across different projects.

1.  **Create a virtual environment**: Run the following command to create a virtual environment in the project folder:

    ```sh
    python -m venv env
    ```

    This will create a directory called `env` that contains the environment for your project.

2.  **Activate the virtual environment**:

    - **On Windows**:

    ```sh
        .\env\Scripts\activate

        or

        cd .\env\Scripts\
        .\activate
        cd ..\..
    ```

    - **On macOS/Linux**:

      ```sh
      source env/bin/activate
      ```

    After activating, your terminal prompt should change, showing that you're now working within the `env` virtual environment.

3.  **Install the project dependencies** from the `requirements.txt` file:

    ```sh
    pip install -r requirements.txt
    ```

---

### 2. Set Up Environment Variables

Create a `.env` file in the root of the project and add your environment-specific settings such as database credentials, API keys, and other sensitive information:

```plaintext
OPENAI_API_KEY=
EMAIL_BACKEND=
EMAIL_USE_TLS=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```

---

### 3. Create a Local Database Image (PostgreSQL)

If you are using Docker, set up PostgreSQL by running:

```sh
docker-compose up
```

Ensure that the database credentials in your `.env` file match the database setup in Docker.

---

### 4. Run Tailwind CSS

Run the following command to start the Tailwind CSS development process:

```sh
python manage.py tailwind start
```

---

### 5. Apply Migrations and Create Superuser

Apply database migrations to create the necessary tables:

```sh
python manage.py migrate
```

Create a superuser for admin access:

```sh
python manage.py createsuperuser
```

---

### 6. Run the Django Development Server

Now, you can start the Django web server:

```sh
python manage.py runserver
```

Access the web application in your browser:

```
http://127.0.0.1:8000
```

---

### 7. Run Celery

To handle background tasks like email scheduling, start the **Celery worker**:

```sh
celery -A coldemail worker --pool=solo -l info
```

You can also run **Celery beat** to manage scheduled tasks:

```sh
celery -A coldemail beat -l info
```

---

### How to Reset the Database

If you need to reset the database, use the following command:

```sh
python manage.py flush
```

This will delete all data in the database but leave the schema intact.

---

Here’s a detailed description of your project that you can include in the README file to explain the functionality of your cold email automation web service:

---

## Project Overview

This project is a **Cold Email Automation Web Service** designed to streamline email communication, particularly for internal use by businesses. The service integrates with **ChatGPT** to generate personalized email content based on predefined input parameters. It features several functionalities aimed at enhancing productivity and efficiency in managing bulk email campaigns, scheduling, and customization.

### Key Features

1. **ChatGPT-Generated Email Content**:
   - Users can generate email content using personalized input based on specific groups or departments (e.g., HR, R&D).
   - The email content is optimized for different tones such as formal, casual, or persuasive, depending on the user's input.
2. **Dashboard for Email Management**:

   - A comprehensive dashboard allows users to view:
     - **Sent Emails**: A list of successfully delivered emails.
     - **Scheduled Emails**: Emails that are scheduled for future delivery. This feature provides the ability to edit or reschedule them before the scheduled sending time.

3. **Message Generator**:

   - A generator page allows users to create email content, which can be personalized and bulk-sent to different departments.
   - It also includes scheduling options, allowing users to set the exact time when the email should be sent.

4. **Bulk and Manual Email Data Input**:

   - Users can input email data either manually, one by one, or upload a CSV/Excel file to handle large batches of emails.
   - The system supports department customization, allowing departments to be created and assigned to emails.

5. **Department Customization**:

   - Administrators can manually create or modify departments within the system, which helps segment and target specific groups of email recipients.

6. **Security**:

   - For security reasons, only **superusers** are allowed to register new staff accounts.
   - This ensures that the platform remains secure and only authorized personnel have access.

7. **HTML Email Formatting**:
   - All outgoing emails are formatted in **HTML**, ensuring that they are visually appealing and maintain a professional appearance.

### Usage

This service is specifically designed for businesses to automate internal and external email communication. By leveraging AI-generated content, businesses can save time, improve engagement, and ensure the personalization of their emails to specific audiences.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
