# E-Commerce Backend System

Production-ready Django REST Framework backend for an e-commerce platform.

## Overview

- Multi-role users: Customer, Vendor, Admin
- Product catalog with categories, search, filtering, image uploads
- Shopping cart with add/remove/update
- Order checkout from cart with stock validation
- Simulated payment processing
- Signal-driven notifications on order events
- JWT authentication with role-based access control
- Cached product listings for performance

## Tech Stack

- Django 5.x + Django REST Framework
- PostgreSQL
- SimpleJWT for authentication
- django-filter for queryset filtering
- Django cache framework (LocMem)
- Gunicorn for production serving
- Docker + Docker Compose


## API Endpoints

Base: `/api/v1/`

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register customer or vendor |
| POST | `/auth/login/` | Get JWT access token |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List products (public) |
| POST | `/products/` | Create product (vendor) |
| GET | `/products/{id}/` | Product detail |
| GET | `/categories/` | List categories |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cart/` | View cart |
| POST | `/cart/items/` | Add/update cart item |
| DELETE | `/cart/items/` | Remove cart item |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders/` | Checkout (creates order from cart) |
| GET | `/orders/` | List user orders |
| PATCH | `/orders/{id}/status/` | Update status (admin) |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/pay/` | Pay for an order |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notifications/` | List notifications |
| PATCH | `/notifications/read-all/` | Mark all as read |

## Setup

1. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```

2. Copy and configure environment:
   ```bash
   copy .env.example .env
   ```

3. Create PostgreSQL database:
   ```sql
   CREATE DATABASE ecommerce_db;
   ```

4. Run migrations:
   ```bash
   py manage.py makemigrations
   py manage.py migrate
   ```

5. Create admin user:
   ```bash
   py manage.py createsuperuser
   ```

6. Run server:
   ```bash
   py manage.py runserver
   ```

## Docker

```bash
docker-compose up --build
```

## Design Decisions

- **Modular apps** for clean separation: each domain concern is isolated
- **Role-based permissions** (Customer/Vendor/Admin) via custom permission classes
- **Cart-to-order checkout** with atomic stock deduction to prevent overselling
- **Django signals** for decoupled notification creation on order events
- **Cached product listings** to reduce DB load on high-traffic catalog pages
- **Split settings** for safe local development vs hardened production config
- **JWT access token** for simple, stateless auth (single token per login)
