# 📚 Library Management System (Tkinter + MySQL)

This is a GUI-based **Library Management System** built using **Python Tkinter** for the frontend and **MySQL** for data storage. It is designed to help manage books and members in a library efficiently with a user-friendly interface.

---

## 🚀 What This Project Can Do

- Add, update, delete **Books**
- Add, update, delete **Members**
- Issue and return books
- Automatically calculates **fine** for late returns
- Shows borrowing history and unreturned books
- All sensitive operations (like update/delete) are **password protected**
- Built-in **search** for books and members
- Fullscreen, image-based GUI for better UX

---

## 💻 Tech Stack

- **Python 3.x**
- **Tkinter** (GUI)
- **tkcalendar** (for date picking)
- **MySQL**
- **mysql-connector-python**
- **PyInstaller** (to generate `.exe`)

---

## 🧑‍🏭 What You Need To Do Before Running

### 1. ▶️ Run Setup Script

Just run the setup file to automatically install all dependencies and configure the environment:

```bash
python setup.py
```

✅ This will:
- Install required Python packages (`tkcalendar`, `mysql-connector-python`, etc.)
- Prepare for `.exe` build if needed

---

### 2. 🔐 Change the Hardcoded MySQL Password

In `library.py`, near the top, you will find:

```python
mysql_password = 'your-password-here'
```

➡️ **Replace `your-password-here` with your own MySQL password.**

---

### 3. 🖼️ Make Sure Image Folder Exists

There is a folder called `widget_images/` that contains all GUI images.

📁 Make sure it is in the same directory as `library.py`.

---

### 4. ▶️ To Run the App

```bash
python library.py
```

---

### 5. 🛠️ To Create `.exe` (Optional)

Once setup is complete, you can also generate a `.exe` version:

```bash
python setup.py
```

The executable will be saved inside the `dist/` folder.

---

## 📌 Notes

- Password is needed for sensitive actions (update, delete).
- All background images and icons are loaded from `widget_images/` folder.
- When running as `.exe`, image paths are auto-adjusted.
- No external server or hosting required. Everything runs locally.

---

## 👤 Author

**Logeshwaran U**  
If you found this project helpful, feel free to give it a ⭐
