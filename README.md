# CohabGrid - Roommate Recommendation System

This project is a full-stack Roommate Recommendation System with automated deployment. The application is built using Streamlit, offering an interactive interface for users to input preferences and receive matches. The backend logic implements a KNN model to process these inputs, and also handles data storage and matching with modules like Pandas and NumPy.

The app is containerized with Docker for environment consistency and easy deployment. A Jenkins CI/CD pipeline automates the workflow—cloning the GitHub repository, building the Docker image, and pushing it to Docker Hub.

This setup showcases an end-to-end DevOps pipeline for a modern web application.

