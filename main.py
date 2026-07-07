"""
main.py
The unified entry point application execution hook.
"""
from gui import SmartRouteApp

if __name__ == "__main__":
    # Launch application interface loop
    app = SmartRouteApp()
    app.mainloop()