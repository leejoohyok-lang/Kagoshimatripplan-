name: Update Kagoshima Weather

on:
  schedule:
    # 19:00 UTC = 04:00 KST (Asia/Seoul & Asia/Tokyo) the next day
    - cron: '0 19 * * *'
  workflow_dispatch: {}   # allows manual "Run workflow" from the Actions tab

permissions:
  contents: write

jobs:
  update-weather:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Fetch latest weather and write weather.json
        run: python3 scripts/update_weather.py

      - name: Commit and push if weather.json changed
        run: |
          git config user.name "weather-bot"
          git config user.email "actions@users.noreply.github.com"
          git add weather.json
          if git diff --cached --quiet; then
            echo "No weather changes, skipping commit."
          else
            git commit -m "chore: update weather data ($(date -u +'%Y-%m-%d %H:%M UTC'))"
            git push
          fi

