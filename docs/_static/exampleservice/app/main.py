from pathlib import Path
from typing import NoReturn

from app import __version__
from app.endpoints import ENDPOINTS

from fastapi_serviceutils import make_app

app = make_app(
    config_path=Path(__file__).with_name('config.yml'),
    version=__version__,
    endpoints=ENDPOINTS,
    enable_middlewares=['trusted_hosts',
                        'log_exception'],
    additional_middlewares=[]
)


def main() -> NoReturn:
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=app.config.service.port)


if __name__ == '__main__':
    main()
