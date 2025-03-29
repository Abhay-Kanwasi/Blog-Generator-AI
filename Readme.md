# AI Blog Generator

A web application that generates blog posts using AI. This project consists of a React frontend and a FastAPI backend that leverages Large Language Models from Groq and Hugging Face.

## Features

- Generate blog posts on any topic
- Choose from multiple writing tones (formal, casual, professional, friendly, technical)
- Select between different AI providers (Groq and Hugging Face)
- Copy generated content to clipboard with one click
- Responsive user interface

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- CSS

### Backend
- FastAPI
- Python
- httpx (for API requests)
- python-dotenv (for environment variable management)

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.7 or higher)
- API keys for Groq and/or Hugging Face

## Installation

### Backend Setup

1. Clone this repository:
   ```bash
   git clone https://https://github.com/Abhay-Kanwasi/Blog-Generator-AI.git
   cd AI Blog Generator/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn httpx python-dotenv
   ```

4. Create a `.env` file in the backend directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   HF_API_KEY=your_huggingface_api_key_here
   HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.2
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

## Usage

1. Enter a blog topic in the input field
2. Select a tone for your blog post
3. Choose your preferred AI provider (Groq or Hugging Face)
4. Click "Generate Blog"
5. Wait for the AI to generate your blog post
6. Use the "Copy to Clipboard" button to copy the generated content

## API Endpoints

- `POST /generate` - Generate a blog post
  - Request body:
    ```json
    {
      "topic": "Your blog topic",
      "tone": "formal",
      "apiProvider": "groq"
    }
    ```
  - Response:
    ```json
    {
      "content": "Generated blog content...",
      "status": "success"
    }
    ```

## Project Structure

```
AI Blog Generator/
├── backend/
│   ├── main.py            # FastAPI application
│   ├── .env               # Environment variables
│   └── venv/              # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # Main React component
│   │   ├── App.css        # Styling
│   │   ├── main.tsx       # React entry point
│   │   └── ...
│   ├── package.json
│   └── ...
└── README.md
```

## Getting API Keys

### Groq API Key
1. Go to [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key

### Hugging Face API Key
1. Go to [Hugging Face](https://huggingface.co/settings/tokens)
2. Sign up or log in
3. Generate a new API token

## Deployment

### Backend
You can deploy the FastAPI backend on platforms like:
- Heroku
- Render
- AWS Lambda
- Google Cloud Run

### Frontend
The React frontend can be deployed on:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Groq](https://groq.com/) for their LLM API
- [Hugging Face](https://huggingface.co/) for their open-source models
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend library
- [Vite](https://vitejs.dev/) for the frontend build tool