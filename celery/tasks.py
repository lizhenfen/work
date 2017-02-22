from celery import  Celery


app = Celery('tasks', backend="'redis://192.168.15.2:6379/0",broker='redis://192.168.15.2:6379/0')
app.config_from_object('config')
@app.task
def add(x,y):
    return x+y


if __name__ == "__main__":
    pass