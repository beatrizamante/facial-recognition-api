
app = FastAPI()

if __name__ == "__main__":
    server, logger = make_server()
    server.run()
    logger.debug("Housten, we have a %s", 'thorny problem')
