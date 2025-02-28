"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def add(*args):
  """ Returns a STRING with the sum of the arguments """ 
  sum = 0
  for number in args:
    sum += int(number) 
  
  content = """
  <h1>{}</h1>
  """.format(sum)
  return content
  
def multiply(*args):
  product = 1

  for number in args:
    product *= int(number)
  
  content = """
  <h1>{}</h1>
  """.format(product)
  return content

def divide(*args):
  # Take the arguments and place them into a list
  numbers = []
  for number in args:
    numbers.append(int(number))
  
  # Try to divide them by one another
  try:
    quotient = numbers[0] / numbers[1]
    content = """
    <h1>{}</h1>
    """.format(quotient)
    return content
  except ZeroDivisionError:
    content = """
    <h1>You Cannot Divide By Zero!</h1>
    """
    return content
  
  content = """
  <h1>{}</h1>
  """.format(quotient)
  return content

def subtract(*args):
  # Place the arguments into a list
  numbers = []
  for number in args:
    numbers.append(int(number))

  # Subtract the difference of the two numbers.
  difference = numbers[0] - numbers[1]
  
  content = """
  <h1>{}</h1>
  """.format(difference)
  return content

def Home():
  content = """
  <h1>Home</h1>
  <body>
  <br>Welcome to the WSGI Server Calculator.
  <br>This Calculator will resovle the URL to perform a mathematical
  operation and return the result to the screen. This is how you should
  provide the Data:

  <br>[function]/[first_operand]/[second_operand]
  
  <li>add: Adds Both of the Operands </li>
  <li>Subtract: Subtracts the Second Provided Operand with the first</li>
  <li>Multiply: Multiplies Both Operands</li>
  <li>Divide: Divides the First Operand by the Second</li>
  
  </body>
  """
  return content
# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # Create a dicionary to map the functions to the requested
    # Function.
    funcs = {
      '': Home,
      'add': add,
      'subtract': subtract,
      'multiply': multiply,
      'divide': divide,
    }

    # This will strip the provided path of it's right most
    # '/' and then split it on the remaining '/'
    path = path.strip('/').split('/')

    # Slice the list for the base function and arguments
    func_name = path[0]
    args = path[1:]


    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    func = funcs[func_name]
    args = args

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
