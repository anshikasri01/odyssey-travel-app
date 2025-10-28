# ✈️ Odyssey Travel App - Dynamic Web Service

Ek mobile-responsive travel application jo Flask aur PostgreSQL ka upyog karke alag-alag destinations ko manage karta hai. Users ismein feedback submit kar sakte hain.

## 🌐 Live Application Link

Yeh application **Render Web Service** par deploy ki gayi hai.

**Live Link:** [https://odyssey-travel-app.onrender.com/](https://odyssey-travel-app.onrender.com/)

---

### ✨ Key Features

* **Destinations Display:** Database se dynamic tareeke se tours aur destinations ko load karta hai.
* **User Feedback System:** Users dwara submit kiye gaye feedback ko seedhe PostgreSQL database mein store karta hai.
* **Full Mobile Responsiveness:** CSS **Media Queries** ka upyog karke mobile, tablet, aur desktop screen sizes ke liye optimized.
* **Database Integration:** Data storage aur management ke liye **PostgreSQL** ka upyog kiya gaya hai.
* **Professional Deployment:** Cloud platform **Render** par deploy kiya gaya hai.

---

### 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python, **Flask** | Server-side logic, routing, aur database connection. |
| **Database** | **PostgreSQL** (Render) | Permanent data storage (Destinations, Feedback). |
| **Frontend** | HTML5, CSS3, JavaScript | User Interface, styling, aur interactivity. |
| **Deployment** | **Git** & **Render** | Version control aur production environment par hosting. |

---

### ⚙️ Local Setup Steps

Agar aap is project ko apne computer par run karna chahte hain:

1.  **Repository Clone Karein:**
    ```bash
    git clone [https://github.com/anshikasri01/odyssey-travel-app.git](https://github.com/anshikasri01/odyssey-travel-app.git)
    cd odyssey-travel-app
    ```
2.  **Virtual Environment Banayein:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (Mac/Linux)
    # Ya
    venv\Scripts\activate     # (Windows)
    ```
3.  **Dependencies Install Karein:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Environment Variables Set Karein:**
    * **`DATABASE_URL`**: Apne local PostgreSQL database ka URL set karein.
    * **`SECRET_KEY`**: Flask session management ke liye koi bhi secret key set karein.
5.  **Application Run Karein:**
    ```bash
    gunicorn app:app
    ```
    