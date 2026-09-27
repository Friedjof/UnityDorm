# UnityDorm 🌐

UnityDorm is a simple landing page and blog platform designed as a central hub for community members. Users can create "shortcuts" displayed as small icons in the upper section to quickly access frequently used links. Additionally, there is a feature for writing and publishing blog articles.

> **Note**: This is in development and may have bugs or incomplete features. Feel free to contribute to the project by submitting pull requests or issues.

## Features ✨

### 1. Shortcuts 🚀
- **Description**: Shortcuts are small icons in the upper section of the page, serving as quick links to external resources.
- **Customization**: Each shortcut can have a title, an image, and a link that can open in a new tab.
- **Purpose**: Shortcuts provide easy access to frequently used links for the community and offer a clear structure.

### 2. Blog Articles 📝
- **Description**: Users can write and publish blog articles organized into various categories.
- **Customization**: Blog articles have a title, a short description, and detailed content. An image and a category can be added for each post.
- **Purpose**: The blog feature provides a platform for sharing news, opinions, or other content with the community.

> **The article text** can be written in Markdown format, allowing for easy formatting and styling. Then the content is rendered as HTML on the frontend.

## Screenshots 📸

<table>
  <tr>
    <td><img src="media/screenshots/demo-home.png" alt="Homepage" width="300"/></td>
    <td><img src="media/screenshots/demo-article-top.png" alt="Article" width="300"/></td>
    <td><img src="media/screenshots/demo-admin-panel-articles.png" alt="Admin" width="300"/></td>
  </tr>
</table>

_This screenshot shows the homepage with shortcuts and blog articles, an article with detailed content, and the admin panel for managing articles._

## Installation ⚙️

1. Clone the repository:
   ```bash
   git clone https://github.com/Friedjof/UnityDorm.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## `.env` Configuration 🛠️
```bash
DJANGO_SECRET_KEY='<your_secret_key>'          # Generate a new secret key
DJANGO_DEBUG='False'                           # Use 'True' only for local development
DJANGO_ALLOWED_HOSTS='<your_domain>,localhost' # Add your domain here (comma-separated values)
DJANGO_CSRF_TRUSTED_ORIGINS='https://<your_domain>'
DJANGO_SUPERUSER_USERNAME='<your_username>'    # Create a superuser with these credentials
DJANGO_SUPERUSER_EMAIL='<your_email>'          # (for accessing the admin interface)
DJANGO_SUPERUSER_PASSWORD='<your_password>'    # (use a strong password)
TLS_ACTIVE='True'                              # Set to 'False' to disable HTTPS
DJANGO_TRUST_PROXY_PROTO='True'                # When a trusted proxy terminates TLS
DJANGO_SECURE_SSL_REDIRECT='True'              # Redirect HTTP to HTTPS
DJANGO_SECURE_HSTS_SECONDS='31536000'           # Enable only after HTTPS is verified
```

## Docker 🐳

You can use the prebuilt Docker image from the GitHub Container Registry:

```bash
docker pull ghcr.io/friedjof/unitydorm:latest
```

Here is an example `docker-compose.yml` configuration:
```yaml
services:
  unitydorm:
    image: ghcr.io/friedjof/unitydorm:latest
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SECRET_KEY='<your_secret_key>'
      - DJANGO_DEBUG='False'
      - DJANGO_ALLOWED_HOSTS='<your_domain>,localhost'
      - DJANGO_SUPERUSER_USERNAME='<your_username>'
      - DJANGO_SUPERUSER_EMAIL='<your_email>'
      - DJANGO_SUPERUSER_PASSWORD='<your_password>'
      - TLS_ACTIVE='True'
      - DJANGO_TRUST_PROXY_PROTO='True'
      - DJANGO_SECURE_SSL_REDIRECT='True'
    volumes:
        - ./data:/data
        - ./uploads:/uploads
    restart: always
```

## Usage 🖥️

- **Admin Interface**: The admin interface allows you to manage shortcuts and blog articles. Log in at `/admin` to add shortcuts or create and edit blog articles.
- **Homepage**: The homepage displays a list of shortcuts and blog articles. Users can access relevant content through the links in the header section.

Uploaded images are converted on demand into cached, responsive WebP sizes. In production,
serve `/media/` directly from a reverse proxy or object storage when possible; the Django
fallback includes long-lived caching for generated derivatives.

## Makefile Commands 🛠️

Here are the available `make` commands for the project:

- **migrations**: Creates new migration files.
- **migrate**: Runs database migrations.
- **requirements**: Updates `requirements.txt` with the current dependencies.
- **build**: Builds the Docker image without cache.
- **up**: Starts the Docker container.
- **down**: Stops the Docker container.
- **logs**: Shows logs of the Docker container.
- **restart**: Stops and restarts the container.
- **demo**: Runs `build` and `up` in sequence.
- **clean**: Stops the container and cleans up unused Docker images.
- **release**: Creates a new release version (including Git tagging and push).
- **version**: Updates `version.txt` with the latest Git tag.
- **admin**: Creates a new Django superuser.
- **shell**: Starts the Django shell.

## Contributing 🤝

Contributions are welcome! Feel free to submit a pull request if you have any improvements or new features to suggest.

## License 📜

This project is licensed under the GPL-3.0 license. For more details, see the [LICENSE](LICENSE) file.

---

Enjoy using UnityDorm! 🎉
