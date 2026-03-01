name: Build APK
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install flet
        run: pip install flet
      
      - name: Setup Flutter (автоматически)
        run: |
          # Автоматически принимаем установку Flutter
          yes | flet build apk || true
      
      - name: Build APK
        run: |
          # Сборка APK
          flet build apk --no-publish
      
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: app
          path: |
            build/apk/**/*.apk
            *.apk
