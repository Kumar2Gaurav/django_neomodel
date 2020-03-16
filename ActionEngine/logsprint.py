import time
import logging
logname="logsfile"
logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.DEBUG)

def entryExit(aFunc):
    """Trace entry, exit and exceptions."""

    def loggedFunc(*args, **kw):
        logging.info('*********************')
        logging.info('enter In Function : {} at {} '.format(aFunc.__name__, str(time.strftime('%I:%M:%S %p'))))
        try:
            result = aFunc(*args, **kw)
            logging.info("These are the arguments {} and results {}".format(args, result))
        except Exception as e:
            logging.warning('exception in {}  and {}'.format(aFunc.__name__, e))

        logging.info('exit from Function : {} at {} '.format(aFunc.__name__, str(time.strftime('%I:%M:%S %p'))))
        logging.info('*********************')
        return result

    loggedFunc.__name__ = aFunc.__name__
    loggedFunc.__doc__ = aFunc.__doc__
    return loggedFunc

