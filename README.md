## Homework Application: URL Shortener and Decoder

Diego Andres Torres Guarin 22202528


Instructions:
 1. Run `docker compose up` in this directory
 2. Go to http://0.0.0.0:8000/docs
 3. Try the different endpoints to create/retrieve/delete new urls and get the statistics


 Details of the application:
 - I validate the *user_email* field to be an actual email
 - To get the long URL I ask for the hash only, not the new short URL
 - When you delete a URL, the count for the creator of the URL goes down, so we only consider the active ones when computing the URL count of the users.