import logging


# create debuger
debuger = logging.getLogger("RL DEBUGGER")
debuger.setLevel(logging.INFO)
# define a Handler which writes INFO messages or higher to the sys.stderr
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
# set a format which is simpler for handler use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
handler.setFormatter(formatter)
# add the handler to the root debuger
debuger.addHandler(handler)