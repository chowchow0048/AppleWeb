# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AppleWeb is a Django-based academy management system for Apple Science academy. It's a Korean language web application that manages students, courses, attendance, reviews, and administrative tasks.

## Architecture

**Main Django Apps:**

- `common/` - User authentication, shared models (User, Course, Attendance, Review)
- `main/` - Public-facing pages and home functionality
- `community/` - Community features and notices
- `management/` - Administrative interface for teachers/managers

**Key Models:**

- `User` (AbstractUser) - Students and staff with roles (teacher, manager)
- `Course` - Class schedules with subjects, rooms, times
- `Attendance` - Student attendance tracking
- `Review` - Student reviews with images and importance levels

## Common Development Commands

### Django Commands

```bash
# Navigate to Django project directory
cd appleWeb/

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

### Environment Settings

- Development: `config.settings.local`
- Production: `config.settings.prod`
- Railway deployment: `config.settings.railway` (referenced in deployment docs)

### Frontend Assets

- CSS files in `static/css/` organized by app
- JavaScript files in `static/scripts/` organized by app
- Images in `static/images/`
- Templates in `templates/` organized by app

## Key Features

- Multi-role user system (students, teachers, managers)
- Course scheduling and room management
- Attendance tracking with date filtering
- Student reviews with image uploads
- Administrative dashboards
- Korean localization (TIME_ZONE: Asia/Seoul)

## Dependencies

- Django 5.0.2 with CKEditor 5 for rich text editing
- APScheduler for background task scheduling
- Frontend uses vanilla JavaScript (no major frameworks)
- Database: SQLite (development), PostgreSQL (production/Railway)

## Deployment

Railway deployment is documented in RAILWAY_DEPLOYMENT_GUIDE.md with PostgreSQL database migration from AWS Lightsail.

## Rules for Claude agent

1. answer in Korean
