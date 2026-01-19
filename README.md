# Travel Itinerary Optimizer

An intelligent application that scrapes top travel websites and creates optimal itineraries for couples, optimizing for both cost and time.

## Features

- Scrapes data from top 10 travel websites
- Extracts flights, hotels, and activities
- Optimizes itinerary for cost and time
- Generates detailed itinerary for couples

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Local Development

**Command Line:**
```bash
python main.py
```

**Web Interface (Flask):**
```bash
python app.py
```
Then visit `http://localhost:5000`

**Netlify Dev (Recommended for testing Netlify deployment):**
```bash
npm install -g netlify-cli
netlify dev
```

### Deployment

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions to Netlify.

## Configuration

Edit `config.py` to customize:
- Travel websites to scrape
- Optimization weights (cost vs time)
- Default search parameters
