# Code Interview Application

This is a full-stack web application for conducting real-time online coding interviews.

## Project Structure

- `backend/`: Node.js, Express, Socket.IO server
- `frontend/`: Plain JavaScript, Vite, Monaco Editor client

## How to Run

### Prerequisites

- Node.js (v14 or later)
- npm

### Installation

1.  Install dependencies for both backend and frontend:
    ```bash
    npm install
    ```

### Running the Application

1.  Start the development servers for both backend and frontend:
    ```bash
    npm run dev
    ```
    - The backend will be running on `http://localhost:3000`.
    - The frontend will be running on `http://localhost:5173`.

2.  Open your browser and navigate to `http://localhost:5173`. A new session will be created automatically.

3.  Share the URL with another person to join the same session.

### Running Tests

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Run the tests:
    ```bash
    npm test
    ```

## Features

- Real-time collaborative code editor using Monaco Editor and Socket.IO.
- Create and join interview sessions.
- In-browser JavaScript code execution (Ctrl+Enter or Cmd+Enter).
- Split-panel layout for code editor and output.
- Dark theme.
