# Life-GPS Flutter Makefile
# Usage: make <target>

FLUTTER := C:/src/flutter/bin/flutter
PROJECT := .

.PHONY: help run test analyze build web clean gen deps doctor

help:
	@echo ""
	@echo "Life-GPS Flutter Developer Commands"
	@echo "====================================="
	@echo "  make run       - Start dev server"
	@echo "  make test      - Run all tests with coverage"
	@echo "  make analyze   - Run flutter analyze"
	@echo "  make build     - Build release APK"
	@echo "  make web       - Build web release"
	@echo "  make clean     - Clean + pub get"
	@echo "  make gen       - Run code generation"
	@echo "  make deps      - Fetch dependencies"
	@echo "  make doctor    - Flutter doctor"
	@echo ""

run:
	$(FLUTTER) run --dart-define=APP_ENV=development

test:
	$(FLUTTER) test --coverage

analyze:
	$(FLUTTER) analyze

build:
	$(FLUTTER) build apk --release --dart-define=APP_ENV=production

web:
	$(FLUTTER) build web --dart-define=APP_ENV=production

clean:
	$(FLUTTER) clean && $(FLUTTER) pub get

gen:
	$(FLUTTER) pub run build_runner build --delete-conflicting-outputs

deps:
	$(FLUTTER) pub get

doctor:
	$(FLUTTER) doctor -v
