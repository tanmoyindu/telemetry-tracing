# telemetry-tracing

A simple FastAPI ecommerce example demonstrating telemetry tracing using OpenTelemetry and Jaeger.

## Overview

This project shows how to instrument a FastAPI application with OpenTelemetry to collect distributed traces and export them to a Jaeger backend for visualization and analysis.

## Features

- FastAPI backend with simple product endpoints
- OpenTelemetry tracing setup with Jaeger exporter
- Dockerized for easy deployment of app and Jaeger all-in-one
- Example of tracing spans for API calls

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- (Optional) Python 3.11+ if running locally without Docker

## This starts both the FastAPI app and Jaeger UI.

FastAPI API: http://localhost:8000

Jaeger UI: http://localhost:16686

### Running with Docker Compose

```bash
docker-compose up --build
