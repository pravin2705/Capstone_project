
Follow these steps to set up the project folder, create a virtual environment, install dependencies, and run the API.

### 1. Project Setup
Ensure all your project files are in a single folder. Open your terminal and navigate to that directory:
```bash
cd path/to/your/project-folder
```

### 2. Create a Virtual Environment
Create an isolated environment to prevent package conflicts:

- **Windows:**
  ```bash
  python -m venv venv
  ```

### 3. Activate the Virtual Environment
Activate the environment before installing packages:

- **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```

### 4. Install Dependencies
Install all the required packages listed in your `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 5. Run the Application
Execute the following command to start the application server:
```
python -m uvicorn app.main:app --reload
```
