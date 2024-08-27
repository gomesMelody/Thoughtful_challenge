from robocorp.tasks import task
from main import *
@task
def minimal_task():
    search_latimes(search_phrase="covid", period=2)
