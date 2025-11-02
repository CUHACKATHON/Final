# MoodLift - Mental Health Support Platform

A comprehensive digital mental health and support system tailored for Indian college students. Built with Django, this platform provides anonymous chat support, appointment booking, educational resources, peer support forums, and an admin dashboard with analytics.

## Features

### 1. **Anonymous Chat Support (24/7)**
- Completely anonymous interface - no registration required
- AI-powered chatbot with psychiatrist perspective using OpenAI GPT-4
- Evidence-based psychiatric support with clinical empathy
- Crisis detection and immediate helpline referrals
- Session-based conversation history
- Sentiment analysis and emotion detection

### 2. **Professional Counseling Appointments**
- Book confidential appointments with verified counselors
- Anonymous booking option
- Appointment management system for counselors/admins
- Status tracking (pending, confirmed, completed, cancelled)

### 3. **Educational Resources**
- Videos, guided meditations, and articles
- Multi-language support (English, Hindi, Tamil, Telugu, Kannada, Marathi)
- Filter by type and language
- Culturally contextualized content

### 4. **Peer Support Forum**
- Anonymous posting and replies
- Moderation system for content safety
- Thread-based discussions
- Community support

### 5. **Admin Dashboard**
- Real-time analytics and statistics
- Trend charts (sessions, anxiety/depression keywords)
- Appointment management
- Forum moderation queue
- Keyword analysis

## Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (default, can be switched to PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Charts**: Chart.js

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd Final
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   
   Create a `.env` file in the project root directory:
   ```bash
   # Django Secret Key (optional, has default for development)
   SECRET_KEY=your_secret_key_here
   
   # Debug mode (optional, defaults to True for development)
   DEBUG=True
   
   # OpenAI API Key (Primary - Psychiatrist Perspective)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Google Gemini API Key (Optional Fallback)
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **To get an OpenAI API key:**
   1. Visit https://platform.openai.com/
   2. Sign up or log in
   3. Go to API Keys section
   4. Create a new API key
   5. Copy and paste it into your `.env` file
   
   **Note:** The chat will use Gemini as a fallback if OpenAI is not configured, but OpenAI is recommended for best psychiatrist-perspective responses.

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user. Make sure to set the role to 'admin' in the Django admin panel after creation.

7. **Create sample counselors (optional)**
   You can create counselor accounts through Django admin or use the shell:
   ```bash
   python manage.py shell
   ```
   ```python
   from core.models import CustomUser
   user = CustomUser.objects.create_user(
       username='counselor1',
       password='your_password',
       role='counselor',
       email='counselor1@example.com'
   )
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login: http://127.0.0.1:8000/login/

## Usage Guide

### For Students (Anonymous Users)

1. **Start Chatting**
   - Navigate to `/chat/`
   - Begin chatting anonymously - no login required
   - Your session is automatically tracked via browser localStorage

2. **Book Appointment**
   - Go to `/appointments/`
   - Select a counselor and preferred date/time
   - Optionally share what you'd like to discuss

3. **Browse Resources**
   - Visit `/resources/`
   - Filter by type (video/meditation/article) and language
   - Access educational content

4. **Join Forum**
   - Go to `/forum/`
   - Create anonymous posts or reply to existing threads
   - Posts require moderation before appearing publicly

### For Admins/Counselors

1. **Login**
   - Go to `/login/`
   - Use your admin/counselor credentials

2. **Dashboard**
   - View analytics and statistics at `/dashboard/`
   - Monitor trends, appointments, and forum activity

3. **Manage Appointments**
   - Access `/appointments/manage/`
   - Update appointment statuses
   - View all appointments

4. **Moderate Forum**
   - Go to `/forum/moderate/`
   - Approve or delete posts/replies
   - Maintain content quality

5. **Django Admin**
   - Access `/admin/` for full database management
   - Manage users, resources, analytics, etc.

## Project Structure

```
Final/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── mentalhealth/            # Main Django project
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── ...
├── core/                     # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin configuration
│   ├── utils/
│   │   └── chatbot_logic.py # Chatbot logic
│   └── migrations/          # Database migrations
├── static/                  # Static files
│   ├── css/style.css       # Main stylesheet
│   ├── js/                 # JavaScript files
│   └── assets/             # Media files
└── templates/             # HTML templates
    ├── base.html           # Base template
    ├── index.html          # Landing page
    ├── chat.html           # Chat interface
    └── ...
```

## Key Features Implementation

### Anonymous Session Management
- Uses UUID-based session IDs stored in browser localStorage
- No user authentication required for chat/forum
- Sessions are linked but users remain anonymous

### Chatbot Logic (AI-Powered Psychiatrist Perspective)
- **Primary**: OpenAI GPT-4 integration for psychiatrist-perspective responses
  - Clinical empathy and professional validation
  - Evidence-based therapeutic techniques (CBT, mindfulness, grounding)
  - Psychoeducation about mental health conditions
  - Gentle clinical questioning and assessment
  - Professional referral guidance
- **Fallback**: Google Gemini API for continued support if OpenAI unavailable
- Rule-based intent recognition
- Crisis detection with immediate helpline referrals
- Sentiment analysis and emotion detection
- Context-aware responses with conversation history

### Analytics
- Daily aggregation of sessions, keywords, appointments
- Trend analysis over time
- Keyword tracking (anxiety, depression)
- Exam season spike detection capability

## Emergency Helplines

If you or someone you know is in crisis, please contact:

- **National Mental Health Helpline**: 1800-599-0019 (24/7)
- **Aasra Suicide Prevention**: +91-9820466726
- **iCall**: +91-9152987821

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in your `.env` file or `settings.py`
2. Configure `ALLOWED_HOSTS` in `settings.py`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up SSL/HTTPS
6. Use environment variables for sensitive data (SECRET_KEY, API keys, etc.)

## Contributing

This is a hackathon project. For improvements:

1. Ensure code follows Django best practices
2. Add comments for complex logic
3. Test all features before deployment
4. Follow the existing code style

## License

This project is created for educational/hackathon purposes.

## Support

For issues or questions, please refer to the Django documentation or contact the development team.

---

**Built with ❤️ for Indian College Students' Mental Health**
