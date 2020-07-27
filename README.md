# Rest API for ACME Company
API to create Store, Order, Payment and check or update its values. Must fix some security vunerabilties, logical and code problems. New feature coming soon.
Version: 3.4 (everything from 2.5 is actually beta)
### Documentation:
The API documentation is a *Swagger UI Live documentation generated by Swagger 2.0*. You can open the Swagger generated documentation UI from:
[ http://localhost:8080/ui](http://localhost:8080/ui) (Your API URL then /ui)

### How to run:
#### Using Python in terminal:
Make sure that Python >= 3.6, and all resources is installed then clone or download this repo and inside the project directory run:

>python3 app.py

#### Run using Docker:

>docker build -t acme-api-3.4 .

>docker run -dp 8080:8080 acme-api-3.4

### Demo Image of the Swagger UI:
If not displaying, open the file: [SwaggerUI.pdf](https://github.com/tonykingnz/RestAPIACMECompany/blob/master/SwaggerUI.pdf)

![Swagger UI Demo Image](SwaggerUI.pdf)

###### based on https://github.com/invillia/backend-challenge

###### last updated: 2020-07-25 14:44:50 (UTC -3)
