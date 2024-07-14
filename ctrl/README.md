这个是后端的package

注意，事实上，前端仅需要阅读的代码在`handler.py`,`mission.py`和`request.py`
三个文件中

这个函数是前端唯一需要调用的函数，使用这个函数，你需要提供一个`Request`对象，并在`Request`对象中填充好对应的成员变量
```python
from ctrl.handler import dispatch
```

