import os
import log
import upip

DEPENDENCIES = []


def install_dependencies():
    log.info("install_dependencies")

    for (packageName, importName) in DEPENDENCIES:
        try:
            os.stat('/lib/' + importName)
        except OSError:
            log.info("installing %s" % packageName)
            upip.install(packageName)


def setup():
    install_dependencies()
