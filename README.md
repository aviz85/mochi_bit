# 🍡 Mochi Bot

Welcome to Mochi Bot, your AI-powered chatbot that's as sweet and flexible as its namesake! 🤖✨

## About Mochi Bot

Mochi Bot is a delightful blend of cutting-edge AI and user-friendly design, created to bring the joy of intelligent conversation to your digital world. Just like the beloved Japanese treat, Mochi Bot comes in many flavors and can be customized to suit your taste!

### 🌟 Key Features

- **Multi-Flavored Bots**: Create various chatbot types, each with its own unique personality and purpose.
- **AI-Powered Conversations**: Leveraging Anthropic's advanced AI models for human-like interactions.
- **Customizable to the Core**: Fine-tune your bots with specific settings like response style and knowledge base.
- **User-Friendly Interface**: A sleek React frontend for smooth chatting experiences.
- **Secure & Scalable**: Built on Django with robust user authentication and RESTful API.

Whether you're looking for a virtual assistant, a customer support bot, or just a fun conversational companion, Mochi Bot has got you covered!

## 🚀 Getting Started

Let's get your very own Mochi Bot up and running!

### Prerequisites

Before we begin, make sure you have the following ingredients:

- Python 3.8+
- Node.js 14+
- npm 6+
- Git
- A pinch of excitement!

### Setup Instructions

1. **Clone the Mochi Bot repository**
   ```
   git clone https://github.com/aviz85/mochi_bot.git
   cd mochi_bot
   ```

2. **Set up the Backend (Django)**
   ```
   cd mochi_bot_backend

   # Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your settings

   # Run migrations
   python manage.py makemigrations
   python manage.py makemigrations chatbot
   python manage.py migrate

   # Create a superuser
   python manage.py createsuperuser

   # Initialize chatbot schemas
   python manage.py init_chatbot_schemas

   # Start the Django server
   python manage.py runserver
   ```

3. **Set up the Frontend (React)**
   ```
   cd ../mochi_bot_frontend

   # Install dependencies
   npm install

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your settings

   # Start the React app
   npm start
   ```

4. **Access Your Mochi Bot**
   - Frontend: Open your browser and visit `http://localhost:3000`
   - Backend API: Available at `http://localhost:8000/api`
   - Django admin: `http://localhost:8000/admin`

### 🔧 Configuration

Don't forget to configure your environment variables:

- Backend (`.env` in `mochi_bot_backend/`):
  - `DEBUG`: Set to `True` for development, `False` for production
  - `SECRET_KEY`: Your Django secret key
  - `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
  - `ANTHROPIC_API_KEY`: Your Anthropic API key

- Frontend (`.env` in `mochi_bot_frontend/`):
  - `REACT_APP_API_URL`: URL of the backend API

## 🎉 Usage

Once set up, you can:
1. Create different types of chatbots through the admin interface.
2. Customize each bot's settings and personality.
3. Chat with your bots through the React frontend.
4. Manage conversations and bot behaviors via the Django admin panel.

## 🤝 Contributing

We love contributions! If you'd like to improve Mochi Bot, please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📬 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

## 📜 License

[Add your license information here]

---

Enjoy your Mochi Bot! May your conversations be as sweet and satisfying as a perfectly made mochi! 🍡💬