#!/workspaces/pmp01/.venv/bin/python
import sys
from adk.rpc.rpc_service import main
if __name__ == '__main__':
    sys.argv[0] = sys.argv[0].removesuffix('.exe')
    sys.exit(main())
