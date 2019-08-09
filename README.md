# ${1:Greengen}
Greengen is a python package that allow implementing generators without yielding items all the way up.
Instead, any inner function called from a greengen generator, can yield items directly to the outer generator.
See [Usage](#usage)
## Installation
```
pip install greengen
```
## Usage
For example, suppose we want to implement a function that performs some heavy business logic, and generates logs.
We want to handle the logs the moment they are created.
But our functions has to call a deep stack of helper functions, which in their turn call more functions,
and logs may be written anywhere inside any function.
The implementation with regular generators will be utterly annoying:
```python
import time


def do_business_logic_and_yield_logs(some_input):
    yield from _helper_function(some_input)
    yield from _more_helper_function(some_input)


def _helper_function(some_input):
    for i in range(some_input):
        logs_and_result = _inner_helper_function(i)
        # Notice the enormous effort needed in order to retrieve the last result (using StopIteration etc.)
        while True:
            try:
                yield next(logs_and_result)  # This is a log
            except StopIteration as e:
                result = e.value  # This is the result
                yield log('Result for {} is {}'.format(i, result))
                break


def _more_helper_function(some_input):
    yield from _helper_function(some_input * 100)
    yield from _helper_function(some_input ** 2)


def _inner_helper_function(some_input):
    yield log('Started calculating')
    result = 2 ** some_input  # (Or whatever other heavy calculation)
    yield log('Finished calculating')
    return result  # Will be raised as StopIteration


def log(stuff):
    return {'message': str(stuff), 'timestamp': time.time()}


def main():
    for l in do_business_logic_and_yield_logs(42):
        # Consume the logs however we want
        print('{}: {}'.format(l['timestamp'], l['message']))
```
Using Greengen, this example can be changed into the following:
```python
import time
import greengen

@greengen.greengen
def do_business_logic_and_yield_logs(some_input):
    # Notice how we don't need the "yield from" anymore
    _helper_function(some_input)
    _more_helper_function(some_input)


def _helper_function(some_input):
    for i in range(some_input):
        # Notice how easy it is to retrieve the result now
        result = _inner_helper_function(i)
        log('Result for {} is {}'.format(i, result))


def _more_helper_function(some_input):
    _helper_function(some_input * 100)
    _helper_function(some_input ** 2)


def _inner_helper_function(some_input):
    log('Started calculating')
    result = 2 ** some_input  # (Or whatever other heavy calculation)
    log('Finished calculating')
    return result


def log(stuff):
    # This is the only place in the entire code where we use "yield".
    # This will directly yield the log as the next item in the outer generator ("do_business_logic_and_yield_logs")
    greengen.yield_({'message': str(stuff), 'timestamp': time.time()})


def main():
    for l in do_business_logic_and_yield_logs(42):
        # Consume the logs however we want
        print('{}: {}'.format(l['timestamp'], l['message']))
```
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
## History
TODO: Write history
## Credits
TODO: Write credits
## License
TODO: Write license