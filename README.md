# Page Analyzer

[![Actions Status](https://github.com/tatapestova/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/tatapestova/python-project-83/actions)
[![Python CI](https://github.com/tatapestova/python-project-83/actions/workflows/github-actions.yml/badge.svg)](https://github.com/tatapestova/python-project-83/actions/workflows/github-actions.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/da9f39d48d317f0427d9/maintainability)](https://codeclimate.com/github/tatapestova/python-project-83/maintainability)
***
click to try [Page analyzer](https://python-project-83-production-d957.up.railway.app/)

Page Analyzer is a site that analyzes specified pages for SEO suitability.

![Main page](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImE3YzdlNTIwNTc5Y2FjYjhlZTI3NmE1YWNkMzAwZDA0LnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=649161c5471aae452572ce231ec1c1d8247f36b39f4f6f3ef0f36a64f04495a8)

![List of urls](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjEwMzBhMTIwMDEwYTgzMDk5ODQxZTk3YmQ0ZTA1MmQyLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=d679a4d7ebb40a9850af2b0d04afe128dc536277228fdd4b771043acc2664129)

![Details of url](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjYzNTBmODFkZjZmMDQ5YWFhNGI3MGU2MDg5Mjc2MGVlLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=ce17f5a7aa6dcb665396ccabea0fd5b0d399bb2d806f43e7f3eddc61122c1fc4)

### For local deployment
1. Clone repository.
```
git clone https://github.com/tatapestova/python-project-83.git
```
2. Add dependencies
```
make install
```
3. Set up DATABASE_URL and SECRET_KEY in the new .env file. and place it in the root of the project. 
4. There are instructions for create tables in the database in the file database.sql.
5. Then this command will be available for local deployment.
```
make dev
```
