FROM continuumio/miniconda3

# Update packages and install nano and curl
RUN apt-get update -y && apt-get install nano curl -y

# This part is specific to Hugging Face Space
    # We create a new user named "user" with ID of 1000
    # We switch from "root" (default user when creating an image) to "user"
RUN useradd -m -u 1000 user
USER user

# We set two environnement variables
# so that we can give ownership to all files in there afterwards
# we also add /home/user .local/bin in the $PATH environment variable
# PATH environment variaable sets paths to look for installed binaries
# We update it so that Linux knows where to look for binaries if we were to install them with "user"

ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH

# We set working directory to $HOME/app (<=> /home/user/app)
WORKDIR $HOME/app

# Copy all local files to /home/user/app with "user" as owner of these files
# Alays use --chown=user when using HUGGING FACE SPACE to avoid permission errors
COPY --chown=user . $HOME/app

# Install all dependencies
RUN pip install -r requirements.txt

# Run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]