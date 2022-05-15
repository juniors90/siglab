# API REST en Flask

```cmd
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"aanu","email":"aanu@gmail.com","password":"dontleaveme"}' http://127.0.0.1:5000/api/register
```

```cmd
curl -u aanu:dontleaveme -i -X GET http://127.0.0.1:5000/api/dothis
```

```cmd
curl -u aanu:leaveme -i -X GET http://127.0.0.1:5000/api/dothis
```

```cmd
curl -u aanu:dontleaveme -i -X GET http://127.0.0.1:5000/api/login
```

```cmd
curl -u eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjUyNTgwMDE5LjE2NDc2Mzd9.eLN4al6tLushV2DM1Cjll8v5DysOPZYjjnVPotrvGps:notrelevant -i -X GET http://127.0.0.1:5000/api/dothis
```

```cmd
curl -u aanu:dontleaveme -i -X GET http://127.0.0.1:5000/api/movies
```

## COMO FUNCIONA PyJWT

```cmd
>>> import jwt
>>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
>>> print(encoded_jwt)
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
>>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
{'some': 'payload'}
```

## PROPAGATE_EXCEPTIONS:

- [Para propagar las excepciones y poder manejarlas a nivel de aplicación.](https://stackoverflow.com/questions/59680787/setting-propagate-exceptions-to-true-is-not-re-raising-exception-in-flask-produc)