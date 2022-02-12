### Сборка образа

```
docker build -t stocks_products .
```

### Запуск контейнера

```
docker run -d -rm -p 8000:8000 --name my_stocks stocks_products
```
