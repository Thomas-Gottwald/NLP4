def pytest_configure(config):
    import src.modules # NB this causes `src/core/__init__.py` to run
    # set up any "aliases" (optional...)
    import sys
    sys.modules['modules'] = sys.modules['src.modules']