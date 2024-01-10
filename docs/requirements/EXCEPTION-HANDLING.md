# LMS Toolkit - Exception Handling and Logging

## Exception Handling

### Web Service Calls

* Covers 4xx and 5xx HTTP response codes.
* Automatic retry on error (configurable number of attempts, default to
  (4 ![(question)](/s/-30dpkv/9012/1ca6q62/_/images/icons/emoticons/help_16.svg))
* On Xth attempt failure should be thrown as an exception that will bubble up to
  the calling program (e.g. the main user interface). For example, error occurs
  on the fourth try, then don't try a fifth time.
* Throw a `RuntimeError` based on the caught exception. Example:

   ```python
    try:
        a = 1 / 0
    except Exception as ex:
        raise RuntimeError("This bad thing happened") from ex
    ```

* Once logging is in scope
    * WARN log on each initial failure
    * ERROR log on final failure

## Logging

### Framework

The logs will be generated with the [logger from the Python Standard
Library](https://docs.python.org/3/library/logging.html).

Reasons for this choice:

* It has [built-in logging
  levels](https://docs.python.org/3/library/logging.html#logging-levels) (Debug,
  Info, Warning, Error, Critical).
* You can [configure the log
  level](https://docs.python.org/3/library/logging.html#logging.Logger.setLevel)
  that you want to see in your log output (DEBUG, WARNING).
* You can configure the output for your logs by defining a [logging
  handler](https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers):
  log to console, log to a file, or even separate files by dates if is what is
  needed. **Note: if you don't need any specific logger, you can leave it as it
  is and it will log to the standard output device (probably the terminal
  window).**
* There is a big chance that the external libraries will use this standard
  logger.
* Output format: you can define as much data as you consider is useful and
  format it as required for your logs. For example: **'%(asctime)s -
  %(levelname)s - %(user)s - %(message)s'**
* If you want to have a very detailed level of logging when debugging, even if
  you want to call expensive functions such as getting the user name, but you
  don't want to impact performance in production, you can do something like
  this:

  ```python
  if logger.isEnabledFor(logging.INFO):
      logger.debug('%s', expensive_func())
  ```

* We could define the handler and log level configuration from our .env
  variables, and then move it to command line parameters.

### Logging Format

The minimum level of detail could be something like:

`'%(asctime)s - %(levelname)s -  %(message)s'``

You can declare it in your code like this:

```python
import logging
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('All requests were made successfully')
```

The response would be something like

```none
2020-09-17 17:44:10,276 - INFO - All requests were made successfully
```

### Criteria for Log Levels

The logger has 5 different levels: debug, info, warning, error, critical.

#### DEBUG

Could be used to track how much time some tasks are taking. Examples:

* Start loading .env variables / Finished loading .env variables.
* Start request to(courses/students/assignments...) / finished request.

#### INFO

Similar to debug. It should register the beginning or end of important methods
that could potentially fail. Examples:

* Started / finished writing csv files.
* Validate required .env variables are present.

#### WARNING

Events that does not stop the code from working but could potentially fail or
have undesired effects. Examples:

* A request that took more time than expected.
* The server responded a request with a code different than 200 but did not fail
  (a redirect for example).
* When generating the csv files, a file has been overwritten.

#### ERROR

Expected errors in code that break the execution but (most of them) could be
solved. Examples:

* The LMS initial path is not valid.
* The output path for the generated csv is too long.
* Some required values were not set in the .env file.
* The .env file was not found.
* Errors when writing files: Path does not exist, not enough permissions, the
  server run out of storage.

#### CRITICAL

Unexpected errors in code that break the execution.

* No internet connection.
* A request gets a server error/resource not found/... response.
* External libraries' critical exceptions.
