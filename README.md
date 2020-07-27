# Rest API for ACME Company
Currently, only the Store API is made.  Order and Payment must be developed. (https://bit.ly/trelloRestAPIACMECompanyListAsJul182020)

### Documentation:
The API documentation is a *Swagger UI Live documentation generated by Swagger 2.0*. You can open the Swagger generated documentation UI from:
[ http://localhost:8080/ui](http://localhost:8080/ui) (Your API URL then /ui)

### How to run:
#### Using Python in terminal:
Make sure that Python >= 3.6 is installed then clone or download this repo and inside the project directory run:

>python3 app.py

#### Run using Docker:

>docker build -t store-api-2.2 .

>docker run -dp 8080:8080 store-api-2.2

### Demo Image of the Swagger UI:
If not displaying, open the file: [SwaggerUI.pdf](https://github.com/tonykingnz/RestAPIACMECompany/blob/master/SwaggerUI.pdf)

![Swagger UI Demo Image](SwaggerUI.pdf)
