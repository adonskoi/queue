# queue



###### ```POST '/' ```

Create new task

Response:

```
{
 "id": 1
}
```



###### ```GET '/<id>' ```

Response:

```
{
  "create_time": 1602444301.577321,
  "start_time": 1602444301.579627,
  "status": "Completed", // "In Queue", "Run"
  "time_to_execute": 1602444311.586422
}
```