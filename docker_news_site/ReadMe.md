News site project

Written on Python 3.8 using Django,
djangorestframwork. Connected PostgreSQL.
Also project was dockerezied and depolyed on
Heroku. Workflow - ubuntu 18.04

To run this up in your terminal
1. Create docker
`sudo docker-compose build`
2. Migrate database `sudo docker-compose run web python news_site/manage.py migrate
`
3. Start docker `sudo docker-compose up`

About URLS you can read at: `https://web.postman.co/collections/11430788-305d8a7c-c1aa-4c93-96f7-bbcb9786c041?version=latest&workspace=e692dced-eba2-4bc1-8f5e-29b4f3387fac`
