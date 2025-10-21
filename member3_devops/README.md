# Member 3 - DevOps Engineer

Work here on Docker, testing enhancements, and CI/CD.

Initial scope implemented:
- Dockerfile builds the Flask app
- GitHub Actions runs tests and builds image
- docker-compose.yml for local up

Suggested next tasks:
- Configure Docker Hub push (add repo secrets, uncomment steps in workflow)
- Add test coverage report (pytest-cov) and upload artifact/badge
- Enable dependency caching in Actions (pip cache, buildx cache)
- Consider multi-stage Docker builds or distroless for smaller images
