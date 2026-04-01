# Health Risk Prediction System

A modern Flask web application for predicting health risks based on vital signs and displaying analytics.

## Features

- Health risk assessment based on heart rate, blood pressure, sugar levels, temperature, oxygen saturation, and cholesterol
- Real-time dashboard with analytics and charts
- Patient record management (search, delete)
- Live health monitoring simulation
- Modern dark theme UI

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser

## Deployment

### Heroku Deployment (Recommended)

1. **Install Heroku CLI** (if not already installed):
   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

4. **Deploy to Heroku**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open your deployed app**:
   ```bash
   heroku open
   ```

### Alternative Deployment Options

#### Railway
1. Connect your GitHub repository to Railway
2. Railway will automatically detect Flask and deploy

#### Render
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`

## Project Structure

```
healthrisk/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment configuration
├── runtime.txt           # Python version specification
├── static/               # CSS and generated images
│   └── style.css
├── templates/            # HTML templates
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   ├── search.html
│   ├── delete.html
│   └── live.html
└── patients.csv          # Patient data (generated)
```

## Technologies Used

- **Backend**: Flask (Python)
- **Data Processing**: Pandas
- **Visualization**: Matplotlib
- **Frontend**: HTML, CSS
- **Deployment**: Heroku/Railway/Render

## License

This project is open source and available under the MIT License.