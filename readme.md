# Resume Screener Frontend

A basic **Streamlit** application to interact with and test the [`resume-screener-backend`](https://github.com/RohanKP1/resume-screener-backend). This frontend allows users to upload resumes and view screening results based on backend processing.

## 🔧 Features

* Upload resumes (PDF)
* Interact with the backend to screen resumes
* Display candidate evaluation results
* Simple and clean Streamlit UI for quick testing and iteration

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* The [`resume-screener-backend`](https://github.com/RohanKP1/resume-screener-backend) should be running locally or accessible via URL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/RohanKP1/resume-screener-frontend.git
   cd resume-screener-frontend
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Set the backend URL inside the Streamlit app if required. You may find a line like:

```python
BACKEND_URL = "http://localhost:8000"
```

Modify it according to your backend deployment.

### Run the App

```bash
streamlit run app.py
```

The app will launch in your default web browser.

## 🧪 Example Use Case

1. Start the `resume-screener-backend`.
2. Launch this frontend.
3. Upload a candidate's resume.
4. View the screening results directly in the app.

## 📁 Project Structure

```
resume-screener-frontend/
├── src                   # Main source file
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 🛠️ Tech Stack

* [Streamlit](https://streamlit.io/)
* [Python](https://www.python.org/)
* REST API (for communication with backend)

## 🙌 Contributing

Feel free to fork the repo and submit pull requests to enhance the functionality or UI. Bug reports and feature suggestions are welcome!

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
