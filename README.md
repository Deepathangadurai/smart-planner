# SmartPlanner

**SmartPlanner** is a data-driven productivity dashboard designed to help users organize their life through structured goal setting. Unlike standard to-do lists, it categorizes tasks into **Daily**, **Weekly**, and **Monthly** objectives, offering a high-level view of your personal progress.



## Key Features

* **Secure Authentication:** Complete user registration and login system with password hashing (Werkzeug security).
* **Data Visualization:** Dynamic progress bars that calculate real-time completion rates for each category.
* **Full CRUD System:** Create, Read, Update (mark complete), and Delete tasks instantly.
* **Responsive Design:** Professional UI built with CSS Grid/Flexbox that works on mobile and desktop.
* **Duplicate Protection:** Smart logic to prevent duplicate usernames and ensure data integrity.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite, SQLAlchemy
* **Frontend:** HTML5, CSS3, Jinja2 Templating
* **Icons:** Font Awesome 6
* **Fonts:** Plus Jakarta Sans (Google Fonts)

## Installation & Setup

Want to run this project locally? Follow these steps:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Deepathangadurai/smart-planner.git](https://github.com/Deepathangadurai/smart-planner.git)
    cd smart-planner
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App**
    ```bash
    python app.py
    ```

5.  **Visit the App**
    Open your browser and go to `http://127.0.0.1:5000`

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).

---
*Built by [Deepa Thangadurai](https://github.com/Deepathangadurai)*
